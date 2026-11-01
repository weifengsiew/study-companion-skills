---
name: notes-generator
description: Create per-subsection learning notes by orchestrating question, answer, aid, review, synthesis, and formatting skills.
---

# Notes Generator

## Load learning preferences

Using the host's invocation syntax, invoke `learning-preference-manager` and load confirmed `shared` and `notes` preferences before generating or revising notes. Continue if unavailable. Apply the manager's precedence and pass relevant preferences to affected creation and review stages.

## Notes path

Determine the matching notes path before processing the source:

- Use the learner-supplied notes path when provided.
- Otherwise, use `source_dir/notes/<source-stem>-notes.md`, where `source_dir` contains the source and `<source-stem>` is the source filename without its final extension.
- Create the `notes/` directory when needed.
- If the target file already exists, do not replace it without the learner's explicit confirmation.

Save the completed notes there. Report the exact source and notes paths and explain that `teach-me` uses them to start or resume a study session. If saving fails, say so rather than implying the file exists.

For every invoked skill, prefer the bundled copy when present and require no installation path.

## From source to notes

Before dividing the source, map its central purpose or question, major parts, and important relationships. Use this map throughout generation. Divide the source into two or three contiguous parts at natural section or subsection boundaries; never split a subsection. Assign each part one primary subagent to process its subsections in source order. Keep subsections as distinct outputs and batch when capacity is limited.

For each subsection, identify distinct learning objectives and run these stages in order. One primary subagent runs creation stages 1, 2, and 4; separate reviewer subagents run stages 3, 5, and 6. The primary applies valid findings after each review.

1. `question-generator`
2. `answer-generator`
3. `scope-reviewer`
4. `learning-aid-creator`
5. `alignment-reviewer`
6. `transferability-reviewer`

Minimize repeated context. Give each stage only the current subsection, its objectives, the relevant source-map slice, and the drafts or findings it needs. Give reviewers only the relevant objective, source-map context, source excerpt, and current draft; tag findings by objective and report failed stages as incomplete. Include supplemental material only when the draft relies on it.

## Finalize

1. Invoke `duplication-reviewer` with the source map, learning objectives, and completed detailed notes; apply valid recommendations.
2. Invoke `big-picture-generator` with the source map and completed notes, then invoke `practical-takeaway-generator` with the source map, completed notes, and heading-anchor index.
3. Invoke `notes-formatter` with their outputs, the detailed note units, source order, and heading-anchor index.
4. Return formatting blockers to the responsible generation stage, rerun the formatter, then save and report the complete notes path.
