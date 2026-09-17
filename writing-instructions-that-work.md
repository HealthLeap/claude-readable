# Writing instructions that work

Start with a repeated failure you can describe and a result you can check. Add only the instruction needed to change that result.

## Put the instruction where it belongs

| Need | Mechanism | Example |
| --- | --- | --- |
| A consistent response format | Output style | Lead with the answer; use a table for a comparison when clearer |
| A convention relevant to ongoing work | Rule | Use the project's existing migration command |
| A task that needs reusable guidance | Skill | Interpret a particular export format and produce a reconciliation |
| An action at a lifecycle event | Hook | Print a style reminder when the user submits a prompt |
| Exact execution with little room for judgment | Script | Validate a config and merge only selected keys |

Output styles change Claude Code's system prompt. Rules add standing or path-scoped context. Skills load when invoked or selected as relevant. Hooks execute at specified events. These are different mechanisms, not interchangeable names for a long instruction file. [Output styles](https://code.claude.com/docs/en/output-styles), [rules](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [hooks](https://code.claude.com/docs/en/hooks)

If a fixed sequence can be encoded and checked, use a script. Leave judgment, interpretation, and tradeoffs in the skill. That is why this repo has a settings installer instead of asking an agent to reconstruct the merge each time.

## Make the instruction checkable

| Vague or ambiguous | More specific |
| --- | --- |
| Be concise | At most 150 words by default. Most answers should be shorter. |
| Write 150 words | 150 is a ceiling, not a target. Requested depth lifts it. |
| Make it readable | Put the decision first. Explain one idea per sentence. |
| Be careful with settings | Preserve unrelated keys and hook entries; back up files before changing them. |

A number is not enforcement. The [historical experiment](testing-readable-output.md#historical-comparison) motivated ceiling wording, but the model can still ignore it. Check whether the output actually follows the instruction and retains what matters.

## Diagnose loading before rewriting the body

A well-written skill cannot help if it is never selected. Its description should name the task and the language people use when asking for it. Include a boundary when a neighboring task is easy to confuse with it.

For a reconciliation skill, "Compare a bank CSV with an invoice export and identify unmatched payments" is more useful than "Help with finance." Test nearby requests, such as drafting an invoice email, that should not invoke it.

Claude Code exposes skill descriptions for selection before loading full skill content. Large references belong in supporting files linked from the body so they can be read when needed. A short description and focused body reduce irrelevant context; they do not guarantee selection. [Skill loading](https://code.claude.com/docs/en/skills)

## Give each instruction one owner

Keep response length in the output style. Let a writing rule own PR and ticket conventions. Let the hook point back to the style instead of carrying another copy of its budgets.

When behavior changes, check for old instructions that contradict the new ones. Search the rules, selected style, loaded skills, and host settings. Adding another instruction can leave the conflict intact.

The reminder hook is optional because output styles already receive built-in reminders. Compare with and without it instead of assuming another layer must help. [Output-style behavior](https://code.claude.com/docs/en/output-styles#how-output-styles-work)

## Remove instructions that don't change the result

Try the task without a line such as "write clean code" or "be thorough." If the result is unchanged, the line has not earned its place. Prefer a concrete project convention or failure mode the model would otherwise miss.

Keep necessary safeguards. A brevity exercise is not a reason to delete verification requirements, permission boundaries, or error details. Test the behavior you care about before removing its guidance.

## Test both use and non-use

For a skill, start with several prompts that should invoke it and several nearby prompts that should not. Run them repeatedly in fresh sessions with the same model and settings. Grade the completed task, not whether the agent followed your preferred sequence.

For a style, compare the same questions under Default, the custom style, and the custom style plus hook. Check answer correctness, preserved caveats, readability, and word count separately. A shorter wrong answer fails.

Retest after a model or workflow change. If removing an instruction no longer makes the result worse, consider retiring it while keeping the test that would catch a regression.

## Sources and further reading

| Source | Useful for |
| --- | --- |
| [Anthropic: skill authoring](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Focused instructions, appropriate freedom, and supporting references |
| [Philipp Schmid: testing skills](https://www.philschmid.de/testing-skills) | Trigger tests, repeated runs, and outcome evaluation |
| [Joe Cotellese: steering Claude Code](https://joecotellese.com/posts/steering-claude-code-bluf/) | Related answer-first guidance and a per-prompt reminder hook |

The defaults in this repository are preferences to adapt, not universal limits on how an agent should work.
