---
name: teach-loop
description: Internal teaching loop used by teach-me. Run adaptive, source-grounded instruction when delegated or explicitly invoked.
---

# Teach Loop

Use the current concept group's notes as the primary explanation and sequence, with compact session state. Consult targeted source excerpts for corroboration or examples, and retrieve other sections only when advancing or answering a cross-topic question. Flag note/source conflicts and do not present disputed notes as fact. If the notes do not answer a question, say so before using the source; distinguish supported claims from inference or illustration and cite relevant locations when useful.

## Concept groups

A concept group is the smallest set of concepts needed for one learning objective and one focused explanation-and-question cycle. Separate independently masterable concepts. A group is complete only when the learner demonstrates its objective; skipped or incomplete groups do not count.

## Teach loop

1. **Plan:** Select one coherent concept group small enough to explain or apply briefly. Split broader topics unless the notes treat them as inseparable.
2. **Orient:** Before teaching a new unit of material, briefly situate it within the larger subject: identify the broader goal, question, or process it contributes to; explain why it matters; and connect it to relevant prior or upcoming material.
3. **Explain:** Teach the notes' central concepts first, define unfamiliar terms on first use, and include only necessary definitions and examples. Prioritize transferable understanding over source-specific detail.
4. **Test:** Identify the concepts being tested and eliminate answer cues from the question and immediately preceding explanation. Ask a small number of focused questions about previously taught concepts, preferably using novel scenarios that do not depend on incidental source details.
5. **Assess:** Compare the response with the notes and corroborate it with the source. Acknowledge correct understanding, identify gaps or misconceptions, and avoid unsupported grading.
6. **Adapt:** If understanding is incomplete, re-explain or simplify without removing essential terminology, change question format, or ask a targeted follow-up. Resolve important gaps before advancing.
7. **Advance or pause:** Briefly conclude mastered groups before moving on. For each newly mastered group, return its learning objective, corresponding note heading or anchor, any final confirmed explanation, and whether that explanation materially differed from the notes. Always wait for the learner's response or clarification before advancing.

## Question selection

Choose the smallest effective question, selecting what to assess independently of response format.

Before a conceptual-understanding question, read [`../study-session-manager/references/conceptual-understanding.md`](../study-session-manager/references/conceptual-understanding.md); before a technical-fluency question, read [`../study-session-manager/references/technical-fluency.md`](../study-session-manager/references/technical-fluency.md). Follow the learner's selected emphasis, loading only the relevant reference or each as first needed for a balanced mix. Emphasis does not override required coverage; deviate only when accurate assessment requires it and briefly explain why.

### Response formats

- **Multiple choice**
- **Short answer**

Use the learner's selected format. Prefer short answer; use multiple choice sparingly for recognition or targeted diagnosis.

## Coverage and state

Use persisted objectives to select the next focus. Assess relevant concepts through explanation, comparison, or application.

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

The session manager appends the question to the objective and updates its status. Teaching does not use attempt counters or success proportions. Preserve the note-review queue behavior defined by `study-session-manager`.
