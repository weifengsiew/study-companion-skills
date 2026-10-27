---
name: learning-aid-creator
description: Create a source-grounded learning aid that supplements an explanatory question-and-answer note.
---

# Learning Aid Creator

Read the question and answer. Identify the concept structure and generate one suitable new aid per question. If the source material contains essential suitable aids, include them in addition to the generated aid and identify them as source-provided.

| Aid | Use when |
|---|---|
| Comparison table | Concepts, settings, or methods differ |
| Decision tree | A choice depends on conditions |
| Workflow/process diagram | Steps or branching processes matter |
| Worked numerical example | A formula or calculation needs demonstration |
| Worked code example | An abstract idea appears in implementation |
| Concept/dependency map | Relationships or prerequisites matter |
| Example–counterexample | Boundaries or misconceptions need clarification |
| Annotated plot/visual | Trends, distributions, or visual patterns matter |

Use Markdown tables for comparisons, Mermaid for diagrams, and fenced Python for code examples. Treat the supplied source as primary. Authoritative external sources may provide supplemental support, but cite and label them as supplemental, and do not silently replace or contradict the supplied source. Avoid decorative visuals and repetition.

Return:

```markdown
### Learning aid(s): <type>

<artifact>

Why it helps: <one concise explanation>
```

Check that the aids are accurate, useful, and consistent with the answer.
