---
name: notes-formatter
description: Internal finalization stage used by notes-generator. Assemble and validate the canonical notes layout when delegated or explicitly invoked.
---

# Notes Formatter

Format the supplied `Big picture`, `Practical takeaway`, and detailed note units into one Markdown document. Do not generate, summarize, review, deduplicate, fact-check, or otherwise revise instructional content.

## Required structure

```markdown
# Big picture

<big-picture content>

# Practical takeaway

<practical-takeaway content>

## <Source heading>

### Question

<question>

#### Key terminology

<definitions>

#### General principle

<explanation>

<learning aid>

#### Source-specific example

<example>
```

Place source headings and note units in source order. When a source section has multiple objectives, repeat the objective-level structure under the same source heading.

Every objective must contain `Question`, `Key terminology`, `General principle`, a learning aid, and `Source-specific example`. Place the learning aid directly after the general principle without adding a learning-aid heading.

## Formatting rules

- Preserve content wording, citations, tables, code fences, equations, Mermaid diagrams, and learning aids.
- Preserve source headings and use consistent heading levels.
- Keep `Big picture` free of internal links.
- Verify that internal links in `Practical takeaway` resolve to the intended detailed source headings.
- Normalize spacing and blank lines.
- Do not add, remove, rewrite, merge, or deduplicate instructional content.

If required content is missing or cannot be placed unambiguously, report the formatting blockers instead of inventing content. Otherwise, return only the complete formatted Markdown document.
