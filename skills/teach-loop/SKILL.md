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
7. **Advance or pause:** Briefly conclude mastered chunks before moving on. Always wait for the learner's response or clarification before advancing.

## Question selection

Choose the smallest effective question, selecting what to assess independently of response format.

Before selecting a conceptual-understanding question, read [`../study-session-manager/references/conceptual-understanding.md`](../study-session-manager/references/conceptual-understanding.md); before a technical-fluency question, read [`../study-session-manager/references/technical-fluency.md`](../study-session-manager/references/technical-fluency.md). Follow the learner's selected emphasis: load only the relevant reference, or each when first needed for a balanced mix. Emphasis does not override required coverage; deviate only when accurate assessment requires it, briefly explaining why.

### Response formats

- **Multiple choice**
- **Short answer**

Default to the learner's selected format. Prefer short answer to demonstrate understanding without recognition cues. Use multiple choice sparingly for recognition or targeted diagnosis.

## Coverage and state

Track required, tested, and remaining concepts before testing each chunk. Collectively assess all relevant concepts through explanation, comparison, or application.

Given session state, resume its current chunk, pending question, and remaining concepts. Return enough state to record the learner's answer and assessment.
