---
name: notes-generator
description: Create per-subsection learning notes by orchestrating question, answer, aid, scope, alignment, and transferability reviews.
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

## From source to notes

Before dividing the source, map its central purpose or question, major parts, and important relationships. Use this map throughout generation. Divide the source into two or three contiguous parts at natural section or subsection boundaries; never split a subsection. Assign each part one primary subagent to process its subsections in source order. For each subsection, the primary identifies distinct learning objectives and runs the ordered seven-step workflow, performing creation while separate subagents perform reviews. Keep subsections as distinct outputs and batch when capacity is limited. Prefer bundled copies of named skills when present; require no installation path:

Minimize repeated context. Give each stage only the current subsection, its objectives, the relevant source-map slice, and the drafts or findings that stage needs. Do not pass unrelated source sections or completed notes. Include supplemental material only when the current draft relies on it.

1. `question-generator` — the primary subagent creates one focused question per objective.
2. `answer-generator` — the same primary subagent creates one answer per objective.
3. `scope-reviewer` — a separate reviewer subagent reviews all objectives in the subsection; the primary incorporates valid findings before creating the learning aids.
4. `learning-aid-creator` — the primary subagent creates learning aid(s) per objective and places each aid directly after the answer's general principle and before any source-specific example, without a separate learning-aid subsection.
5. `alignment-reviewer` — a separate reviewer subagent reviews all objectives and current drafts in the subsection; the primary incorporates valid findings before continuing.
6. `transferability-reviewer` — a separate reviewer subagent reviews all objectives and current drafts in the subsection; the primary incorporates valid findings before final review.
7. Independent final review — a fresh reviewer subagent validates the completed subsection against the source and all specialist findings. The primary incorporates valid final corrections before returning the subsection.

## Reviewers

Give each specialist reviewer only its instructions, the subsection's objectives, relevant source-map context and source excerpt, and current drafts. Review each objective separately and tag findings by objective.

After specialist reviews, give a fresh final reviewer the objectives, relevant source excerpt, completed drafts, and all specialist findings. It checks that valid findings were addressed, resolves conflicts, and identifies remaining gaps or errors without repeating resolved findings or exceeding the objectives.

The primary incorporates valid final corrections before returning the subsection. Report failed or timed-out stages as incomplete; batch large subsections as needed.

## Completeness pass

After completing all subsections, compare the source map with a compact index of note headings, objectives, and relationships. Consult targeted source and note sections only for suspected gaps. For each confirmed gap, define a focused learning objective and run it through the full seven-step workflow.

## Deduplication pass

Perform a deduplication pass: remove duplication across questions and between answers and aids.

## Big picture and practical takeaways

After completing the detailed notes, invoke `big-picture-generator`, then `practical-takeaway-generator`, with the source map, completed notes, and a heading-anchor index. Provide targeted source excerpts only when the map and notes cannot support or verify a point. Prefer bundled copies when present; require no installation path.

## Output format

Place their returned sections at the beginning of the notes in this order: `Big picture`, then `Practical takeaway`. Verify that their internal Markdown links resolve to the intended detailed headings.

Then output the remaining notes in source order: heading (same as the source material), `Question`, and answer, with each learning aid embedded directly after its general principle.
