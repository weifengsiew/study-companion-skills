---
name: notes-generator
description: Create per-subsection learning notes by orchestrating question, answer, aid, scope, alignment, and transferability reviews.
---

# Notes Generator

## Load learning preferences

Invoke the available `learning-preference-manager` skill using the host's skill-invocation syntax and load confirmed `shared` and `notes` preferences before generating or revising notes. Continue without them if the profile is unavailable. Apply the preference precedence defined by the manager, and pass relevant preferences to each creation or review stage they affect.

## Notes path

Determine the matching notes path before processing the source:

- Use the notes path supplied by the learner when one is provided.
- Otherwise, use `source_dir/notes/<source-stem>-notes.md`, where `source_dir` contains the source and `<source-stem>` is the source filename without its final extension.
- Create the `notes/` directory when needed.
- If the target file already exists, do not replace it without the learner's explicit confirmation.

Save the completed notes to that path. When finished, tell the learner the exact source and notes paths and explain that `teach-me` will use those same paths to start or resume an interactive study session. If the notes cannot be saved, state that clearly instead of implying that the file exists.

## From source to notes

Before dividing the source, identify its central purpose or question, major parts, and important relationships. Use this source map as shared context throughout note generation. Then divide the source into two to three contiguous parts along natural section or subsection boundaries, without splitting subsections. Assign one primary subagent to each part to process its subsections in source order. For each subsection, the primary identifies its distinct learning objectives, then runs the seven-step workflow below in the stated order, performing the creation steps while separate reviewer subagents perform the required reviews. Keep subsections as distinct output units and batch work when capacity is limited. Prefer copies of the named skills bundled with the current package when present; do not require a particular installation path:

1. `question-generator` — the primary subagent creates one focused question per objective.
2. `answer-generator` — the same primary subagent creates one answer per objective.
3. `scope-reviewer` — a separate reviewer subagent reviews all objectives in the subsection; the primary incorporates valid findings before creating the learning aids.
4. `learning-aid-creator` — the primary subagent creates learning aid(s) per objective and places each aid directly after the answer's general principle and before any source-specific example, without a separate learning-aid subsection.
5. `alignment-reviewer` — a separate reviewer subagent reviews all objectives and current drafts in the subsection; the primary incorporates valid findings before continuing.
6. `transferability-reviewer` — a separate reviewer subagent reviews all objectives and current drafts in the subsection; the primary incorporates valid findings before final review.
7. Independent final review — a fresh reviewer subagent validates the completed subsection against the source and all specialist findings. The primary incorporates valid final corrections before returning the subsection.

## Reviewers

Give each specialist reviewer only its assigned review instructions, the subsection's learning objectives, relevant source-map context, source, and current drafts. Include cited supplemental material only when a draft relies on it. Review each objective separately and tag findings by objective.

After the specialist reviews, give a fresh final reviewer the subsection's learning objectives, source, completed drafts, and findings from all specialist reviewers. The final reviewer checks whether valid findings were addressed, resolves conflicting recommendations, and identifies remaining gaps or errors. It must not repeat resolved findings or introduce changes outside the learning objectives.

The primary subagent incorporates valid final corrections before returning the completed subsection. Report failed or timed-out stages as incomplete and batch large subsections as needed.

## Final pass

After completing all subsections, compare the source map, source, and notes for missing concepts or relationships within and across sections. For each gap, define a focused learning objective and run it through the full seven-step workflow.

Then perform a concision pass. Remove duplication across questions and between answers and aids. Use the shortest complete explanation while preserving key terminology, accuracy, reasoning, and essential qualifications.

Begin the notes with a concise `Big picture` section explaining the source's central purpose, what its major parts cover, how they relate, and how the topic fits into the broader subject.

After the `Big picture`, include a concise, source-wide `Practical takeaway`. Drawing on the source as a whole and without repeating details covered later in the notes, synthesize when and why its concepts are useful in practice, the decisions they inform, and the actions they enable. Use a high-level workflow, decision matrix, checklist, or a combination of these formats, selecting only what best communicates the practical overview.

Then output the remaining notes in source order: heading (same as the source material), `Question`, and answer, with each learning aid embedded directly after its general principle.
