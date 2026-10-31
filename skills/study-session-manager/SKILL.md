---
name: study-session-manager
description: Manage the shared lifecycle of persistent teach-me and quiz-me sessions, including setup, progress, preferences, note updates, and ending.
---

# Study Session Manager

Use this skill as the session-lifecycle support for `teach-me` and `quiz-me`.

## 1. Set up session

Find the exact source material at `source_dir/<source-name>` and its matching notes at `source_dir/notes/<notes-name>`, where `source_dir` is the source material's containing directory. Handle setup according to what is known and available:

- If either exact path is unknown, ask the learner to specify it.
- If the source path is known but the source is absent, ask the learner to place the source material there. Do not attempt note generation without the source.
- If the source exists but the notes are absent, invoke the available `notes-generator` skill using the host's skill-invocation syntax. Return to setup after the notes file has been created, using the exact notes path reported by `notes-generator`.
- If both files exist, inform the learner of both exact paths and continue.

Do not generate notes directly.

## 2. Persist progress

Create `source_dir/notes/progress/<notes-stem>-progress.json` if it does not exist, where `<notes-stem>` is the notes filename without its final extension. If a progress file already exists during session setup, do not replace or reset it without asking; resume it by default. Routine state updates during an active session do not require repeated confirmation. Track exactly:

1. `source` — source path.
2. `notes` — matching notes path.
3. `current_chunk` — current subsection, status, and pending question.
4. `concept_coverage` — required, tested, and remaining concepts.
5. `assessment_history` — learner answers and assessment results.

Update the progress file after every learner response, clarification, or note change.

## 3. Load learning preferences

Invoke the available `learning-preference-manager` skill using the host's skill-invocation syntax and load confirmed `shared` and `teaching` preferences relevant to the current session. Continue without them if the profile is unavailable. Apply the preference precedence defined by the manager and return the relevant preferences to the calling workflow.

## 4. Manage note updates

After an initial or substantially adapted explanation, ask: "Is that clear, or should I explain it another way?" Continue explaining if further clarification is needed.

Whenever the learner confirms an explanation is clear, propose it as a replacement for the corresponding notes, and specify what it would change. Preserve all relevant source-supported detail. Show the original and proposed wording, and edit only with explicit confirmation. Use an independent subagent only for complex or cross-subsection changes.

## 5. End session

When the learner explicitly pauses or ends the session, save progress first, then invoke `learning-preference-manager` to propose preference changes. Save only confirmed changes. Failure or refusal to update preferences must not prevent the session from ending.
