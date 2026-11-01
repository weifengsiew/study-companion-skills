---
name: quiz-loop
description: Assess interactively from source-grounded notes before explaining, targeting instruction to gaps in the learner's understanding.
---

# Quiz Loop

Use relevant loaded note sections as the primary basis for assessment, explanation, and sequence. By default, load only the current concept group and compact session state. Consult targeted source excerpts to corroborate claims or provide examples; retrieve other sections only when advancing or a question spans topics. If notes conflict with the source, flag the disagreement and do not present the disputed note as fact.

If the notes do not answer a question, say so before using the source. Distinguish supported claims from inference or illustration, citing relevant subsections, pages, or passages when useful.

## Quiz loop

1. **Plan:** Select one untested concept or coherent group small enough for a focused question. Split broader topics unless the notes treat them as inseparable.
2. **Question:** Ask a focused question before explaining the material. Identify the concepts being tested and eliminate answer cues from the question and surrounding context.
3. **Assess:** Compare the response with the notes and corroborate it with the source. Acknowledge correct understanding, identify gaps or misconceptions, and avoid unsupported grading.
4. **Branch:** If the answer is correct, briefly confirm it without explaining and advance. If it is partially correct, explain only the missing or mistaken parts. If it is incorrect or the learner does not know, explain the tested material without requiring another guess first.
5. **Explain:** When needed, briefly situate the material within the larger subject, then teach the relevant concepts using essential terminology, defining unfamiliar terms on first use. Prioritize transferable understanding over source-specific details and include only necessary definitions and examples.
6. **Reassess:** After the learner confirms the explanation is clear, ask a different question that tests the same concepts without answer cues. Demonstrated understanding, rather than recall of the explanation, is required before marking them mastered.
7. **Advance or pause:** Mark demonstrated concepts as mastered and move to the next untested concept group. If understanding remains incomplete, explain or adapt again and reassess. Allow the learner to skip or pause, and always wait for their response before advancing.

## Question selection

Choose the smallest effective question, selecting what to assess independently of response format.

Before selecting a conceptual-understanding question, read [`../shared/conceptual-understanding.md`](../shared/conceptual-understanding.md); before a technical-fluency question, read [`../shared/technical-fluency.md`](../shared/technical-fluency.md). Follow the learner's selected emphasis: load only the relevant reference, or each when first needed for a balanced mix. Emphasis does not override required coverage; deviate only when accurate assessment requires it, briefly explaining why.

### Response formats

- **Multiple choice**
- **Short answer**

Default to the learner's selected format. Prefer short answer to demonstrate understanding without recognition cues. Use multiple choice sparingly for recognition or targeted diagnosis.

## Coverage and state

Track required, tested, and remaining concepts before each question. Collectively assess all relevant concepts through explanation, comparison, or application.

Given session state, resume its current chunk, pending question, and remaining concepts. Return enough state to record the learner's answer and assessment.
