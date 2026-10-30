---
name: notes-generator
description: Create per-subsection learning notes by orchestrating question, answer, aid, scope, alignment, and transferability reviews.
---

# Notes Generator

## Notes path

Determine the matching notes path before processing the source:

- Use the notes path supplied by the learner when one is provided.
- Otherwise, use `source_dir/notes/<source-stem>-notes.md`, where `source_dir` contains the source and `<source-stem>` is the source filename without its final extension.
- Create the `notes/` directory when needed.
- If the target file already exists, do not replace it without the learner's explicit confirmation.

Save the completed notes to that path. When finished, tell the learner the exact source and notes paths and explain that `teach-me` will use those same paths to start or resume an interactive study session. If the notes cannot be saved, state that clearly instead of implying that the file exists.

## From source to notes

Divide the source into three to five contiguous parts along natural section or subsection boundaries, without splitting subsections. Assign one primary subagent to each part to process its subsections in source order. For each subsection, run the nine-step workflow below in the stated order, with the primary performing the creation steps and separate reviewer subagents performing the required reviews. Keep subsections as distinct output units and batch work when capacity is limited. Afterward, review the assembled notes for gaps, duplication, consistency, and cross-part relationships. Prefer copies of the named skills bundled with the current package when present; do not require a particular installation path:

1. `question-generator` — the primary subagent creates one focused question per objective.
2. `answer-generator` — the same primary subagent creates one answer per objective.
3. `scope-reviewer` — a separate reviewer subagent reviews all objectives in the subsection.
4. `final-boss` — send its correction message to the scope-reviewer subagent, then have the primary incorporate valid findings from the reviewer's final revision.
5. `learning-aid-creator` — the primary subagent creates learning aid(s) per objective.
6. `alignment-reviewer` — a separate reviewer subagent reviews all objectives in the subsection.
7. `final-boss` — send its correction message to the alignment-reviewer subagent, then have the primary incorporate valid findings from the reviewer's final revision.
8. `transferability-reviewer` — a separate reviewer subagent reviews all objectives in the subsection.
9. `final-boss` — send its correction message to the transferability-reviewer subagent, then have the primary incorporate valid findings from the reviewer's final revision before returning the completed subsection.

## Reviewers

Give each reviewer only its assigned review instructions, the subsection's learning objectives, source, and current drafts. Include cited supplemental material only when a draft relies on it. Review each objective separately and tag findings by objective. Do not include other source sections, completed notes, prior review transcripts, or the full orchestration workflow.

Treat each review as provisional until its `final-boss` step is complete. Send the correction message to the existing reviewer subagent so its context does not need to be sent again. Report failed or timed-out stages as incomplete. Batch large subsections as needed.

## Final pass

After completing all subsections in a section, compare its source and notes for missing concepts or cross-subsection relationships. For each gap, define a focused learning objective and run it through the full nine-step workflow.

Then perform a concision pass. Remove duplication across questions and between answers and aids. Use the shortest complete explanation while preserving key terminology, accuracy, reasoning, and essential qualifications.

Output notes in source order: heading (same as the source material), `Question`, answer, and learning aid(s).
