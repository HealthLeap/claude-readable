#!/usr/bin/env python3
"""Install selected Claude writing preferences while preserving existing config."""

import argparse
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
from datetime import datetime, timezone
from uuid import uuid4


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
STYLE_NAME = "simple-and-visual"


def read_json_object(path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key in {path}; resolve it first")
            result[key] = value
        return result

    try:
        result = json.loads(path.read_text(), object_pairs_hook=unique_keys)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}; no files changed") from error
    if not isinstance(result, dict):
        raise ValueError(f"Expected a JSON object in {path}; no files changed")
    return result


def reject_symlinks(path, configuration_root):
    # Replacing a symlink would bypass a user's canonical configuration file.
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise ValueError(f"Symlink at {candidate}; use manual setup instead")
        if candidate == configuration_root:
            break


def atomic_write(path, contents):
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
    descriptor, temporary_name = tempfile.mkstemp(prefix=".claude-readable-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(contents)
            output.flush()
            os.fsync(output.fileno())
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, path)
    finally:
        Path(temporary_name).unlink(missing_ok=True)


def plan_install(claude_dir, with_hook=False, with_writing_rule=False, replace=False):
    settings_path = claude_dir / "settings.json"
    reject_symlinks(settings_path, claude_dir)
    settings = read_json_object(settings_path) if settings_path.exists() else {}
    previous_settings = json.dumps(settings, sort_keys=True)
    settings["outputStyle"] = STYLE_NAME

    if with_hook:
        hooks = settings.setdefault("hooks", {})
        if not isinstance(hooks, dict):
            raise ValueError("Existing hooks must be an object; no files changed")
        groups = hooks.setdefault("UserPromptSubmit", [])
        if not isinstance(groups, list):
            raise ValueError("Existing UserPromptSubmit must be a list; no files changed")
        for group in groups:
            if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                raise ValueError("Malformed UserPromptSubmit group; no files changed")
            if not all(isinstance(handler, dict) for handler in group["hooks"]):
                raise ValueError("Malformed hook handler; no files changed")
        template = read_json_object(REPOSITORY_ROOT / "settings/style-reminder-hook.json")
        reminder_group = template["hooks"]["UserPromptSubmit"][0]
        reminder = reminder_group["hooks"][0]
        exists = any(
            handler.get("type") == reminder["type"]
            and handler.get("command") == reminder["command"]
            for group in groups
            for handler in group["hooks"]
        )
        if not exists:
            groups.append(reminder_group)

    relative_files = [Path("output-styles/simple-and-visual.md")]
    if with_writing_rule:
        relative_files.append(Path("rules/readable-artifacts.md"))

    changes = []
    for relative_path in relative_files:
        destination = claude_dir / relative_path
        reject_symlinks(destination, claude_dir)
        contents = (REPOSITORY_ROOT / relative_path).read_bytes()
        if destination.exists():
            if destination.read_bytes() == contents:
                continue
            if not replace:
                raise ValueError(f"Different file at {destination}; review it, then use --replace to back up and replace it")
        changes.append((destination, contents))

    if json.dumps(settings, sort_keys=True) != previous_settings:
        changes.append((settings_path, (json.dumps(settings, indent=2, ensure_ascii=False) + "\n").encode()))

    # Preflight every parent before changing any file.
    for path, _ in changes:
        for parent in path.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Expected directory at {parent}; no files changed")
    return changes


def install(args):
    claude_dir = Path(os.path.abspath(args.claude_dir.expanduser()))
    changes = plan_install(claude_dir, args.with_hook, args.with_writing_rule, args.replace)
    if not changes:
        print("Already installed. No files changed.")
        return
    for path, _ in changes:
        print(f"{'Would update' if args.dry_run else 'Will update'} {path}")
    if args.dry_run:
        print("Dry run complete. No files changed.")
        return

    existing_paths = [path for path, _ in changes if path.exists()]
    if existing_paths:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_dir = claude_dir / "claude-readable-backups" / f"{stamp}-{uuid4().hex[:8]}"
        reject_symlinks(backup_dir, claude_dir)
        backup_dir.mkdir(parents=True, mode=0o700)
        for path in existing_paths:
            backup = backup_dir / path.relative_to(claude_dir)
            backup.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            shutil.copy2(path, backup)
            os.chmod(backup, 0o600)
        print(f"Backups: {backup_dir}")

    for path, contents in changes:
        atomic_write(path, contents)
    print("Installed. Start a fresh Claude Code session to use simple-and-visual.")


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claude-dir", type=Path, default=Path.home() / ".claude", help="Configuration directory (default: ~/.claude)")
    parser.add_argument("--with-hook", action="store_true", help="Add the optional per-prompt reminder without replacing existing hooks")
    parser.add_argument("--with-writing-rule", action="store_true", help="Install the optional rule for PRs, tickets, and other artifacts")
    parser.add_argument("--replace", action="store_true", help="Back up and replace differing files owned by this setup")
    parser.add_argument("--dry-run", action="store_true", help="Validate and list changes without writing files")
    args = parser.parse_args()
    try:
        install(args)
    except (OSError, ValueError) as error:
        print(f"Installation stopped: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(cli())
