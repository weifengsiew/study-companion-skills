---
name: practical-takeaway-generator
description: Create a concise, source-wide practical takeaway using a dependency-driven Mermaid workflow and interpretive caption.
---

# Practical Takeaway Generator

Use the source map, completed detailed notes, and heading-anchor index to create the content for the opening `Practical takeaway` section. Consult targeted source excerpts only when these inputs cannot support or verify a point.

Synthesize when and why the source's concepts are useful, the decisions they inform, and the actions they enable. Do not repeat the `Big picture` orientation or granular explanations from the detailed notes.

## Workflow

Create one Mermaid flowchart showing a coherent, source-supported practical workflow. Organize the main path around meaningful dependencies and handoffs: each step should use a result, decision, or condition established earlier and produce something needed later.

Include optional work and failure handling only when supported by the source. Show optional paths as conditional branches that rejoin when appropriate, and show failure paths leading to retry, correction, escalation, or stopping.

Do not force every source theme into the workflow. Include only concepts that contribute to the practical flow, and do not invent dependencies or guidance.

## Caption

After the workflow, add one concise caption explaining when to use it, what moves between its stages, and how to interpret its branches. Do not merely repeat node labels or narrate every step.

Use descriptive internal links where the detailed notes help the learner understand or perform a stage. Ensure each link matches the heading-anchor index.

Return only the `Practical takeaway` content, without its heading.
