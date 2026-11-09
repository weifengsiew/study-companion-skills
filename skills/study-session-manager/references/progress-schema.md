# Progress JSON contract

Use exactly the structure and key order in [`progress-example.json`](progress-example.json). Do not add fields.

## Field rules

- `source` and `notes` are the exact session paths; `current_chunk.subsection` is the current subsection label.
- `current_chunk.status` is one of `in_progress`, `paused`, or `completed`.
- `current_chunk.pending_question` is the exact unanswered question, or `null` when no answer is pending.
- Coverage arrays contain ordered, unique concept-group names, with the same exact name used across arrays.
- Append one chronological `assessment_history` entry per assessed answer; store the rendered learner response in `answer`.
- `assessment_history[].assessment` is one of `correct`, `partially_correct`, or `incorrect`.
- `assessment_history[].gaps` lists concise missing or mistaken concepts; use `[]` for a correct answer.
- `session_preferences.assessment_emphasis` is one of `conceptual understanding`, `technical fluency`, or `balanced mix`.
- `session_preferences.response_format` is one of `multiple choice`, `short answer`, or `mix`.
- Each `note_review_queue` entry has exactly this shape; use `null` for `confirmed_explanation` when no new explanation was needed:

```json
{
  "learning_objective": "Explain Concept 1",
  "note_location": "## 1 · Topic name",
  "confirmed_explanation": null
}
```

## Coverage invariants

- `mastered ⊆ tested ⊆ required`.
- `remaining` is `required` minus `mastered`, in `required` order.
