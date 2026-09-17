"""Exercise configuration mutations in isolated directories."""

import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
INSTALLER = REPOSITORY_ROOT / "scripts/install-claude-readable.py"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.claude_dir = self.root / "claude configuration"

    def run_installer(self, *flags, expected=0):
        result = subprocess.run(
            [sys.executable, str(INSTALLER), "--claude-dir", str(self.claude_dir), *flags],
            text=True, capture_output=True, timeout=10,
        )
        self.assertEqual(result.returncode, expected, result.stderr)
        return result

    def seed_settings(self, text):
        self.claude_dir.mkdir(parents=True)
        path = self.claude_dir / "settings.json"
        path.write_text(text)
        return path

    def snapshot(self):
        return {str(path.relative_to(self.claude_dir)): path.read_bytes()
                for path in self.claude_dir.rglob("*") if path.is_file()}

    def test_clean_install_and_repeat_are_idempotent(self):
        self.run_installer()
        settings = json.loads((self.claude_dir / "settings.json").read_text())
        self.assertEqual(settings, {"outputStyle": "simple-and-visual"})
        self.assertFalse((self.claude_dir / "rules").exists())
        before = self.snapshot()
        self.run_installer()
        self.assertEqual(self.snapshot(), before)

    def test_dry_run_does_not_create_directory(self):
        self.run_installer("--dry-run", "--with-hook", "--with-writing-rule")
        self.assertFalse(self.claude_dir.exists())

    def test_preserves_settings_and_hooks_and_backs_up_exact_bytes(self):
        original = '{"model":"chosen-model","permissions":{"deny":["Bash(rm *)"]},"hooks":{"Stop":[{"hooks":[{"type":"command","command":"true"}]}],"UserPromptSubmit":[{"hooks":[{"type":"command","command":"echo existing"}]}]}}\n'
        path = self.seed_settings(original)
        path.chmod(0o640)
        self.run_installer("--with-hook", "--with-writing-rule")
        settings = json.loads(path.read_text())
        old = json.loads(original)
        self.assertEqual(settings["model"], old["model"])
        self.assertEqual(settings["permissions"], old["permissions"])
        self.assertEqual(settings["hooks"]["Stop"], old["hooks"]["Stop"])
        self.assertEqual(settings["hooks"]["UserPromptSubmit"][0], old["hooks"]["UserPromptSubmit"][0])
        self.assertEqual(len(settings["hooks"]["UserPromptSubmit"]), 2)
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o640)
        backups = list((self.claude_dir / "claude-readable-backups").glob("*/settings.json"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), original)
        self.assertEqual(stat.S_IMODE(backups[0].stat().st_mode), 0o600)
        before = self.snapshot()
        self.run_installer("--with-hook", "--with-writing-rule")
        self.assertEqual(self.snapshot(), before)

    def test_refuses_bad_settings_without_partial_writes(self):
        for value in ["not json", "[]", '{"model":"one","model":"two"}', '{"hooks":[]}', '{"hooks":{"UserPromptSubmit":{}}}', '{"hooks":{"UserPromptSubmit":[{"hooks":[null]}]}}']:
            with self.subTest(value=value):
                if not self.claude_dir.exists():
                    self.claude_dir.mkdir()
                path = self.claude_dir / "settings.json"
                path.write_text(value)
                before = self.snapshot()
                self.run_installer("--with-hook", expected=1)
                self.assertEqual(self.snapshot(), before)

    def test_conflict_requires_replace_and_keeps_backup(self):
        style = self.claude_dir / "output-styles/simple-and-visual.md"
        style.parent.mkdir(parents=True)
        style.write_text("My existing style\n")
        before = self.snapshot()
        self.run_installer(expected=1)
        self.assertEqual(self.snapshot(), before)
        self.run_installer("--replace")
        backups = list((self.claude_dir / "claude-readable-backups").glob("*/output-styles/simple-and-visual.md"))
        self.assertEqual(backups[0].read_text(), "My existing style\n")
        self.assertEqual(style.read_bytes(), (REPOSITORY_ROOT / "output-styles/simple-and-visual.md").read_bytes())

    def test_symlink_settings_are_not_replaced(self):
        self.claude_dir.mkdir()
        original = self.root / "canonical-settings.json"
        original.write_text('{"model":"keep"}')
        settings = self.claude_dir / "settings.json"
        settings.symlink_to(original)
        self.run_installer(expected=1)
        self.assertTrue(settings.is_symlink())
        self.assertEqual(original.read_text(), '{"model":"keep"}')

    def test_symlink_configuration_directory_is_not_followed(self):
        actual = self.root / "canonical-config"
        actual.mkdir()
        self.claude_dir.symlink_to(actual, target_is_directory=True)
        self.run_installer(expected=1)
        self.assertEqual(list(actual.iterdir()), [])

    def test_hook_runs_without_reading_or_expanding_prompt(self):
        self.run_installer("--with-hook")
        settings = json.loads((self.claude_dir / "settings.json").read_text())
        command = settings["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
        result = subprocess.run(
            ["sh", "-c", command], input='{"prompt":"$(touch should-not-exist)"}',
            capture_output=True, text=True, cwd=self.root, timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("simple-and-visual", result.stdout)
        self.assertNotIn("touch", result.stdout)
        self.assertFalse((self.root / "should-not-exist").exists())

    def test_invalid_parent_is_detected_before_any_write(self):
        self.claude_dir.mkdir()
        (self.claude_dir / "rules").write_text("A file, not a directory")
        before = self.snapshot()
        self.run_installer("--with-writing-rule", expected=1)
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
