# Install without the plugin

Install the output style, writing rule, and per-prompt reminder for the current user. Use `CLAUDE_CONFIG_DIR` if set; otherwise use `~/.claude`.

## 1. Get the files

Read or clone [HealthLeap/claude-readable](https://github.com/HealthLeap/claude-readable). Use these files from the same checkout:

| Source | Destination under the Claude configuration directory |
| --- | --- |
| [output-styles/simple-and-visual.md](https://raw.githubusercontent.com/HealthLeap/claude-readable/main/output-styles/simple-and-visual.md) | `output-styles/simple-and-visual.md` |
| [rules/readable-artifacts.md](https://raw.githubusercontent.com/HealthLeap/claude-readable/main/rules/readable-artifacts.md) | `rules/readable-artifacts.md` |

Create missing directories. Back up existing destination files before replacing them. Skip files whose contents already match.

## 2. Select the style

Read the existing `settings.json` in that configuration directory. Back it up before changing it. If it does not exist, create a JSON object.

Set `outputStyle` to `simple-and-visual`. Preserve all unrelated settings. If the existing JSON cannot be parsed, stop and report the error rather than replacing it.

The style's `force-for-plugin` field applies only to plugin installs. This manual installation selects the style through `outputStyle`.

## 3. Add the reminder

Read [hooks/claude-readable-hooks.json](https://raw.githubusercontent.com/HealthLeap/claude-readable/main/hooks/claude-readable-hooks.json). Append its `hooks.UserPromptSubmit` group to `settings.json` under `hooks.UserPromptSubmit`, creating the object and array if absent. If that reminder command is already present, do not add it again. Preserve other hooks.

Do not copy the `SessionStart` hook. It references a plugin-only path; the writing rule installed in step 1 loads directly from the user's rules directory instead.

## 4. Finish

If `claude-readable@healthleap` is already enabled, disable it to avoid loading the setup twice:

```sh
claude plugin disable claude-readable@healthleap
```

Check that the saved settings parse as JSON and both installed files exist. Report the installed paths and any backup paths. Tell the user to start a fresh Claude Code session.

Keep model selection, permissions, unrelated rules, and unrelated plugins unchanged.
