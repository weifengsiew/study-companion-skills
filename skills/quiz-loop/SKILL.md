---
name: quiz-loop
description: Internal assessment loop used by quiz-me. Run question-first assessment when delegated or explicitly invoked.
---

# Quiz Loop

Use loaded notes as the primary basis for assessment, explanation, and sequence, corroborating them with targeted source excerpts. If the notes are silent or conflict with the source, say so and do not present disputed content as fact. Distinguish supported claims from inference or illustration, citing relevant locations when useful.

## Quiz loop

1. **Plan:** Select one untested concept or coherent group small enough for a focused question. Split broader topics unless the notes treat them as inseparable.
2. **Question:** Ask a focused question. Identify the concepts being tested and eliminate answer cues from the question and surrounding context.
3. **Assess:**

   - Compare the response with the notes and corroborate it with the source. Evaluate both correctness and completeness of the response.
   - Persist immediately when clearly correct and complete, clearly incorrect, or when the learner says they do not know or requests teaching.
   - If the answer is correct and complete, briefly confirm it without explaining and advance.
4. **Clarify:**

   - For incomplete or ambiguous answers, use up to six neutral, non-leading prompts without teaching or revealing missing content.
   - Persist each unresolved response and prompt in the pending assessment, not assessment history. Replacing the question at the learner's request does not increment `clarification_count`.
5. **Resolve:**

   - If the learner independently demonstrates the tested concepts correctly and completely at any point, persist one correct assessment with no gap.
   - After the sixth prompt, or when the learner requests help or clearly cannot answer, persist one `partially_correct` or `incorrect` assessment with specific gaps.
6. **Teach:**

   - If it is partially correct or incomplete, explain only the missing or mistaken parts.
   - If it is incorrect or the learner does not know, explain the tested material without requiring another guess first.
   - Teach the relevant concepts using essential terminology, defining unfamiliar terms on first use. Prioritize transferable understanding over source-specific examples and include only necessary examples.
7. **Reassess:**

   - After the learner confirms the explanation is clear, ask a different question that tests the same concepts without answer cues.
   - Demonstrated understanding, rather than recall of the explanation, is required before marking them mastered. The earlier gap remains recorded.
8. **Advance or pause:**

   - Mark groups as mastered only after they are demonstrated correctly and completely, then move to the next untested group.
   - If understanding remains incomplete, explain or adapt again and reassess.
   - Allow the learner to skip or pause, and always wait for their response before advancing.

## Appeals

If the learner contests the latest assessment before the pass is extracted, pause teaching and recheck their rationale against the source and notes. When it shows the original answer was valid or the question ambiguous, use `revise-latest` to mark correct, clear active gaps, and preserve the rationale and correction reason. Knowledge demonstrated only after instruction is reassessment, not a grading correction.

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

Use `assessment_history` citations to select the earliest in-scope learning objective not yet demonstrated correctly, following source order. When given a gap manifest, use its gaps and citations as the scope; select the earliest unresolved target in the current pass and combine targets only when they form one coherent concept group. Ask a new question without exposing or copying an earlier question, answer, assessment, or gap wording. Complete only when every in-scope objective has a correct assessment and none is pending.
