---
name: answer-generator
description: Internal creation stage used by notes-generator. Write source-grounded answers to learning questions when delegated or explicitly invoked.
---

# Answer Generator

Given a question and source, produce a clear, self-contained answer grounded primarily in the source and written in original wording.

## Workflow

1. **Analyze:** Determine what a complete answer must address and its supporting source material.
2. **Synthesize:** Organize that material into a coherent explanation using the structure below.
3. **Enhance:** When the source defines a term or concept vaguely and web access is available, clarify it using authoritative online sources. Cite and label findings as supplemental; never silently replace or contradict the source, and identify unresolved conflicts. Without web access, state the limitation rather than inventing clarification.

## Answer Structure

Use compact Markdown in this order:

### 1. Key terminology (required)
- From the source, define only the key terms needed to answer the question and explain its learning objective.
- Introduce each necessary technical term here before its first use in the general principle.
- Use them consistently thereafter.

### 2. General principle (required)

- Lead with the direct answer, then provide the reasoning and context needed for completeness.
- Preserve assumptions, qualifiers, and trade-offs.
- Include relevant equations for mathematical or quantitative relationships, defining symbols and applicable assumptions.

### 3. Source-specific example (required)

- In one sentence, give a source-specific example illustrating the principle and cite its exact section, subsection, page, or other available locator.

## Style and Accuracy

- Ensure factual alignment with the source material.
- Keep supplemental external clarification distinguishable from source-supported claims and cite it.
