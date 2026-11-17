---
name: prepare-for-test
description: Run persistent, multi-pass test preparation that quizzes all material once, then repeatedly targets recorded gaps until a pass produces none.
---

# Prepare For Test

Orchestrate `test-prep-setup`, `quiz-me`, and `gaps-extractor`. Do not perform their work or edit progress JSON directly.

## Open

At the start of a directly requested workflow, say exactly:

> Hi! I’ll help you prepare for your test. First, I’ll quiz you across all the tested material. Each new round will focus on the knowledge gaps found in the previous one until no gaps remain. Your progress will be saved, so you can pause and resume at any time. Let’s start by confirming the tested topics and where their source materials and notes are located.

If the learner has already supplied all required topics, source material, and notes, omit only the final sentence and continue with them.

Before initialization, tell the learner the exact preparation root and obtain the single workspace approval defined by `test-prep-setup`. That approval covers new workflow-managed files under the root, including future passes; do not request approval for each internal file. It does not authorize overwrites or files outside the root.

## Set up

Invoke `test-prep-setup` for a new workspace or to validate an existing one. Use the exact root, authoritative topic document, ordered topic scope, and readable source-and-notes paths it returns. Pass 1 assesses only that scope.

Store independent state in numbered pass directories:

```text
progress/
├── pass_01/progress/<topic>-progress.json
├── pass_02/gaps/{_manifest.json,<topic>-gaps.json}
├── pass_02/progress/<topic>-progress.json
└── pass_03/...
```

## Run passes

At every start, resumption, or completed quiz, run:

```bash
python3 scripts/manage_test_prep.py status --root <prep-root>
```

Follow its single `next_action`:

- `resume_pending`, `resume_quiz`, or `start_quiz`: invoke `quiz-me` with the returned source, notes, progress file, and optional gaps file.
- `initialize_pass`: run `scripts/manage_test_prep.py init-pass --root <prep-root> --pass-number <n>` to use the defaults. `study-session-manager` asks the learner for question types and response format when the quiz starts or resumes, so those choices may replace the stored defaults.
- `extract_gaps`: invoke `gaps-extractor` with the returned progress and gaps directories, then check status again.
- `setup_required`: invoke `test-prep-setup`.
- `workflow_complete`: report mastery completion and stop.

There is no pass limit. Every recorded gap enters the next pass, even if its immediate retry was correct. Mastery is reached when a completed pass produces zero gaps.
