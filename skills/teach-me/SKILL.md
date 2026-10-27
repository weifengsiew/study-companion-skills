---
name: teach-me
description: Set up and persist an interactive study session from notes and their sources.
---

# Teach Me

Use this skill when a learner wants a persistent interactive study session using notes tied to source material. 

## 1. Set up session

Find the exact source material at `source_dir/<source-name>` and its matching notes at `source_dir/notes/<notes-name>`, where `source_dir` is the source material's containing directory. Handle setup according to what is known and available:

- If either exact path is unknown, ask the learner to specify it.
- If the source path is known but the source is absent, ask the learner to place the source material there. Do not attempt note generation without the source.
- If the source exists but the notes are absent, invoke the available `notes-generator` skill using the host's skill-invocation syntax. Tell the learner that note generation will pause until they confirm they are using an advanced model with the strongest available reasoning or effort setting, as required by that skill. Return to setup after the notes file has been created, using the exact notes path reported by `notes-generator`.
- If both files exist, inform the learner of both exact paths and continue.

Never generate notes directly within `teach-me`.

## 2. Persist progress

Create `source_dir/notes/progress/<notes-stem>-progress.json` if it does not exist, where `<notes-stem>` is the notes filename without its final extension. If a progress file already exists during session setup, do not replace or reset it without asking; resume it by default. Routine state updates during an active session do not require repeated confirmation. Track exactly:

1. `source` — source path.
2. `notes` — matching notes path.
3. `current_chunk` — current subsection, status, and pending question.
4. `concept_coverage` — required, tested, and remaining concepts.
5. `assessment_history` — learner answers and assessment results.

Update the progress file after every learner response, clarification, or note change.

## 3. Use tutoring skill

Use `teaching-loop` skill for all live instruction, including explanations, clarifications, questions, assessment, adaptation, pacing, and instructional state. Use notes to teach concepts, source material to supply illustrative examples and progress json to track and update progress.

## 4. Manage note updates

After `teaching-loop` closes a lesson chunk or resolves a clarification, use an independent subagent to compare the final explanation with the corresponding notes subsection and relevant source material. Prefer it only if it is clearer than in the notes, while remaining accurate, complete, and within scope. If it is better, show the proposed edit location in the notes, original wording vs edited wording. Edit only if the user gives explicit confirmation. Otherwise, leave the notes unchanged.
