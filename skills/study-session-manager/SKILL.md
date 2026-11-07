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

Invoke `progress-state-manager` with the mode and exact source and notes paths to create or resume the mode-specific file, record objective and question updates, and save each state change. Routine updates need no repeated confirmation.

## 3. Load learning preferences

Invoke `learning-preference-manager` with the host's skill-invocation syntax. Load confirmed `shared` and `teaching` preferences relevant to this session, apply the manager's precedence, and return them to the calling workflow. Continue if the profile is unavailable.

## 4. Choose session preferences

At the start of every session, ask the learner to choose:

1. **Assessment emphasis:** conceptual understanding, technical fluency, or a balanced mix.
2. **Response format:** multiple choice, short answer, or a mix.

Do not substitute saved preferences for this prompt. If the current request specifies either choice, use it and ask only for what is missing. These are session, not permanent learning, preferences. Save them in `session_preferences`, return and apply them throughout the session, and allow changes at any time. On resumption, ask again and replace the prior choices.

## 5. Manage teach-me note updates

Use this section only for `teach-me`; `quiz-me` leaves `note_review_queue` unchanged.

After each initial or substantially adapted explanation, ask: "Is that clear, or should I explain it another way?" Re-explain until confirmed.

When a concept group is mastered, enqueue its objective, note location, and final confirmed explanation; count it toward the three-group threshold even without a new explanation.

When the queue reaches three, review it before the next group. Compare each explanation with its note and propose replacements only for material improvements in clarity, organization, accuracy, or usefulness. For each proposal, retain source-supported detail, show original and proposed text, explain the improvement, and edit only with explicit confirmation; say when no replacement is warranted. After the learner responds, clear the three entries regardless of acceptance. Persist fewer than three entries across pauses. Use an independent subagent only for complex or cross-subsection changes.

## 6. End session

When the learner explicitly pauses or ends the session, save progress, then invoke `learning-preference-manager` to propose preference changes. Save only confirmed changes; failure or refusal to update preferences must not prevent the session from ending.
