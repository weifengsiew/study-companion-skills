---
name: quiz-me
description: Set up and persist a question-first quiz session from notes and their sources, explaining only identified gaps.
---

# Quiz Me

Use this skill when a learner wants a persistent question-first assessment session using notes tied to source material.

## 1. Manage study session

Use `study-session-manager` for session setup, progress persistence, preference loading, note updates, and session ending. Use the exact source and notes paths, progress state, and relevant confirmed preferences it returns.

## 2. Use quizzing skill

Use `quiz-loop` for all live assessment, including questions, assessment, gap explanations, reassessment, pacing, and instructional state. Pass relevant confirmed preferences. For each turn, load only the current concept group's note sections, targeted source excerpts needed for corroboration, and compact progress state. Retrieve more only when the learner advances or a question spans topics.
