---
name: practical-takeaway-generator
description: Create a concise, source-wide practical takeaway from completed learning notes using a Mermaid workflow diagram and linked step captions.
---

# Practical Takeaway Generator

Use the source map, completed detailed notes, and heading-anchor index to create the opening `Practical takeaway` section. Consult only targeted source excerpts when these inputs cannot support or verify a point.

Synthesize when and why the source's concepts are useful in practice, the decisions they inform, and the actions they enable. Draw on the source as a whole without repeating granular explanations from the detailed notes.

## Workflow diagram

Use a Mermaid diagram to synthesize an overall workflow from related smaller workflows in the source when their relationships support it. Group related steps into stages, preserve source-supported relationships, keep nodes concise, and verify that the diagram renders clearly.

## Captions

State the workflow's practical purpose. For every step, explain what it does and why it matters in no more than two high-level sentences, omitting details and linking to the relevant detailed notes.

Do not introduce guidance unsupported by the source.

Link major points to the relevant detailed note sections using valid internal Markdown links. Use descriptive link text and exact heading anchors.

Return only the complete `Practical takeaway` section.
