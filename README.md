# Claude Code setup

## Install as a plugin

Paste into your terminal:

```sh
claude plugin marketplace add HealthLeap/claude-readable && claude plugin install claude-readable@healthleap
```

Start a fresh Claude Code session. The output style, writing instructions, and per-prompt reminder are active automatically across your projects. The plugin uses its output style while enabled.

## Install through your agent

Paste this into Claude Code or another coding agent with access to your local files:

```text
Read https://raw.githubusercontent.com/HealthLeap/claude-readable/main/manual-setup.md and follow it to install the full Claude Readable setup for my user without the plugin. Preserve my existing settings and hooks.
```

This installs the same output style, writing rule, and per-prompt reminder directly into your Claude Code configuration. Start a fresh Claude Code session afterward.

## Uninstall the plugin

```sh
claude plugin uninstall claude-readable@healthleap
```

Start a fresh session to apply the change.

---

[HealthLeap](https://www.linkedin.com/company/healthleapinc) builds AI that helps hospital teams identify and treat patients missed by manual screening. [We're hiring engineers. Come build AI that saves lives.](https://careers.healthleap.ai/)
