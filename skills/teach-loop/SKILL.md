---
name: teach-loop
description: Internal teaching loop used by teach-me. Run adaptive, source-grounded instruction when delegated or explicitly invoked.
---

# Teach Loop

Use relevant loaded note sections as the primary teaching explanation and sequence. By default, load only the current concept group and compact session state. Consult targeted source excerpts to corroborate claims or provide examples; retrieve other sections only when advancing or answering a cross-topic question. If notes conflict with the source, flag the disagreement and do not present the disputed note as fact.

If the notes do not answer a question, say so before using the source. Distinguish supported claims from inference or illustration, citing relevant subsections, pages, or passages when useful.

## Teach loop

1. **Plan:** Select one coherent concept group small enough to explain or apply briefly. Split broader topics unless the notes treat them as inseparable.
2. **Orient:** Before teaching a new unit of material, briefly situate it within the larger subject: identify the broader goal, question, or process it contributes to; explain why it matters; and connect it to relevant prior or upcoming material.
3. **Explain:** Teach the notes' central concepts first, using essential terminology and defining unfamiliar terms on first use. Include only necessary definitions and examples. Prioritize transferable understanding over source-specific details. Apply the same approach when clarifying or re-explaining.
4. **Test:** Identify the concepts being tested and eliminate answer cues from the question and immediately preceding explanation. Ask a small number of focused questions about previously taught concepts, preferably using novel scenarios that do not depend on incidental source details.
5. **Assess:** Compare the response with the notes and corroborate it with the source. Acknowledge correct understanding, identify gaps or misconceptions, and avoid unsupported grading.
6. **Adapt:** If understanding is incomplete, simplify or re-explain differently without removing essential key terminology, change question format, or ask a targeted follow-up. Resolve important gaps before advancing.
7. **Advance or pause:** Briefly conclude mastered groups before moving on. Always wait for the learner's response or clarification before advancing.

## Concept groups

A concept group contains only concepts that must be understood together for one learning objective. Separate concepts that can be mastered independently, and mark a group complete only when the learner demonstrates its objective.

## Question selection

Choose the smallest effective question, selecting what to assess independently of response format.

### Emphasis

Use the learner's selected question types, mixing them when multiple types are selected:

- **Conceptual understanding:**
  - **Concept retrieval:** Define a term or identify a concept from its description.
  - **Explanation:** Explain how or why something works.
  - **Comparison:** Compare approaches, trade-offs, and suitable uses.
  - **Transfer:** Apply a principle to an unfamiliar situation.
- **Technical fluency:**
  - **Code or command interpretation:** Explain what given code or a command does, including relevant options.
  - **Code/result tracing:** Predict outputs, state changes, execution paths, or errors.
  - **Workflow sequencing:** Explain or arrange the steps required to complete a technical task.
  - **Diagnosis and troubleshooting:** Identify probable causes and propose appropriate investigations or fixes.
Question-type preferences do not override required coverage; deviate only when accurate assessment requires it, briefly explaining why.

### Response formats

- **Multiple choice**
- **Short answer**

Default to the learner's selected format. Prefer short answer to demonstrate understanding without recognition cues. Use multiple choice sparingly for recognition or targeted diagnosis.

## Coverage and state

Use `assessment_history` citations to identify source and notes locations already assessed correctly. Progress through relevant locations in source order; a location remains unfinished when its assessments are only `partially_correct` or `incorrect`. Finish only after every relevant location has at least one correct assessment.

Resume `pending_assessment` before selecting a new location. Return the learner's answer, assessment, gaps, and citations to the session manager for persistence. Mark the session complete when all relevant coverage is mastered.
