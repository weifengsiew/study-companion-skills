---
name: teach-loop
description: Internal teaching loop used by teach-me. Run adaptive, source-grounded instruction when delegated or explicitly invoked.
---

# Teach Loop

Use the current concept group's notes as the primary basis for teaching, with compact session state. Consult targeted source excerpts for corroboration or examples; retrieve other sections only when advancing or a question spans topics. Flag note/source conflicts, say when notes do not answer a question, and distinguish supported claims from inference or illustration.

A concept group is the smallest independently masterable set needed for one learning objective and focused question cycle. Split independently masterable concepts. A group is complete only when the learner demonstrates its objective.

Choose the smallest effective question. Before a conceptual-understanding question, read [`../study-session-manager/references/conceptual-understanding.md`](../study-session-manager/references/conceptual-understanding.md); before a technical-fluency question, read [`../study-session-manager/references/technical-fluency.md`](../study-session-manager/references/technical-fluency.md). Follow the learner's selected emphasis and response format; prefer short answer and use multiple choice sparingly. Emphasis does not override required coverage.

Use persisted objectives to resume `current_objective_id`, select the next focus, and assess relevant concepts. Return an objective update to `study-session-manager`; do not save progress directly.

## Teach loop

1. **Plan:** Select one coherent concept group small enough to explain or apply briefly. Split broader topics unless the notes treat them as inseparable.
2. **Explain:** Teach the notes' central concepts first, define unfamiliar terms on first use, and include only necessary definitions and examples. Prioritize transferable understanding over source-specific detail.
3. **Test:** Identify the concepts being tested and eliminate answer cues from the question and immediately preceding explanation. Ask a small number of focused questions about previously taught concepts, preferably using novel scenarios that do not depend on incidental source details.
4. **Assess:** Compare the response with the notes and corroborate it with the source. Acknowledge correct understanding, identify gaps or misconceptions, and avoid unsupported grading.
5. **Adapt:** If understanding is incomplete, re-explain or simplify without removing essential terminology, change question format, or ask a targeted follow-up. Resolve important gaps before advancing.
6. **Advance or pause:** Briefly conclude mastered groups. For each newly mastered group, return its objective, note heading or anchor, and final confirmed explanation. Wait for the learner's response or clarification before advancing.

## Coverage and state

Given session state, resume `current_objective_id` and the last question on that objective. After each response or clarification, return an objective update:

```json
{
  "objective_id": "objective-02",
  "status": "in_progress",
  "question": {
    "prompt": "The question asked",
    "outcome": "incomplete",
    "gaps": ["Specific unresolved gap"]
  }
}
```

Teaching does not use attempt counters or success proportions. Return the update to `study-session-manager`; preserve its note-review queue behavior.
