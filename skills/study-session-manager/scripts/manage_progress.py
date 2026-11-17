#!/usr/bin/env python3
"""Create, validate, and update study progress files through safe transitions."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


TOP_LEVEL_KEYS = (
    "source",
    "notes",
    "session_status",
    "pending_assessment",
    "assessment_history",
    "session_preferences",
)
LEGACY_TOP_LEVEL_KEYS = ("note_review_queue",)
PENDING_ASSESSMENT_KEYS = (
    "question",
    "citations",
    "learner_responses",
    "clarification_prompts",
    "clarification_count",
)
CITATION_KEYS = ("source", "notes")
ASSESSMENT_HISTORY_KEYS = (
    "question",
    "answer",
    "assessment",
    "gaps",
    "citations",
    "revisions",
)
REVISION_KEYS = ("previous_assessment", "previous_gaps", "rationale", "reason")
SESSION_PREFERENCE_KEYS = ("assessment_emphasis", "response_format")
SESSION_PREFERENCE_OPTIONAL_KEYS = ("question_types",)
ASSESSMENT_VALUES = ("correct", "partially_correct", "incorrect")
SESSION_STATUS_VALUES = ("not_started", "active", "complete")
ASSESSMENT_EMPHASIS_VALUES = (
    "conceptual understanding",
    "technical fluency",
    "balanced mix",
)
RESPONSE_FORMAT_VALUES = ("multiple choice", "short answer", "mix")
CONCEPTUAL_QUESTION_TYPES = (
    "recall",
    "explanation",
    "comparison",
    "transfer",
)
TECHNICAL_QUESTION_TYPES = (
    "code or command interpretation",
    "code or result tracing",
    "workflow sequencing",
    "diagnosis and troubleshooting",
)
QUESTION_TYPE_VALUES = CONCEPTUAL_QUESTION_TYPES + TECHNICAL_QUESTION_TYPES


def _default_question_types(emphasis: str) -> list[str]:
    if emphasis == "conceptual understanding":
        return list(CONCEPTUAL_QUESTION_TYPES)
    if emphasis == "technical fluency":
        return list(TECHNICAL_QUESTION_TYPES)
    return list(QUESTION_TYPE_VALUES)


def _derive_emphasis(question_types: list[str]) -> str:
    selected = set(question_types)
    if selected <= set(CONCEPTUAL_QUESTION_TYPES):
        return "conceptual understanding"
    if selected <= set(TECHNICAL_QUESTION_TYPES):
        return "technical fluency"
    return "balanced mix"


class ProgressError(Exception):
    """A user-correctable progress-file error."""

    def __init__(self, errors: str | Iterable[str]):
        if isinstance(errors, str):
            self.errors = [errors]
        else:
            self.errors = list(errors)
        super().__init__("; ".join(self.errors))


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        _print_json({"ok": False, "errors": [message]}, stream=sys.stderr)
        raise SystemExit(2)


def _print_json(value: Any, *, stream: Any = sys.stdout) -> None:
    json.dump(value, stream, indent=2, ensure_ascii=False)
    stream.write("\n")


def _required_object(
    value: Any,
    expected_keys: tuple[str, ...],
    location: str,
    errors: list[str],
    *,
    optional_keys: tuple[str, ...] = (),
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{location} must be an object")
        return None
    missing = [key for key in expected_keys if key not in value]
    unknown = [
        key for key in value if key not in expected_keys and key not in optional_keys
    ]
    errors.extend(f"Missing required key: {location}.{key}" for key in missing)
    errors.extend(f"Unknown key: {location}.{key}" for key in unknown)
    return value


def _non_empty_string(value: Any, location: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{location} must be a non-empty string")


def _string_list(
    value: Any,
    location: str,
    errors: list[str],
    *,
    non_empty: bool,
    unique: bool = False,
) -> None:
    if not isinstance(value, list):
        errors.append(f"{location} must be an array")
        return
    if non_empty and not value:
        errors.append(f"{location} must contain at least one item")
    for index, item in enumerate(value):
        _non_empty_string(item, f"{location}[{index}]", errors)
    if unique and len(value) != len(set(item for item in value if isinstance(item, str))):
        errors.append(f"{location} must contain unique items")


def _validate_citations(value: Any, location: str, errors: list[str]) -> None:
    citations = _required_object(value, CITATION_KEYS, location, errors)
    if citations is None:
        return
    for key in CITATION_KEYS:
        if key in citations:
            _string_list(
                citations[key],
                f"{location}.{key}",
                errors,
                non_empty=True,
                unique=True,
            )


def _validate_pending(value: Any, errors: list[str]) -> None:
    if value is None:
        return
    pending = _required_object(
        value, PENDING_ASSESSMENT_KEYS, "pending_assessment", errors
    )
    if pending is None:
        return
    if "question" in pending:
        _non_empty_string(pending["question"], "pending_assessment.question", errors)
    if "citations" in pending:
        _validate_citations(
            pending["citations"], "pending_assessment.citations", errors
        )
    for key in ("learner_responses", "clarification_prompts"):
        if key in pending:
            _string_list(
                pending[key], f"pending_assessment.{key}", errors, non_empty=False
            )
    count = pending.get("clarification_count")
    if not isinstance(count, int) or isinstance(count, bool) or not 0 <= count <= 6:
        errors.append("pending_assessment.clarification_count must be from 0 to 6")
    elif (
        isinstance(pending.get("learner_responses"), list)
        and isinstance(pending.get("clarification_prompts"), list)
        and (
            len(pending["learner_responses"]) != count
            or len(pending["clarification_prompts"]) != count
        )
    ):
        errors.append(
            "pending assessment clarification lists must match clarification_count"
        )


def _validate_history(value: Any, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append("assessment_history must be an array")
        return
    for index, item in enumerate(value):
        location = f"assessment_history[{index}]"
        entry = _required_object(item, ASSESSMENT_HISTORY_KEYS, location, errors)
        if entry is None:
            continue
        for key in ("question", "answer"):
            if key in entry:
                _non_empty_string(entry[key], f"{location}.{key}", errors)
        if "assessment" in entry and entry["assessment"] not in ASSESSMENT_VALUES:
            errors.append(
                f"{location}.assessment must be one of: "
                + ", ".join(ASSESSMENT_VALUES)
            )
        if "gaps" in entry:
            _string_list(
                entry["gaps"], f"{location}.gaps", errors, non_empty=False
            )
            if entry.get("assessment") == "correct" and entry["gaps"]:
                errors.append(f"{location}.gaps must be empty when assessment is correct")
            if entry.get("assessment") in {"partially_correct", "incorrect"} and not entry[
                "gaps"
            ]:
                errors.append(
                    f"{location}.gaps must not be empty when assessment is "
                    f"{entry.get('assessment')}"
                )
        if "citations" in entry:
            _validate_citations(entry["citations"], f"{location}.citations", errors)
        revisions = entry.get("revisions")
        if not isinstance(revisions, list):
            errors.append(f"{location}.revisions must be an array")
        else:
            for revision_index, item in enumerate(revisions):
                revision_location = f"{location}.revisions[{revision_index}]"
                revision = _required_object(
                    item, REVISION_KEYS, revision_location, errors
                )
                if revision is None:
                    continue
                if revision.get("previous_assessment") not in ASSESSMENT_VALUES:
                    errors.append(
                        f"{revision_location}.previous_assessment must be one of: "
                        + ", ".join(ASSESSMENT_VALUES)
                    )
                if "previous_gaps" in revision:
                    _string_list(
                        revision["previous_gaps"],
                        f"{revision_location}.previous_gaps",
                        errors,
                        non_empty=True,
                    )
                for key in ("rationale", "reason"):
                    if key in revision:
                        _non_empty_string(
                            revision[key], f"{revision_location}.{key}", errors
                        )


def _validate_preferences(value: Any, errors: list[str]) -> None:
    preferences = _required_object(
        value,
        SESSION_PREFERENCE_KEYS,
        "session_preferences",
        errors,
        optional_keys=SESSION_PREFERENCE_OPTIONAL_KEYS,
    )
    if preferences is None:
        return
    emphasis = preferences.get("assessment_emphasis")
    if emphasis not in ASSESSMENT_EMPHASIS_VALUES:
        errors.append(
            "session_preferences.assessment_emphasis must be one of: "
            + ", ".join(ASSESSMENT_EMPHASIS_VALUES)
        )
    response_format = preferences.get("response_format")
    if response_format not in RESPONSE_FORMAT_VALUES:
        errors.append(
            "session_preferences.response_format must be one of: "
            + ", ".join(RESPONSE_FORMAT_VALUES)
        )
    question_types = preferences.get("question_types")
    if question_types is not None:
        _string_list(
            question_types,
            "session_preferences.question_types",
            errors,
            non_empty=True,
            unique=True,
        )
        if isinstance(question_types, list):
            invalid = [item for item in question_types if item not in QUESTION_TYPE_VALUES]
            if invalid:
                errors.append(
                    "session_preferences.question_types must contain only: "
                    + ", ".join(QUESTION_TYPE_VALUES)
                )
            elif question_types and emphasis in ASSESSMENT_EMPHASIS_VALUES:
                if _derive_emphasis(question_types) != emphasis:
                    errors.append(
                        "session_preferences.assessment_emphasis must match "
                        "session_preferences.question_types"
                    )
            invalid = [item for item in question_types if item not in QUESTION_TYPE_VALUES]
            if invalid:
                errors.append(
                    "session_preferences.question_types contains unsupported values: "
                    + ", ".join(str(item) for item in invalid)
                )
            elif emphasis in ASSESSMENT_EMPHASIS_VALUES and _derive_emphasis(
                question_types
            ) != emphasis:
                errors.append(
                    "session_preferences.assessment_emphasis must match question_types"
                )


def validate_progress(value: Any) -> list[str]:
    errors: list[str] = []
    progress = _required_object(
        value,
        TOP_LEVEL_KEYS,
        "progress",
        errors,
        optional_keys=LEGACY_TOP_LEVEL_KEYS,
    )
    if progress is None:
        return errors
    for key in ("source", "notes"):
        if key in progress:
            _non_empty_string(progress[key], key, errors)
    if (
        "session_status" in progress
        and progress["session_status"] not in SESSION_STATUS_VALUES
    ):
        errors.append(
            "session_status must be one of: " + ", ".join(SESSION_STATUS_VALUES)
        )
    if (
        progress.get("session_status") == "complete"
        and progress.get("pending_assessment") is not None
    ):
        errors.append("pending_assessment must be null when session_status is complete")
    if "pending_assessment" in progress:
        _validate_pending(progress["pending_assessment"], errors)
    if "assessment_history" in progress:
        _validate_history(progress["assessment_history"], errors)
    if "session_preferences" in progress:
        _validate_preferences(progress["session_preferences"], errors)
    return errors


def _load(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError as error:
        raise ProgressError(f"Progress file does not exist: {path}") from error
    except (OSError, json.JSONDecodeError) as error:
        raise ProgressError(f"Could not read valid JSON from {path}: {error}") from error
    errors = validate_progress(value)
    if errors:
        raise ProgressError(errors)
    value.pop("note_review_queue", None)
    preferences = value["session_preferences"]
    if "question_types" not in preferences:
        preferences["question_types"] = _default_question_types(
            preferences["assessment_emphasis"]
        )
    return value


def _write_atomic(path: Path, value: dict[str, Any]) -> None:
    errors = validate_progress(value)
    if errors:
        raise ProgressError(errors)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    except OSError as error:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise ProgressError(f"Could not write progress file {path}: {error}") from error


def _read_text_argument(value: str | None, file: str | None, label: str) -> str:
    if value is not None:
        result = value
    else:
        assert file is not None
        try:
            result = Path(file).read_text(encoding="utf-8")
        except OSError as error:
            raise ProgressError(f"Could not read {label} file {file}: {error}") from error
    if not result.strip():
        raise ProgressError(f"{label} must be a non-empty string")
    return result


def _result(
    operation: str,
    path: Path,
    state: dict[str, Any] | None = None,
    *,
    include_state: bool = False,
) -> None:
    value: dict[str, Any] = {
        "ok": True,
        "operation": operation,
        "file": str(path),
    }
    if state is not None:
        if include_state:
            value["state"] = state
        else:
            value["summary"] = {
                "session_status": state["session_status"],
                "has_pending_assessment": state["pending_assessment"] is not None,
                "assessment_count": len(state["assessment_history"]),
            }
    _print_json(value)


def _contract() -> dict[str, Any]:
    return {
        "required_keys": {
            "progress": list(TOP_LEVEL_KEYS),
            "pending_assessment": list(PENDING_ASSESSMENT_KEYS),
            "citations": list(CITATION_KEYS),
            "assessment_history_item": list(ASSESSMENT_HISTORY_KEYS),
            "revision": list(REVISION_KEYS),
            "session_preferences": list(SESSION_PREFERENCE_KEYS),
        },
        "optional_keys": {
            "session_preferences": list(SESSION_PREFERENCE_OPTIONAL_KEYS),
        },
        "field_types": {
            "source": "non-empty string",
            "notes": "non-empty string",
            "session_status": "session_status allowed value",
            "pending_assessment": "null or pending_assessment object",
            "pending_assessment.question": "non-empty string",
            "pending_assessment.learner_responses": "array of non-empty strings",
            "pending_assessment.clarification_prompts": "array of non-empty strings",
            "pending_assessment.clarification_count": "integer from 0 to 6",
            "citations.source": "non-empty array of unique non-empty strings",
            "citations.notes": "non-empty array of unique non-empty strings",
            "assessment_history": "array of assessment_history_item objects",
            "assessment_history_item.question": "non-empty string",
            "assessment_history_item.answer": "non-empty string",
            "assessment_history_item.assessment": "assessment allowed value",
            "assessment_history_item.gaps": "array of non-empty strings",
            "assessment_history_item.citations": "citations object",
            "assessment_history_item.revisions": "array of revision objects",
            "revision.previous_assessment": "assessment allowed value",
            "revision.previous_gaps": "non-empty array of non-empty strings",
            "revision.rationale": "non-empty string",
            "revision.reason": "non-empty string",
            "session_preferences": "session_preferences object",
            "session_preferences.assessment_emphasis": (
                "assessment_emphasis allowed value"
            ),
            "session_preferences.response_format": "response_format allowed value",
            "session_preferences.question_types": (
                "non-empty array of unique question_type allowed values"
            ),
        },
        "allowed_values": {
            "assessment": list(ASSESSMENT_VALUES),
            "session_status": list(SESSION_STATUS_VALUES),
            "assessment_emphasis": list(ASSESSMENT_EMPHASIS_VALUES),
            "response_format": list(RESPONSE_FORMAT_VALUES),
            "question_type": list(QUESTION_TYPE_VALUES),
        },
        "defaults": {
            "session_status": "not_started",
            "pending_assessment": None,
            "assessment_history": [],
        },
        "constraints": {
            "additional_properties": False,
            "citation_arrays": "non-empty, ordered, unique strings",
            "correct_assessment_gaps": [],
            "non_correct_assessment_gaps": "at least one non-empty string",
        },
    }


def _add_file_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--file", required=True, type=Path)


def _add_text_input(
    parser: argparse.ArgumentParser, name: str, *, required: bool
) -> None:
    group = parser.add_mutually_exclusive_group(required=required)
    group.add_argument(f"--{name}")
    group.add_argument(f"--{name}-file")


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("schema", help="Print the authoritative contract")

    init_parser = subparsers.add_parser("init", help="Create a new progress file")
    init_parser.add_argument(
        "--file", type=Path, help="Exact output path (default: derived from --notes)"
    )
    init_parser.add_argument("--source", required=True)
    init_parser.add_argument("--notes", required=True)
    init_parser.add_argument(
        "--assessment-emphasis", choices=ASSESSMENT_EMPHASIS_VALUES
    )
    init_parser.add_argument("--question-type", action="append", choices=QUESTION_TYPE_VALUES)
    init_parser.add_argument(
        "--response-format", required=True, choices=RESPONSE_FORMAT_VALUES
    )

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a progress file"
    )
    _add_file_argument(validate_parser)

    show_parser = subparsers.add_parser("show", help="Print validated progress")
    _add_file_argument(show_parser)

    complete_parser = subparsers.add_parser(
        "complete", help="Mark fully assessed coverage as complete"
    )
    _add_file_argument(complete_parser)

    pending_parser = subparsers.add_parser(
        "set-pending", help="Record a pending assessment"
    )
    _add_file_argument(pending_parser)
    _add_text_input(pending_parser, "question", required=True)
    pending_parser.add_argument("--source-citation", action="append", required=True)
    pending_parser.add_argument("--notes-citation", action="append", required=True)

    replace_parser = subparsers.add_parser(
        "replace-question", help="Replace a pending question without using a clarification"
    )
    _add_file_argument(replace_parser)
    _add_text_input(replace_parser, "question", required=True)

    clarification_parser = subparsers.add_parser(
        "add-clarification", help="Persist one unresolved response and neutral prompt"
    )
    _add_file_argument(clarification_parser)
    _add_text_input(clarification_parser, "response", required=True)
    _add_text_input(clarification_parser, "prompt", required=True)

    revision_parser = subparsers.add_parser(
        "revise-latest", help="Correct the latest assessment to correct"
    )
    _add_file_argument(revision_parser)
    _add_text_input(revision_parser, "rationale", required=True)
    _add_text_input(revision_parser, "reason", required=True)

    answer_parser = subparsers.add_parser(
        "record-answer", help="Assess the answer to the pending question"
    )
    _add_file_argument(answer_parser)
    _add_text_input(answer_parser, "answer", required=True)
    answer_parser.add_argument(
        "--assessment", required=True, choices=ASSESSMENT_VALUES
    )
    answer_parser.add_argument("--gap", action="append", default=[])

    preferences_parser = subparsers.add_parser(
        "set-preferences", help="Replace session preferences"
    )
    _add_file_argument(preferences_parser)
    preferences_parser.add_argument(
        "--assessment-emphasis", choices=ASSESSMENT_EMPHASIS_VALUES
    )
    preferences_parser.add_argument(
        "--question-type", action="append", choices=QUESTION_TYPE_VALUES
    )
    preferences_parser.add_argument(
        "--response-format", required=True, choices=RESPONSE_FORMAT_VALUES
    )

    return parser


def _preference_values(args: argparse.Namespace) -> dict[str, Any]:
    question_types = args.question_type
    if question_types is None:
        if args.assessment_emphasis is None:
            raise ProgressError(
                "Provide at least one --question-type or --assessment-emphasis"
            )
        question_types = _default_question_types(args.assessment_emphasis)
    if len(question_types) != len(set(question_types)):
        raise ProgressError("--question-type values must be unique")
    derived_emphasis = _derive_emphasis(question_types)
    if (
        args.assessment_emphasis is not None
        and args.assessment_emphasis != derived_emphasis
    ):
        raise ProgressError(
            "--assessment-emphasis does not match the selected question types"
        )
    return {
        "assessment_emphasis": derived_emphasis,
        "question_types": question_types,
        "response_format": args.response_format,
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "schema":
            _print_json(_contract())
            return 0

        if args.command == "init":
            notes_path = Path(args.notes)
            path = args.file or (
                notes_path.parent / "progress" / f"{notes_path.stem}-progress.json"
            )
            if path.exists():
                raise ProgressError(
                    f"Progress file already exists; refusing to overwrite: {path}"
                )
            state = {
                "source": args.source,
                "notes": args.notes,
                "session_status": "not_started",
                "pending_assessment": None,
                "assessment_history": [],
                "session_preferences": _preference_values(args),
            }
            _write_atomic(path, state)
            _result("init", path, state)
            return 0

        path = args.file
        state = _load(path)

        if args.command == "validate":
            _result("validate", path)
            return 0
        if args.command == "show":
            _result("show", path, state, include_state=True)
            return 0
        if args.command == "complete":
            if state["pending_assessment"] is not None:
                raise ProgressError(
                    "Cannot complete a session with a pending assessment"
                )
            if state["session_status"] == "not_started":
                raise ProgressError("Cannot complete a session that has not started")
            state["session_status"] = "complete"
            _write_atomic(path, state)
            _result(args.command, path, state)
            return 0
        if args.command == "set-pending":
            if state["session_status"] == "complete":
                raise ProgressError("A completed session cannot accept new questions")
            if state["pending_assessment"] is not None:
                raise ProgressError(
                    "pending_assessment is already populated; record its answer first"
                )
            question = _read_text_argument(
                args.question, args.question_file, "question"
            )
            state["pending_assessment"] = {
                "question": question,
                "citations": {
                    "source": args.source_citation,
                    "notes": args.notes_citation,
                },
                "learner_responses": [],
                "clarification_prompts": [],
                "clarification_count": 0,
            }
            state["session_status"] = "active"
        elif args.command == "replace-question":
            pending = state["pending_assessment"]
            if pending is None:
                raise ProgressError("No pending assessment exists")
            pending["question"] = _read_text_argument(
                args.question, args.question_file, "question"
            )
        elif args.command == "add-clarification":
            pending = state["pending_assessment"]
            if pending is None:
                raise ProgressError("No pending assessment exists")
            if pending["clarification_count"] >= 6:
                raise ProgressError("The six-prompt clarification limit is exhausted")
            response = _read_text_argument(
                args.response, args.response_file, "response"
            )
            prompt = _read_text_argument(args.prompt, args.prompt_file, "prompt")
            pending["learner_responses"].append(response)
            pending["clarification_prompts"].append(prompt)
            pending["clarification_count"] += 1
        elif args.command == "record-answer":
            pending = state["pending_assessment"]
            if pending is None:
                raise ProgressError("No pending assessment exists")
            final_answer = _read_text_argument(args.answer, args.answer_file, "answer")
            answer = "\n\n".join(pending["learner_responses"] + [final_answer])
            if args.assessment == "correct" and args.gap:
                raise ProgressError("A correct assessment cannot include gaps")
            if args.assessment != "correct" and not args.gap:
                raise ProgressError(
                    "A partially_correct or incorrect assessment requires at least one gap"
                )
            state["assessment_history"].append(
                {
                    "question": pending["question"],
                    "answer": answer,
                    "assessment": args.assessment,
                    "gaps": args.gap,
                    "citations": pending["citations"],
                    "revisions": [],
                }
            )
            state["pending_assessment"] = None
        elif args.command == "revise-latest":
            if state["pending_assessment"] is not None:
                raise ProgressError(
                    "Resolve the pending assessment before revising history"
                )
            if not state["assessment_history"]:
                raise ProgressError("No assessment exists to revise")
            latest = state["assessment_history"][-1]
            if latest["assessment"] == "correct":
                raise ProgressError("The latest assessment is already correct")
            rationale = _read_text_argument(
                args.rationale, args.rationale_file, "rationale"
            )
            reason = _read_text_argument(args.reason, args.reason_file, "reason")
            latest["revisions"].append(
                {
                    "previous_assessment": latest["assessment"],
                    "previous_gaps": latest["gaps"],
                    "rationale": rationale,
                    "reason": reason,
                }
            )
            latest["assessment"] = "correct"
            latest["gaps"] = []
        elif args.command == "set-preferences":
            state["session_preferences"] = _preference_values(args)
        else:
            raise ProgressError(f"Unsupported command: {args.command}")

        _write_atomic(path, state)
        _result(args.command, path, state)
        return 0
    except ProgressError as error:
        _print_json({"ok": False, "errors": error.errors}, stream=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
