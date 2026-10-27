---
name: answer-generator
description: Write source-grounded answers to learning questions.
---

# Answer Generator

Given a question and source, produce a clear, self-contained answer. Treat the source as primary and synthesize it in original wording.

## Workflow

1. **Analyze:** Determine what a complete answer must address and identify the source material that supports it.
2. **Synthesize:** Organize the provided source material into a coherent explanation using the structure below.
3. **Enhance:** For terms or concepts the source defines vaguely, research authoritative online sources when web access is available and use relevant findings to clarify the answer. Cite and explicitly label this material as supplemental. Do not silently replace or contradict the supplied source; identify any unresolved conflict. If web access is unavailable, identify the limitation instead of inventing a clarification.

## Answer Structure

Use compact Markdown in this order:

### 1. Key terminology (required)
- Define the key terms needed to answer the current question and explain its learning objective, using the source material.
- Use these key terms consistently throughout the rest of the answer.

### 2. General principle (required)

- Lead with the direct answer to the question, then provide the relevant reasoning and context needed to answer fully.
- Preserve assumptions, qualifiers, and trade-offs.
- Include relevant equations for mathematical or quantitative relationships, defining symbols and applicable assumptions.

### 3. Source-specific example (when useful)

- Provide an example from the supplied source that clearly illustrates the general principle.
- Keep this section under 1.2 times the length of the general principle; omit it if it adds no understanding.

## Style and Accuracy

- Treat the source as primary and synthesize it in original wording.
- Ensure factual alignment with the source material.
- Keep supplemental external clarification distinguishable from source-supported claims and cite it.
