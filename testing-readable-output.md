# Testing readable output

## Historical comparison

The author recorded this small comparison during development. One fixed prompt was run twice under each output-style framing with `claude-opus-5[1m]` through `claude -p`.

Prompt: "Should I use Apache Iceberg or Delta Lake for a new lakehouse on S3? Walk me through the considerations."

| Framing | Response words | Mean |
| --- | --- | --- |
| Built-in Default | 198, 252 | 225 |
| Numbers framed as a budget or target | 247, 300 | 273.5 |
| Numbers framed as ceilings, with permission to be shorter | 183, 161 | 172 |

The ceiling arm was about 24% shorter than Default on this prompt. The explanation that a budget encourages filling the space is a hypothesis; the counts establish only the observed difference.

These are historical reported measurements. Raw transcripts and the exact three historical style files are not included, and the comparison was not rerun to validate this repository's current files. It does not isolate the optional hook, measure correctness, or establish a general improvement across tasks.

The author also reports experimenting across 20 runs on different tasks. Those runs are separate from the six observations above; this repository does not publish an aggregate result for them.

## Evaluate your own setup

Use prompts representative of your work: a factual lookup, a comparison, a bug explanation, a change report, and a request for detailed reasoning. Include a failing-test example and an uncertain result so you can detect harmful omission.

Compare Default, this output style, and this output style with the hook. Keep the model, effort, task inputs, and available tools constant. Start each run in a fresh session. Repeat each case and vary the order of the configurations.

| Check | What to record |
| --- | --- |
| Correctness | Whether the answer and recommendation are supported |
| Completeness | Required facts, failures, uncertainty, and risks retained |
| Readability | Whether the answer is understandable on the first pass |
| Length | Response word count, separately from reasoning or tool tokens |
| Preference | Which response you would choose without seeing the style label |

Save the prompt, full output, model identifier, Claude Code version, style file, hook setting, and score for each run. Report task-level variation along with averages. Do not convert fewer response words into a claim about faster engineering or unchanged reasoning quality.

## Installer checks

The installer tests run against temporary directories, not your real Claude configuration:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

They check settings preservation, backups, repeat installation, optional hook execution, and refusal of malformed or conflicting configuration. Passing these checks establishes installer behavior, not model performance.
