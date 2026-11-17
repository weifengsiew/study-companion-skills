---
name: prepare-for-test
description: Run persistent, multi-pass test preparation that quizzes all material once, then repeatedly targets recorded gaps until a pass produces none.
---

# Prepare For Test

Orchestrate `test-prep-setup`, `quiz-me`, and `gaps-extractor`. Do not perform their work or edit progress JSON directly.

Before any delegated action creates files, tell the learner the exact planned paths and proceed only after explicit approval. Approval covers only the paths presented; obtain fresh approval for files introduced by a later pass. After creation, report the exact created paths.

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
- `initialize_pass`: obtain question types and then response format, then run `scripts/manage_test_prep.py init-pass --root <prep-root> --pass-number <n> --question-type <value> [--question-type <value> ...] --response-format <value>`.
- `extract_gaps`: invoke `gaps-extractor` with the returned progress and gaps directories, then check status again.
- `setup_required`: invoke `test-prep-setup`.
- `workflow_complete`: report mastery completion and stop.

There is no pass limit. Every recorded gap enters the next pass, even if its immediate retry was correct. Mastery is reached when a completed pass produces zero gaps.
