---
name: question-generator
description: Create one source-grounded learning question for a supplied learning objective.
---

# Question Generator

Given one learning objective and its relevant source material, create one focused learning question. Do not identify additional objectives or combine multiple objectives. Produce exactly one question per invocation.

## Method

1. Use the supplied learning objective to identify the key concepts or relationships the question must test.
2. Ask for retrieval plus explanation or reasoning, not just a definition.
3. Use an application, comparison, prediction, evaluation, or evidence-based situation when supported.
4. Focus on one meaningful relationship or outcome; include a trade-off or limitation when central.
5. Keep it clear, appropriately challenging, source-grounded, and answerable.

## Output

Return the question. A rationale may be used internally while drafting, but omit it from the output unless the user explicitly requests it. If the source is insufficient, state the limitation instead of inventing context.
