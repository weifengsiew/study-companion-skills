---
name: teach-me
description: Set up and persist an interactive study session from notes and their sources.
---

# Teach Me

Use this skill when a learner wants a persistent interactive study session using notes tied to source material. 

## 1. Manage study session

Use `study-session-manager` for session setup, progress persistence, preference loading, note updates, and session ending. Use the exact source and notes paths, validated progress state, and relevant confirmed preferences it returns. Never edit progress JSON directly.

## 2. Use tutoring skill

Use `teach-loop` for all live instruction, including explanations, clarifications, questions, assessment, adaptation, pacing, and instructional state. Pass relevant confirmed preferences. For each turn, load only the current concept group's note sections, targeted source excerpts needed for corroboration or examples, and compact progress state. Retrieve more only when the learner advances or asks a cross-topic question.
