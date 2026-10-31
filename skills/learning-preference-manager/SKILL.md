---
name: learning-preference-manager
description: Load and update confirmed preferences shared by note generation and interactive teaching across repositories.
---

# Learning Preference Manager

## Profile

Use the supplied profile path, then `$STUDY_COMPANION_HOME/learning-preferences.json`, or otherwise `~/.study-companion/learning-preferences.json`. Ask before creating the profile and report if it cannot be accessed. Keep the preference profile under 50 KB.

Store preferences as plain strings under exactly three top-level sections, without predefined sub-keys:

```json
{
  "shared": [],
  "notes": [],
  "teaching": []
}
```

- `shared` applies to both note generation and interactive teaching.
- `notes` applies only when creating or revising notes.
- `teaching` applies only during interactive teaching.

## Load preferences

Return `shared` and `notes` preferences to `notes-generator`. Return `shared` and `teaching` preferences to `teach-me`. When preferences conflict, apply them in this order: current learner instructions; source accuracy and mandatory skill requirements; the relevant context-specific preference; shared preferences; default behavior.

## Update preferences

When asked to update preferences, or when a calling workflow asks at its appropriate stopping point:

1. Identify possible preference changes.
2. Distinguish explicit preferences from inferred observations.
3. Show the proposed changes.
4. Save only confirmed changes, preserving unrelated preferences.

Do not store transcripts, assessment results, sensitive inferences, or unconfirmed preferences. Allow the learner to inspect, revise, or remove preferences.
