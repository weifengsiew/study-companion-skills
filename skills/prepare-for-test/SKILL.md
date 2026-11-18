---
name: prepare-for-test
description: Run persistent test preparation that completes each topic's first pass and gap-focused passes before moving to the next topic.
---

# Prepare For Test

Orchestrate `test-prep-setup`, `quiz-me`, and `gaps-extractor`. Do not perform their work or edit progress JSON directly.

## Open

At the start of a directly requested workflow, say exactly:

> Hi! I’ll help you prepare for your test. We’ll work through each topic in order: first covering the topic, then focusing on its knowledge gaps until none remain before moving to the next topic. Your progress will be saved, so you can pause and resume at any time. Let’s start by confirming the tested topics and where their source materials and notes are located.

If the learner has already supplied all required topics, source material, and notes, omit only the final sentence and continue with them.

Before initialization, tell the learner the exact preparation root and obtain the single workspace approval defined by `test-prep-setup`. That approval covers new workflow-managed files under the root, including future passes; do not request approval for each internal file. It does not authorize overwrites or files outside the root.

## Set up

Invoke `test-prep-setup` for a new workspace or to validate an existing one. Use the exact root, authoritative topic document, ordered topic scope, and readable source-and-notes paths it returns. Each topic's Pass 1 assesses only that topic's scope.

Store independent state in numbered pass directories:

```text
progress/
├── <topic>/pass_01/progress.json
├── <topic>/pass_02/{gaps.json,progress.json}
└── <topic>/pass_03/...
```

## Run passes

At every start, resumption, or completed quiz, run:

```bash
python3 scripts/manage_test_prep.py status --root <prep-root>
```

Follow its single `next_action`:

- `resume_pending`, `resume_quiz`, or `start_quiz`: invoke `quiz-me` with the returned source, notes, progress file, and optional gaps file.
- `initialize_pass`: run `scripts/manage_test_prep.py init-pass --root <prep-root> --topic <topic> --pass-number <n>` to use the defaults. `study-session-manager` asks the learner for question types and response format when the quiz starts or resumes, so those choices may replace the stored defaults.
- `extract_gaps`: create the returned gaps file's parent directory if needed, invoke `gaps-extractor` with the returned progress file and gaps file, then check status again.
- `setup_required`: invoke `test-prep-setup`.
- `workflow_complete`: report mastery completion and stop.

Complete each topic's first pass and all required gap-focused passes before moving to the next topic. There is no pass limit. Every recorded gap enters the next pass, even if its immediate retry was correct. Mastery is reached when every topic produces a pass with zero gaps.
