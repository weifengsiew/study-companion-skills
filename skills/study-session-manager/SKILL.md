---
name: study-session-manager
description: Internal lifecycle support for teach-me and quiz-me. Manage shared sessions and teach-me note updates when delegated or explicitly invoked.
---

# Study Session Manager

Support the session lifecycle for `teach-me` and `quiz-me`.

## 1. Set up session

Locate the exact source at `source_dir/<source-name>` and matching notes at `source_dir/notes/<notes-name>`, where `source_dir` contains the source:

- If either exact path is unknown, ask the learner to specify it.
- If the source is absent at its known path, ask the learner to place it there. Do not attempt note generation without it.
- If the source exists but the notes do not, invoke `notes-generator` with the host's skill-invocation syntax. Resume setup using the exact notes path it reports.
- If both files exist, inform the learner of both exact paths and continue.

Do not generate notes directly.

## 2. Persist progress

Use `scripts/manage_progress.py` for every progress-file operation; never read or edit progress JSON directly. Run it from this skill directory or use its absolute path. Common commands are:

```bash
python3 scripts/manage_progress.py init [--file <progress-path>] --source <source-path> --notes <notes-path> --assessment-emphasis <value> --response-format <value>
python3 scripts/manage_progress.py show --file <progress-path>
python3 scripts/manage_progress.py set-pending --file <progress-path> --question <text> --source-citation <locator> --notes-citation <locator>
python3 scripts/manage_progress.py record-answer --file <progress-path> --answer <text> --assessment <value> [--gap <text>]
```

`init` uses a learner-supplied `--file` exactly; otherwise, it derives `source_dir/notes/progress/<notes-stem>-progress.json`. It never overwrites an existing file. Resume with `show`; ask before replacing or resetting existing progress. Use `set-preferences` when session choices change. During `teach-me`, use `enqueue-review` and `clear-reviews`; during `quiz-me`, never use either review command. Use `<command> --help` for arguments and allowed values, or `schema` for the complete contract.

On resumption, continue a pending assessment when present. Otherwise, continue after the latest history entry's cited location, or start at the beginning when history is empty.

Persist through the script after every learner response, clarification, concept-group completion, note review, or note change.

## 3. Load learning preferences

Invoke `learning-preference-manager` with the host's skill-invocation syntax. Load confirmed `shared` and `teaching` preferences relevant to this session, apply the manager's precedence, and return them to the calling workflow. Continue if the profile is unavailable.

## 4. Choose session preferences

At the start of every session, ask the learner to choose:

1. **Assessment emphasis:** conceptual understanding, technical fluency, or a balanced mix.
2. **Response format:** multiple choice, short answer, or a mix.

Do not substitute saved preferences for this prompt. If the current request specifies either choice, use it and ask only for what is missing. These are session, not permanent learning, preferences. Save them in `session_preferences`, return and apply them throughout the session, and allow changes at any time. On resumption, ask again and replace the prior choices.

## 5. Manage teach-me note updates

Run this section only for `teach-me`. During `quiz-me`, do not enqueue explanations, review notes, propose replacements, or alter an existing `note_review_queue`.

After an initial or substantially adapted explanation, ask: "Is that clear, or should I explain it another way?" Continue explaining until the learner confirms it is clear.

Whenever a concept group is mastered during `teach-me`, enqueue its learning objective, corresponding note location, and any final confirmed explanation. A mastered group counts toward the threshold even when no new explanation was needed.

When the queue reaches three groups, review it before starting the next group. Compare recorded explanations with the current corresponding notes and propose a replacement only when an explanation materially improves clarity, organization, accuracy, or usefulness; do not propose equivalent rewording.

For each proposal, preserve all relevant source-supported detail, show the original and proposed wording, explain the improvement, and edit only with explicit confirmation. If no replacement is warranted, say so. After the review and the learner's response, clear those three entries through the script regardless of whether the proposals were accepted. Persist fewer than three entries across pauses and resumed sessions. Use an independent subagent only for complex or cross-subsection changes.

## 6. End session

When the learner explicitly pauses or ends the session, save progress, then invoke `learning-preference-manager` to propose preference changes. Save only confirmed changes; failure or refusal to update preferences must not prevent the session from ending.
