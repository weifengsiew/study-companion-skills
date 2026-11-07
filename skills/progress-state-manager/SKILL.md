---
name: progress-state-manager
description: Internal persistence support for teach-me and quiz-me. Load, update, and save objective-based study progress when delegated.
---

# Progress State Manager

Manage the mode-specific progress file for `teach-me` and `quiz-me`.

## Files and schema

Use `source_dir/notes/progress/<notes-stem>-teach-progress.json` for `teach-me` and `source_dir/notes/progress/<notes-stem>-quiz-progress.json` for `quiz-me`. `<notes-stem>` is the notes filename without its final extension. Resume an existing file by default; ask before replacing or resetting it.

Persist this common shape:

```json
{
  "schema_version": 1,
  "source": "source path",
  "notes": "notes path",
  "current_objective_id": "objective-02",
  "objectives": [
    {
      "id": "objective-02",
      "objective": "Explain the current concept",
      "status": "in_progress",
      "questions": [
        {
          "prompt": "Question text",
          "outcome": "pending"
        }
      ]
    }
  ],
  "session_preferences": {},
  "note_review_queue": []
}
```

Omit `note_review_queue` from quiz progress. Add objectives as the loop encounters them; do not predefine future objectives. Each objective has a stable ID, objective text, status (`in_progress`, `mastered`, or `skipped`), and one or more questions. `current_objective_id` must reference an existing objective; its last question is the resume point.

For teaching, question outcomes are `demonstrated`, `incomplete`, or `pending`. For quizzing, they are `successful`, `unsuccessful`, or `pending`. Store relevant gaps on the question. Derive counts or proportions from quiz question outcomes when needed; do not persist them.

## Updates

On each question or response, append the question record to its objective, update the objective status, and set `current_objective_id`. Save after issuing a question, receiving a response, clarifying or reassessing, completing an objective, reviewing notes, or changing notes. Do not store a separate assessment history or older response fields beyond the recorded question details.
