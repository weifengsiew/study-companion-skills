---
name: study-session-manager
description: Internal lifecycle support for teach-me and quiz-me. Manage shared study sessions when delegated or explicitly invoked.
---

# Study Session Manager

Support the session lifecycle for `teach-me` and `quiz-me`.

## 1. Set up session

Locate the exact source at `source_dir/<source-name>` and matching notes at `source_dir/notes/<notes-name>`, where `source_dir` contains the source:

- If either exact path is unknown, ask the learner to specify it.
- If the source is absent at its known path, ask the learner to place it there. Do not attempt note generation without it.
- If the source exists but the notes do not, do not invoke `notes-generator`. Ask the learner to provide notes or invoke `notes-generator` themselves and return its reported path. If they refuse, use the source path as the notes path.
- If both files exist, inform the learner of both exact paths and continue.

Do not generate notes directly or invoke `notes-generator`.

## 2. Persist progress

Use `scripts/manage_progress.py` for every progress-file operation; never read or edit progress JSON directly. Run it from this skill directory or use its absolute path. Common commands are:

```bash
python3 scripts/manage_progress.py init [--file <progress-path>] --source <source-path> --notes <notes-path> --question-type <value> [--question-type <value> ...] --response-format <value>
python3 scripts/manage_progress.py show --file <progress-path>
python3 scripts/manage_progress.py set-pending --file <progress-path> --question <text> --source-citation <locator> --notes-citation <locator>
python3 scripts/manage_progress.py replace-question --file <progress-path> --question <text>
python3 scripts/manage_progress.py add-clarification --file <progress-path> --response <text> --prompt <text>
python3 scripts/manage_progress.py record-answer --file <progress-path> --answer <text> --assessment <value> [--gap <text>]
python3 scripts/manage_progress.py revise-latest --file <progress-path> --rationale <text> --reason <text>
python3 scripts/manage_progress.py set-preferences --file <progress-path> --question-type <value> [--question-type <value> ...] --response-format <value>
python3 scripts/manage_progress.py complete --file <progress-path>
```

Before creating a progress file, tell the learner its exact path and proceed only after explicit approval. Confirm the path after creation. Updating an existing approved progress file does not require approval for every response.

`init` creates `not_started`; the first pending question changes it to `active`. `replace-question` does not use the clarification budget. `add-clarification` persists an unresolved response and neutral prompt, up to six, without creating assessment history. `record-answer` resolves the exchange once. `revise-latest` corrects only the latest assessment, clears active gaps, and preserves its audit trail. Use `complete` only after required coverage is mastered and no question is pending. Use `<command> --help` or `schema` for the full contract.

On resumption, continue a pending assessment when present. Otherwise, continue after the latest history entry's cited location, or start at the beginning when history is empty.

Persist through the script after every learner response, clarification, or concept-group completion.

## 3. Load learning preferences

Invoke `learning-preference-manager` with the host's skill-invocation syntax. Load confirmed `shared` and `teaching` preferences relevant to this session, apply the manager's precedence, and return them to the calling workflow. Continue if the profile is unavailable.

## 4. Choose session preferences

At the start of every session, ask in this order:

1. **Question types:** Describe each type and let the learner choose a recommended conceptual mix, technical mix, balanced mix, or any custom combination.
   - **Recall:** Define a term or identify a concept from its description.
   - **Explanation:** Explain how or why something works.
   - **Comparison:** Compare approaches, trade-offs, and suitable uses.
   - **Transfer:** Apply a principle to an unfamiliar situation.
   - **Code or command interpretation:** Explain what given code or a command does, including relevant options.
   - **Code or result tracing:** Predict outputs, state changes, execution paths, or errors.
   - **Workflow sequencing:** Explain or arrange the steps required to complete a technical task.
   - **Diagnosis and troubleshooting:** Identify probable causes and propose appropriate investigations or fixes.
2. **Response format:** Multiple choice, short answer, or a mix.

Expand a recommended mix into its concrete question types. Derive `assessment_emphasis` from the selection: conceptual-only, technical-only, or `balanced mix` when both appear. Do not ask for emphasis separately. If the current request specifies either preference, use it and ask only for what is missing. These are session, not permanent learning, preferences. Save the derived emphasis, selected `question_types`, and response format in `session_preferences`; return and apply them throughout the session, and allow changes at any time. On resumption, ask again and replace the prior choices.

## 5. End session

When the learner pauses, ends early, or reaches normal completion, save progress and ask whether they want to persist the session transcript for a future question bank or notes. Do not save it without explicit agreement. If they agree, ask for a destination unless one was supplied, state the exact transcript path, and proceed only after explicit approval. Save all learner-visible teaching or quiz turns verbatim and in chronological order as Markdown, then confirm the saved path. Preserve their exact wording and speaker attribution; do not summarize, paraphrase, combine, or omit turns. Add only the source, notes, progress path, and final session status as metadata. Exclude hidden reasoning and tool output, and do not overwrite an existing file without approval. Transcript persistence does not authorize generating a question bank or notes.

Then invoke `learning-preference-manager` to propose preference changes. Failure or refusal to save a transcript or update preferences must not prevent the session from ending; save only confirmed preference changes.
