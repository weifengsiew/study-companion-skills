---
name: teach-me-preference-manager
description: Load and update confirmed teaching preferences across study sessions and repositories.
---

# Teach Me Preference Manager

## Profile

Use the supplied profile path, then `$STUDY_COMPANION_HOME/learning-preferences.json`, or otherwise `~/.study-companion/learning-preferences.json`. Ask before creating the profile and report if it cannot be accessed. Keep the preference profile under 50 KB.

## Start of session

Return relevant confirmed preferences to `teach-me`. Preferences may guide pacing, explanation depth, examples, questions, feedback, terminology, scaffolding, and learning aids. Current learner instructions and source accuracy take precedence.

## End of session

When the learner explicitly pauses or ends:

1. Identify possible preference changes.
2. Distinguish explicit preferences from inferred observations.
3. Show the proposed changes.
4. Save only confirmed changes, preserving unrelated preferences.

Do not store transcripts, assessment results, sensitive inferences, or unconfirmed preferences. Allow the learner to inspect, revise, or remove preferences.
