---
name: quiz-me
description: Set up and persist a question-first quiz session from notes and their sources, explaining only identified gaps.
---

# Quiz Me

Use this skill when a learner wants a persistent question-first assessment session using notes tied to source material. The scope may be the full relevant material or an explicit gap manifest supplied by `prepare-for-test`.

## Open

At the start of a directly requested workflow, say exactly:

> Hi! I’ll help you find out what you understand and identify any knowledge gaps. I’ll teach only what needs more work. Which source material and notes would you like to be quizzed on?

If the learner or caller has already supplied all required source material and notes, omit only the final question and continue with them. Do not repeat this opening when `prepare-for-test` invokes `quiz-me` within an active workflow.

## 1. Manage study session

Use `study-session-manager` for session setup, progress persistence, preference loading, and session ending. Use the exact source and notes paths, validated progress state, and relevant confirmed preferences it returns. Neither skill may invoke `notes-generator`: if notes are missing, ask the learner to provide notes or invoke `notes-generator` themselves and return its reported path; if they refuse, use the source path as the notes path. Never edit progress JSON directly or modify notes.

When given a gap manifest, create or resume the separate progress path supplied by the caller. Treat the manifest as read-only target scope, not as progress state. Do not assess source locations outside its recorded gaps and citations.

## 2. Use quizzing skill

Use `quiz-loop` for all live assessment, including questions, assessment, gap explanations, reassessment, pacing, and instructional state. Pass relevant confirmed preferences. For each turn, load only the current concept group's note sections, targeted source excerpts needed for corroboration, and compact progress state. Retrieve more only when the learner advances or a question spans topics.

Pass any gap manifest to `quiz-loop`. Earlier questions, answers, assessments, and gap wording are diagnostic context only; do not reveal them before the learner answers or reuse an earlier question verbatim.

## 3. End session

On pause, early end, or normal completion, use `study-session-manager` to save progress and offer optional transcript persistence.
