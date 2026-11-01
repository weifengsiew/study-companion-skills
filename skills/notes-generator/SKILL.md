---
name: notes-generator
description: Create per-subsection learning notes by orchestrating question, answer, aid, review, synthesis, and formatting skills.
---

# Notes Generator

## Load learning preferences

Before generating or revising notes, invoke `learning-preference-manager` using the host's syntax and load confirmed `shared` and `notes` preferences. Continue if unavailable. Apply its precedence and pass relevant preferences to affected creation and review stages.

## Notes path

Before processing the source, determine the notes path:

- Use the learner-supplied notes path when provided.
- Otherwise, use `source_dir/notes/<source-stem>-notes.md`; `source_dir` contains the source and `<source-stem>` omits its final extension.
- Create the `notes/` directory when needed.
- If the target file already exists, do not replace it without the learner's explicit confirmation.

Save the completed notes there. Report the exact source and notes paths, explaining that `teach-me` uses them to start or resume a study session. Report save failures rather than implying success.

For every invoked skill, prefer the bundled copy when present and require no installation path.

## From source to notes

Before dividing the source, map its central purpose or question, major parts, and important relationships; use this map throughout. Divide it into two or three contiguous parts at natural section or subsection boundaries without splitting subsections. Assign each part one primary subagent to process its subsections in source order. Keep subsection outputs distinct and batch when capacity is limited.

For each subsection, identify distinct learning objectives and run these stages in order. One primary subagent runs stages 1, 2, and 4; separate reviewer subagents run 3, 5, and 6. The primary applies valid findings after each review.

1. `question-generator`
2. `answer-generator`
3. `scope-reviewer`
4. `learning-aid-creator`
5. `alignment-reviewer`
6. `transferability-reviewer`

Minimize repeated context. Give each stage only the current subsection, objectives, relevant source-map slice, and needed drafts or findings. Give reviewers only the relevant objective, source-map context, source excerpt, and current draft. Tag findings by objective, report failed stages as incomplete, and include supplemental material only when the draft relies on it.

## Finalize

1. Invoke `duplication-reviewer` with the source map, learning objectives, and completed detailed notes; apply valid recommendations.
2. Invoke `big-picture-generator` with the source map and completed notes, then invoke `practical-takeaway-generator` with the source map, completed notes, and heading-anchor index.
3. Invoke `notes-formatter` with their outputs, the detailed note units, source order, and heading-anchor index.
4. Return formatting blockers to the responsible generation stage, rerun the formatter, then save and report the complete notes path.
