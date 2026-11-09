# Progress JSON contract

Use exactly the structure and key order in [`progress-example.json`](progress-example.json). Do not add fields.

## Field rules

- `source` and `notes` are the exact session paths.
- `pending_assessment` is `null` when no answer is pending. Otherwise, it contains the exact rendered question and its citations.
- Each `citations.source` and `citations.notes` value is a non-empty array of ordered, unique in-file locators relevant to the question. Use the strongest stable locator the format supports, such as a section or heading, a PDF page and heading, or a notebook heading or cell. Prefer stable labels over line numbers.
- Append one chronological `assessment_history` entry per assessed answer; store the rendered learner response in `answer`.
- `assessment_history[].assessment` is one of `correct`, `partially_correct`, or `incorrect`.
- `assessment_history[].gaps` lists concise missing or mistaken concepts; use `[]` for a correct answer.
- Copy `question` and `citations` from `pending_assessment` into the new history entry, add the assessment result fields, then set `pending_assessment` to `null`.
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
