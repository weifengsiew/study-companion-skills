---
name: teach-me
description: Set up and persist an interactive study session from notes and their sources.
---

# Teach Me

Use this skill when a learner wants a persistent interactive study session using notes tied to source material. 

## 1. Manage study session

Use `study-session-manager` for session setup, progress persistence, preference loading, note updates, and session ending. Use the exact source and notes paths, progress state, and relevant confirmed preferences it returns.

## 2. Use tutoring skill

Use `teach-loop` skill for all live instruction, including explanations, clarifications, questions, assessment, adaptation, pacing, and instructional state. Pass it the relevant confirmed preferences. Use notes to teach concepts, source material to supply illustrative examples and progress json to track and update progress.
