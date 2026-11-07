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

Create a mode-specific file when absent: `source_dir/notes/progress/<notes-stem>-teach-progress.json` for `teach-me` or `source_dir/notes/progress/<notes-stem>-quiz-progress.json` for `quiz-me`. `<notes-stem>` is the notes filename without its final extension. During setup, resume that mode's file by default and ask before replacing or resetting it. Routine active-session updates need no repeated confirmation. Persist the matching shape:

```json
{
  "schema_version": 1,
  "mode": "teaching",
  "source": "source path",
  "notes": "matching notes path",
  "current_objective_id": "objective-02",
  "objectives": [
    {
      "id": "objective-02",
      "objective": "Explain the current concept",
      "status": "in_progress",
      "questions": [
        {
          "prompt": "Current unanswered question",
          "outcome": "pending"
        }
      ]
    }
  ],
  "session_preferences": {
    "assessment_emphasis": "balanced",
    "response_format": "short_answer"
  },
  "note_review_queue": []
}
```

For `quiz-me`, use the same structure with `"mode": "quizzing"`; use `successful`, `unsuccessful`, or `pending` question outcomes and omit `note_review_queue`.

During setup, create an empty objectives collection; add each objective when the loop encounters it. Each objective has a stable `id`, its text, a status (`in_progress`, `mastered`, or `skipped`), and one or more questions. `current_objective_id` must reference an existing objective; the last question on that objective is the question to resume. Do not predefine future objectives or persist chunks, concept coverage, or a separate assessment history.

In teaching, append each question with its outcome (`demonstrated`, `incomplete`, or `pending`) and any relevant gaps. Do not use attempt counters or success proportions.

In quizzing, append each question with its outcome (`successful`, `unsuccessful`, or `pending`) and any gaps. Derive counts or proportions from question outcomes when needed; do not persist them.

Save after issuing a question, receiving a response, clarifying or reassessing, completing an objective, reviewing notes, or changing notes.

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
