---
name: test-prep-setup
description: Interview a learner and create or validate the topic document, plan, and initial folders needed for prepare-for-test.
---

# Test Prep Setup

Set up test preparation without running quizzes.

## Intake

Ask for the tested topics, exclusions, coverage emphasis, preparation root, and a `test-topics.md` or equivalent mapping each topic to its source and notes. If no document exists, adapt [`assets/test-topics.md`](assets/test-topics.md) from the learner's answers and confirm it before continuing.

Treat the topic document as authoritative. Resolve links relative to its directory, retain anchors as scope locators, and verify every linked source and notes file is readable. If a source is unavailable, ask the learner to provide it. If notes are missing, do not invoke `notes-generator`; ask the learner to provide notes or invoke `notes-generator` themselves and return its reported path. If they refuse, use the source path as the notes path.

Show the interpreted scope, including every topic's source and notes, and direct the learner to the exact `test-topics.md` path. Revise it as needed and continue only after the learner confirms that the document is correct.

Then briefly describe the defaults: a balanced mix of recall, explanation, comparison, transfer, code or command interpretation, code or result tracing, workflow sequencing, and diagnosis or troubleshooting questions, answered in short form. Explain that the learner can change the question types and response format whenever a quiz starts or resumes.

Ask for approval to initialize the exact preparation root using those defaults. This single approval covers new workflow-managed topic, plan, progress, gap, and future pass files under that root; it does not authorize overwriting existing files or writing outside the root. Do not list every internal file path.

After approval, assign each source-and-notes pair a stable filename-safe ID and run:

```bash
python3 scripts/manage_test_plan.py init --root <prep-root> \
  --topics-file <test-topics-path> \
  --topic <id> <source-path> <notes-path> [--topic ...]
```

This creates canonical `test-topics.md`, immutable `test-plan.json`, and one `not_started` progress file per Pass 1 topic. It refuses inaccessible inputs and existing setup files.

For an existing workspace, run `scripts/manage_test_plan.py check --root <prep-root>`. Report the validated root, topic document, ordered topics, and next action to `prepare-for-test` or the learner.
