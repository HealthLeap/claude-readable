# Make Claude concise and readable

Claude Opus can be exhausting to read. This is the setup I use to get the answer first, plain language, and explanations I can follow without rereading them.

The built-in Concise style wasn't enough for me. After trying combinations of rules, skills, and hooks, I settled on a custom output style with explicit length ceilings and instructions for readable structure.

Use the setup below, then read [Writing instructions that work](writing-instructions-that-work.md) to adapt it. This is a personal configuration shared by Tamir Shklaz at HealthLeap.

## Install

Requires Claude Code and Python 3.10 or later. The installer supports macOS and Linux. Windows users can copy the style manually; the optional hook uses a POSIX shell.

```sh
git clone https://github.com/HealthLeap/claude-readable.git
cd claude-readable
python3 scripts/install-claude-readable.py --dry-run
python3 scripts/install-claude-readable.py
```

Start a new Claude Code session. The installer selects `simple-and-visual` in `~/.claude/settings.json` and copies the [output style](output-styles/simple-and-visual.md). It preserves other settings, backs up changed files, and refuses to overwrite a different style file unless you pass `--replace`.

To include the optional reminder hook and writing rule:

```sh
python3 scripts/install-claude-readable.py --with-hook --with-writing-rule
```

| Component | What it changes |
| --- | --- |
| [Output style](output-styles/simple-and-visual.md) | Response length, wording, and structure |
| [Reminder hook](settings/style-reminder-hook.json) | Adds a short pointer to the style with each submitted prompt |
| [Writing rule](rules/readable-artifacts.md) | PR descriptions, tickets, comments, and other writing produced for readers |

The installer does not edit permissions, model selection, existing rules, or other hooks. Rerunning the same installation makes no changes. Use `--claude-dir /path/to/project/.claude` to install into a project's shared configuration instead of your user configuration.

## What an output style does

An output style is a Markdown file with frontmatter. Claude Code adds its instructions to the system prompt, making it suitable for response preferences you want throughout the conversation. A skill loads instructions for a relevant task; an output style sets the main conversation's voice and format. [Official documentation](https://code.claude.com/docs/en/output-styles)

This style includes:

```yaml
name: simple-and-visual
description: Answer-first replies with plain language and explicit length ceilings.
keep-coding-instructions: true
```

The last field matters: custom styles otherwise leave out Claude Code's built-in software engineering instructions. Preserving those instructions does not prove that a shorter answer retained every important fact; review the result too.

The style asks for the answer first, one thought per sentence, and structure that makes the content easier to follow. Its length limits are ceilings, not targets. Requested depth and necessary error, risk, and reasoning details take precedence.

## Manual setup

Copy [simple-and-visual.md](output-styles/simple-and-visual.md) into `~/.claude/output-styles/`. Back up any existing file with that name first. Merge this key into `~/.claude/settings.json`:

```json
{
  "outputStyle": "simple-and-visual"
}
```

Keep your other settings. Alternatively, select the style through `/config` → Output style in the terminal. That menu saves a project-local selection. Start a new session or use `/clear` for the new style to take effect. [Selection and scope](https://code.claude.com/docs/en/output-styles#change-your-output-style)

For the optional components, merge the `UserPromptSubmit` entry from [style-reminder-hook.json](settings/style-reminder-hook.json) into your existing hooks, and copy [readable-artifacts.md](rules/readable-artifacts.md) into `~/.claude/rules/`. Review existing writing rules for duplicate instructions before enabling another one.

## Why the hook is optional

A `UserPromptSubmit` command hook runs before Claude processes your prompt. Text it prints successfully is added to Claude's context. Ours prints a short reminder to follow the selected style; it does not read your prompt, call a service, or enforce a word count. [Hook behavior](https://code.claude.com/docs/en/hooks#userpromptsubmit)

Claude Code already adds reminders for output styles. Try the style alone first, then compare with the hook if you still see drift. The extra reminder is a hypothesis to test, not a guaranteed improvement.

## If the style doesn't apply

1. Start a fresh session after changing the selected style.
2. Check project and local settings for an `outputStyle` that overrides your user setting.
3. Match the selected value to the style's frontmatter `name`. Without `name`, Claude uses the filename. Matching all three is convenient, not a requirement.
4. Check whether your host application or an enabled plugin supplies its own style or system-prompt override. For Conductor, consult its [agent controls](https://conductor.build/docs/reference/agent-behavior). Host-specific behavior can change between releases.

Output styles apply to the main conversation. Ordinary subagents have their own system prompts; forks inherit the parent's. This setup does not claim to configure every agent in a team. [Scope](https://code.claude.com/docs/en/output-styles#how-output-styles-work)

## Undo

Select your previous output style. Remove only the reminder entry shown in [style-reminder-hook.json](settings/style-reminder-hook.json) from `hooks.UserPromptSubmit`, if installed. Remove the optional `readable-artifacts.md` rule and the installed style only if you no longer use them.

The installer prints a backup directory for overwritten files. Restore those copies only if you have made no later changes to the originals; otherwise merge the relevant settings by hand. Start a fresh session.

## Test it on your work

See [Testing the setup](testing-readable-output.md) for the small historical comparison and a repeatable evaluation method. Shorter output alone does not establish better reasoning or correctness.

For the broader principles, read [Writing instructions that work](writing-instructions-that-work.md).
