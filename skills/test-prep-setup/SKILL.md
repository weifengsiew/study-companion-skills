---
name: test-prep-setup
description: Interview a learner and create or validate the topic document, plan, and initial folders needed for prepare-for-test.
---

# Test Prep Setup

Set up test preparation without running quizzes.

## Intake

Ask for the tested topics, exclusions, coverage emphasis, preparation root, and a `test-topics.md` or equivalent mapping each topic to its source and notes. If no document exists, adapt [`assets/test-topics.md`](assets/test-topics.md) from the learner's answers and confirm it before continuing.

Treat the topic document as authoritative. Resolve links relative to its directory, retain anchors as scope locators, and verify every linked source and notes file is readable. If a source is unavailable, ask the learner to provide it. If notes are missing, do not invoke `notes-generator`; ask the learner to provide notes or invoke `notes-generator` themselves and return its reported path. If they refuse, use the source path as the notes path.

Summarize the interpreted scope and obtain confirmation. Ask once for question types, describing each:

- **Recall:** Define a term or identify a concept from its description.
- **Explanation:** Explain how or why something works.
- **Comparison:** Compare approaches, trade-offs, and suitable uses.
- **Transfer:** Apply a principle to an unfamiliar situation.
- **Code or command interpretation:** Explain what given code or a command does, including relevant options.
- **Code or result tracing:** Predict outputs, state changes, execution paths, or errors.
- **Workflow sequencing:** Explain or arrange the steps required to complete a technical task.
- **Diagnosis and troubleshooting:** Identify probable causes and propose appropriate investigations or fixes.

Offer conceptual, technical, balanced, and custom mixes. Then ask for response format, assign each source-and-notes pair a stable filename-safe ID, and run:

```bash
python3 scripts/manage_test_plan.py init --root <prep-root> \
  --topics-file <test-topics-path> \
  --question-type <value> [--question-type <value> ...] --response-format <value> \
  --topic <id> <source-path> <notes-path> [--topic ...]
```

Before running `init`, show the learner the exact preparation root, canonical topic document, test plan, and initial progress-file paths, and proceed only after explicit approval.

This creates canonical `test-topics.md`, immutable `test-plan.json`, and one `not_started` progress file per Pass 1 topic. It refuses inaccessible inputs and existing setup files.

For an existing workspace, run `scripts/manage_test_plan.py check --root <prep-root>`. Report the validated root, topic document, ordered topics, and initialized progress files to `prepare-for-test` or the learner. After creating a workspace, report every created path; when delegated, `prepare-for-test` must relay them to the learner.
