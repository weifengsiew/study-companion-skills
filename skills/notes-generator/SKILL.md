---
name: notes-generator
description: Create per-subsection learning notes by orchestrating question, answer, aid, scope, alignment, and transferability reviews.
---

# Notes Generator

## Model confirmation

Before starting, ask the user to confirm they are using an advanced model with the strongest available reasoning or effort setting. Wait for confirmation unless they already gave it for this request.

## Notes path

Determine the matching notes path before processing the source:

- Use the notes path supplied by the learner when one is provided.
- Otherwise, use `source_dir/notes/<source-stem>-notes.md`, where `source_dir` contains the source and `<source-stem>` is the source filename without its final extension.
- Create the `notes/` directory when needed.
- If the target file already exists, do not replace it without the learner's explicit confirmation.

Save the completed notes to that path. When finished, tell the learner the exact source and notes paths and explain that `teach-me` will use those same paths to start or resume an interactive study session. If the notes cannot be saved, state that clearly instead of implying that the file exists.

## From source to notes

Process the source one section at a time, preserving its hierarchy and order. Within each section, process its subsections in source order. Assign one primary subagent to each subsection and give it only that subsection's source material. That subagent identifies the subsection's learning objectives and creates one question, one answer, and one generated learning aid, plus any essential source-provided aids, for each objective. Use separate subagents for the required reviews. Process subsections and reviews in batches when capacity is limited. For each objective, invoke the following available skills by name in this order. Prefer copies bundled with the current package when present; do not require a particular installation path:

1. `question-generator` — the primary subagent creates one focused question.
2. `answer-generator` — the same primary subagent creates the answer.
3. `scope-reviewer` — a separate reviewer subagent returns an initial scope review.
4. `final-boss` — apply its two-message sequence to the scope-reviewer subagent, then have the primary incorporate valid findings from the reviewer's final revision.
5. `learning-aid-creator` — the primary subagent creates the learning aid(s).
6. `alignment-reviewer` — a separate reviewer subagent returns an initial alignment review.
7. `final-boss` — apply its two-message sequence to the alignment-reviewer subagent, then have the primary incorporate valid findings from the reviewer's final revision.
8. `transferability-reviewer` — a separate reviewer subagent returns an initial transferability review.
9. `final-boss` — apply its two-message sequence to the transferability-reviewer subagent, then have the primary incorporate valid findings from the reviewer's final revision before returning the completed note.

## Reviewers

Give each reviewer the current draft and assigned source material. Treat its result as provisional until the following `final-boss` step is complete, then incorporate valid final findings before continuing. Report failed or timed-out reviewer stages as incomplete, and batch work within available capacity.

## Final pass

After completing all subsections in a section, compare its source and notes for missing concepts or cross-subsection relationships. For each gap, define a focused learning objective and run it through the full nine-step workflow.

Output notes in source order: heading (same as the source material), `Question`, answer, and learning aid(s).
