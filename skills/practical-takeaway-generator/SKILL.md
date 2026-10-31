---
name: practical-takeaway-generator
description: Create a concise, source-wide practical takeaway from completed learning notes using a dependency-driven Mermaid flow and an interpretive caption.
---

# Practical Takeaway Generator

Use the source map, completed detailed notes, and heading-anchor index to create the opening `Practical takeaway` section. Consult only targeted source excerpts when these inputs cannot support or verify a point.

Synthesize when and why the source's concepts are useful in practice, the decisions they inform, and the actions they enable. Draw on the source as a whole without repeating granular explanations from the detailed notes.

## Workflow diagram

Use a Mermaid diagram to synthesize an overall workflow from related smaller workflows in the source when their relationships support it. Make the information flow explicit: every main-path step must consume a result produced earlier and produce an output needed by the next step. Label nodes or edges concisely enough to make those handoffs understandable.

Show optional work only as a conditional branch that rejoins the main flow when appropriate. Show validation failures, missing inputs, or other source-supported failure handling as decision branches leading to retry, correction, escalation, or stopping; do not present them as unconditional main-path steps. Group related steps into stages, preserve source-supported relationships, and verify that the diagram renders clearly.

## Caption

After the diagram, write one concise caption that explains how to follow the main flow, what is passed between stages, and what each conditional branch means. Clarify when optional and failure paths are taken and where they return or terminate. Do not merely repeat the node labels or narrate every step.

Do not introduce guidance unsupported by the source.

Use valid internal Markdown links in the caption where detailed notes help the learner act on or understand a stage. Use descriptive link text and exact heading anchors.

Return only the complete `Practical takeaway` section.
