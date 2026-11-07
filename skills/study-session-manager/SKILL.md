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

Create `source_dir/notes/progress/<notes-stem>-progress.json` when absent; `<notes-stem>` is the notes filename without its final extension. During setup, resume an existing file by default and ask before replacing or resetting it. Routine active-session updates need no repeated confirmation. Persist exactly this shape:

```json
{
  "schema_version": 1,
  "source": "source path",
  "notes": "matching notes path",
  "current_chunk_id": "chunk-03",
  "chunks": [
    {
      "id": "chunk-03",
      "title": "Chunk title",
      "status": "in_progress",
      "attempt_count": 0,
      "successful_attempt_count": 0,
      "successful_attempt_proportion": null,
      "unsuccessful_attempt_gaps": [],
      "pending_question": "Current unanswered question",
      "latest_attempt": null
    }
  ],
  "session_preferences": {
    "assessment_emphasis": "balanced",
    "response_format": "short_answer"
  },
  "note_review_queue": []
}
```

During setup, identify all required concept groups, create the complete ordered `chunks` collection before the first live question, and assign each chunk a stable `id` and source- or notes-derived `title`. `chunks` is the source of truth; statuses are `untested`, `in_progress`, `mastered`, or `skipped`. `current_chunk_id` must reference a chunk; derive previous and future chunks from its position. Do not persist `concept_coverage` or `assessment_history`.

Overwrite `latest_attempt` after each response; do not store older responses. Increment `attempt_count` for every response and `successful_attempt_count` only when the learner demonstrates the objective. Set `successful_attempt_proportion` to `null` with no attempts, otherwise to `successful_attempt_count / attempt_count`. Store latest gaps in `latest_attempt.gaps` and unresolved gaps in `unsuccessful_attempt_gaps`, removing resolved gaps.

Save after issuing a question, receiving a response, clarifying or reassessing, completing a concept group, reviewing notes, or changing notes.

## 3. Load learning preferences

Invoke `learning-preference-manager` with the host's skill-invocation syntax. Load confirmed `shared` and `teaching` preferences relevant to this session, apply the manager's precedence, and return them to the calling workflow. Continue if the profile is unavailable.

## 4. Choose session preferences

At the start of every session, ask the learner to choose:

1. **Assessment emphasis:** conceptual understanding, technical fluency, or a balanced mix.
2. **Response format:** multiple choice, short answer, or a mix.

Do not substitute saved preferences for this prompt. If the current request specifies either choice, use it and ask only for what is missing. These are session, not permanent learning, preferences. Save them in `session_preferences`, return and apply them throughout the session, and allow changes at any time. On resumption, ask again and replace the prior choices.

## 5. Manage teach-me note updates

Use this section only for `teach-me`; `quiz-me` leaves `note_review_queue` unchanged and does not enqueue, review, or edit notes.

After each initial or substantially adapted explanation, ask: "Is that clear, or should I explain it another way?" Re-explain until the learner confirms.

When a concept group is mastered, enqueue its learning objective, note location, and any final confirmed explanation. Count the group toward the three-group threshold even when no new explanation was needed.

Before starting the next group after the queue reaches three, compare each explanation with its current note. Propose a replacement only for a material improvement in clarity, organization, accuracy, or usefulness; do not suggest equivalent wording. For each proposal, retain relevant source-supported detail, show the original and proposed text, explain the improvement, and edit only with explicit confirmation. If no replacement is warranted, say so. After the learner responds, clear those three entries regardless of acceptance. Persist fewer than three entries across pauses and resumption. Use an independent subagent only for complex or cross-subsection changes.

## 6. End session

When the learner explicitly pauses or ends the session, save progress, then invoke `learning-preference-manager` to propose preference changes. Save only confirmed changes; failure or refusal to update preferences must not prevent the session from ending.
