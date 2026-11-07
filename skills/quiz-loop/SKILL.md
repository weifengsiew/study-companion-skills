---
name: quiz-loop
description: Internal assessment loop used by quiz-me. Run question-first assessment when delegated or explicitly invoked.
---

# Quiz Loop

Use the current concept group's notes as the primary basis for assessment, explanation, and sequence, with compact session state. Consult targeted source excerpts for corroboration or examples, and retrieve other sections only when advancing or a question spans topics. Flag note/source conflicts and do not present disputed notes as fact. If the notes do not answer a question, say so before using the source; distinguish supported claims from inference or illustration and cite relevant locations when useful.

## Concept groups

A concept group is the smallest set of concepts needed for one learning objective and one focused explanation-and-question cycle. Separate independently masterable concepts. A group is complete only when the learner demonstrates its objective; skipped or incomplete groups do not count.

## Quiz loop

1. **Plan:** Select one untested concept or coherent group small enough for a focused question. Split broader topics unless the notes treat them as inseparable.
2. **Question:** Ask a focused question before explaining the material. Identify the concepts being tested and eliminate answer cues from the question and surrounding context.
3. **Assess:** Compare the response with the notes and corroborate it with the source. Acknowledge correct understanding, identify gaps or misconceptions, and avoid unsupported grading.
4. **Branch:** If the answer is correct, briefly confirm it without explaining and advance. If it is partially correct, explain only the missing or mistaken parts. If it is incorrect or the learner does not know, explain the tested material without requiring another guess first.
5. **Explain:** When needed, briefly situate the material, then teach the relevant concepts with essential terminology, defining unfamiliar terms on first use. Prioritize transferable understanding and include only necessary definitions and examples.
6. **Reassess:** After the learner confirms the explanation is clear, ask a different question that tests the same concepts without answer cues. Demonstrated understanding, rather than recall of the explanation, is required before marking them mastered.
7. **Advance or pause:** Mark demonstrated groups as mastered and move to the next untested group. If understanding remains incomplete, explain or adapt again and reassess. Allow the learner to skip or pause, and always wait for their response before advancing.

## Question selection

Choose the smallest effective question, selecting what to assess independently of response format.

Before a conceptual-understanding question, read [`../study-session-manager/references/conceptual-understanding.md`](../study-session-manager/references/conceptual-understanding.md); before a technical-fluency question, read [`../study-session-manager/references/technical-fluency.md`](../study-session-manager/references/technical-fluency.md). Follow the learner's selected emphasis, loading only the relevant reference or each as first needed for a balanced mix. Emphasis does not override required coverage; deviate only when accurate assessment requires it and briefly explain why.

### Response formats

- **Multiple choice**
- **Short answer**

Use the learner's selected format. Prefer short answer; use multiple choice sparingly for recognition or targeted diagnosis.

## Coverage and state

Use the ordered persisted `chunks` collection to track coverage and select each question. Assess all relevant concepts through explanation, comparison, or application.

Given session state, resume `current_chunk_id`, its pending question, and remaining chunks. After each learner response or clarification, return a chunk update in this shape:

```json
{
  "chunk_id": "chunk-03",
  "status": "in_progress",
  "pending_question": null,
  "latest_attempt": {
    "question": "The question asked",
    "response": "The learner's response",
    "assessment": "unsuccessful",
    "gaps": ["Specific unresolved misconception"],
    "feedback": "Brief assessment feedback",
    "timestamp": "2026-11-07T10:25:00Z"
  }
}
```

The session manager applies the update, updates counters and `successful_attempt_proportion`, replaces `latest_attempt`, updates `unsuccessful_attempt_gaps`, and advances `current_chunk_id` only when the chunk is complete. Do not alter the note-review queue.
