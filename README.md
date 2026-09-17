# Claude Code setup

## 1. Add the output style

```sh
git clone https://github.com/HealthLeap/claude-readable.git
cd claude-readable
mkdir -p ~/.claude/output-styles
cp -i output-styles/simple-and-visual.md ~/.claude/output-styles/
```

## 2. Select it

Add this key to `~/.claude/settings.json`, keeping your existing settings:

```json
{
  "outputStyle": "simple-and-visual"
}
```

## Optional: add a reminder hook

Merge [style-reminder-hook.json](settings/style-reminder-hook.json) into `~/.claude/settings.json`. If `hooks.UserPromptSubmit` already exists, append the reminder to its array. Keep existing hooks.

## Optional: use the writing rule

```sh
mkdir -p ~/.claude/rules
cp -i rules/readable-artifacts.md ~/.claude/rules/
```

## 3. Start a fresh session

Open a new Claude Code session to apply the settings.

To customize the style, edit `~/.claude/output-styles/simple-and-visual.md`, then start another session.

---

[HealthLeap](https://www.healthleap.ai/) builds AI for hospitals. [We're hiring engineers](https://careers.healthleap.ai/).
