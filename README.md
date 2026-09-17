# Make Claude Opus concise and readable

I love Opus. Reading its answers was exhausting. Even the built-in Concise style wasn't getting me there.

This is my setup: a custom output style for answer-first replies, plain language, and readable structure, plus an optional reminder hook and writing rule.

## 1. Add the output style

Clone this repo and copy the style into Claude Code's output-styles folder:

```sh
git clone https://github.com/HealthLeap/claude-readable.git
cd claude-readable
mkdir -p ~/.claude/output-styles
cp -i output-styles/simple-and-visual.md ~/.claude/output-styles/
```

An output style adds your writing instructions to Claude's system prompt. This one asks for the answer first, short sentences, and explicit length ceilings. Requested depth and necessary reasoning, risks, and error details take precedence over those ceilings.

The file includes `keep-coding-instructions: true` to preserve Claude Code's built-in engineering instructions. [How output styles work](https://code.claude.com/docs/en/output-styles)

## 2. Select it

Add this key to `~/.claude/settings.json`, keeping your existing settings:

```json
{
  "outputStyle": "simple-and-visual"
}
```

Start a fresh Claude Code session. You can also select the style through `/config` → Output style in the terminal; that selection applies to the current project.

To customize it, edit your installed `~/.claude/output-styles/simple-and-visual.md`. Use ceilings, not targets: “150 words maximum. Most answers should be shorter.” Start a fresh session after changes.

## Optional: add a reminder hook

A `UserPromptSubmit` hook runs whenever you send a prompt. This one adds a short reminder to follow the style without repeating all its instructions. Claude Code already provides output-style reminders, so this extra hook is optional. [How hooks work](https://code.claude.com/docs/en/hooks#userpromptsubmit)

Merge the `hooks` entry from [style-reminder-hook.json](settings/style-reminder-hook.json) into `~/.claude/settings.json`. If you already have hooks, append the reminder to `UserPromptSubmit` rather than replacing your existing entries. Start a fresh session.

## Optional: use the writing rule

The [writing rule](rules/readable-artifacts.md) covers PR descriptions, tickets, review comments, and other writing produced for readers:

```sh
mkdir -p ~/.claude/rules
cp -i rules/readable-artifacts.md ~/.claude/rules/
```

Keep each instruction in one place. The output style owns conversation formatting; the rule owns artifact writing; the hook points back to the style. Remove duplicate writing guidance from your own configuration when adopting it.

---

[HealthLeap](https://www.healthleap.ai/) builds AI for hospitals. [We're hiring engineers](https://careers.healthleap.ai/).
