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
    "pending_assessment",
    "assessment_history",
    "session_preferences",
    "note_review_queue",
)
PENDING_ASSESSMENT_KEYS = ("question", "citations")
CITATION_KEYS = ("source", "notes")
ASSESSMENT_HISTORY_KEYS = (
    "question",
    "answer",
    "assessment",
    "gaps",
    "citations",
)
SESSION_PREFERENCE_KEYS = ("assessment_emphasis", "response_format")
NOTE_REVIEW_KEYS = (
    "learning_objective",
    "note_location",
    "confirmed_explanation",
)

ASSESSMENT_VALUES = ("correct", "partially_correct", "incorrect")
ASSESSMENT_EMPHASIS_VALUES = (
    "conceptual understanding",
    "technical fluency",
    "balanced mix",
)
RESPONSE_FORMAT_VALUES = ("multiple choice", "short answer", "mix")


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
    value: Any, expected_keys: tuple[str, ...], location: str, errors: list[str]
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{location} must be an object")
        return None
    missing = [key for key in expected_keys if key not in value]
    unknown = [key for key in value if key not in expected_keys]
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


def _validate_preferences(value: Any, errors: list[str]) -> None:
    preferences = _required_object(
        value, SESSION_PREFERENCE_KEYS, "session_preferences", errors
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


def _validate_review_queue(value: Any, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append("note_review_queue must be an array")
        return
    for index, item in enumerate(value):
        location = f"note_review_queue[{index}]"
        entry = _required_object(item, NOTE_REVIEW_KEYS, location, errors)
        if entry is None:
            continue
        for key in ("learning_objective", "note_location"):
            if key in entry:
                _non_empty_string(entry[key], f"{location}.{key}", errors)
        explanation = entry.get("confirmed_explanation")
        if explanation is not None:
            _non_empty_string(
                explanation, f"{location}.confirmed_explanation", errors
            )


def validate_progress(value: Any) -> list[str]:
    errors: list[str] = []
    progress = _required_object(value, TOP_LEVEL_KEYS, "progress", errors)
    if progress is None:
        return errors
    for key in ("source", "notes"):
        if key in progress:
            _non_empty_string(progress[key], key, errors)
    if "pending_assessment" in progress:
        _validate_pending(progress["pending_assessment"], errors)
    if "assessment_history" in progress:
        _validate_history(progress["assessment_history"], errors)
    if "session_preferences" in progress:
        _validate_preferences(progress["session_preferences"], errors)
    if "note_review_queue" in progress:
        _validate_review_queue(progress["note_review_queue"], errors)
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
                "has_pending_assessment": state["pending_assessment"] is not None,
                "assessment_count": len(state["assessment_history"]),
                "note_review_count": len(state["note_review_queue"]),
            }
    _print_json(value)


def _contract() -> dict[str, Any]:
    return {
        "required_keys": {
            "progress": list(TOP_LEVEL_KEYS),
            "pending_assessment": list(PENDING_ASSESSMENT_KEYS),
            "citations": list(CITATION_KEYS),
            "assessment_history_item": list(ASSESSMENT_HISTORY_KEYS),
            "session_preferences": list(SESSION_PREFERENCE_KEYS),
            "note_review_queue_item": list(NOTE_REVIEW_KEYS),
        },
        "field_types": {
            "source": "non-empty string",
            "notes": "non-empty string",
            "pending_assessment": "null or pending_assessment object",
            "pending_assessment.question": "non-empty string",
            "citations.source": "non-empty array of unique non-empty strings",
            "citations.notes": "non-empty array of unique non-empty strings",
            "assessment_history": "array of assessment_history_item objects",
            "assessment_history_item.question": "non-empty string",
            "assessment_history_item.answer": "non-empty string",
            "assessment_history_item.assessment": "assessment allowed value",
            "assessment_history_item.gaps": "array of non-empty strings",
            "assessment_history_item.citations": "citations object",
            "session_preferences": "session_preferences object",
            "session_preferences.assessment_emphasis": (
                "assessment_emphasis allowed value"
            ),
            "session_preferences.response_format": "response_format allowed value",
            "note_review_queue": "array of note_review_queue_item objects",
            "note_review_queue_item.learning_objective": "non-empty string",
            "note_review_queue_item.note_location": "non-empty string",
            "note_review_queue_item.confirmed_explanation": (
                "null or non-empty string"
            ),
        },
        "allowed_values": {
            "assessment": list(ASSESSMENT_VALUES),
            "assessment_emphasis": list(ASSESSMENT_EMPHASIS_VALUES),
            "response_format": list(RESPONSE_FORMAT_VALUES),
        },
        "defaults": {
            "pending_assessment": None,
            "assessment_history": [],
            "note_review_queue": [],
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
    init_parser.add_argument("--source", required=True)
    init_parser.add_argument("--notes", required=True)
    init_parser.add_argument(
        "--assessment-emphasis", required=True, choices=ASSESSMENT_EMPHASIS_VALUES
    )
    init_parser.add_argument(
        "--response-format", required=True, choices=RESPONSE_FORMAT_VALUES
    )

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a progress file"
    )
    _add_file_argument(validate_parser)

    show_parser = subparsers.add_parser("show", help="Print validated progress")
    _add_file_argument(show_parser)

    pending_parser = subparsers.add_parser(
        "set-pending", help="Record a pending assessment"
    )
    _add_file_argument(pending_parser)
    _add_text_input(pending_parser, "question", required=True)
    pending_parser.add_argument("--source-citation", action="append", required=True)
    pending_parser.add_argument("--notes-citation", action="append", required=True)

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
        "--assessment-emphasis", required=True, choices=ASSESSMENT_EMPHASIS_VALUES
    )
    preferences_parser.add_argument(
        "--response-format", required=True, choices=RESPONSE_FORMAT_VALUES
    )

    review_parser = subparsers.add_parser(
        "enqueue-review", help="Add a teach-me note-review entry"
    )
    _add_file_argument(review_parser)
    review_parser.add_argument("--learning-objective", required=True)
    review_parser.add_argument("--note-location", required=True)
    _add_text_input(review_parser, "confirmed-explanation", required=False)

    clear_parser = subparsers.add_parser(
        "clear-reviews", help="Remove reviewed entries from the front of the queue"
    )
    _add_file_argument(clear_parser)
    clear_parser.add_argument("--count", required=True, type=int)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "schema":
            _print_json(_contract())
            return 0

        if args.command == "init":
            notes_path = Path(args.notes)
            path = notes_path.parent / "progress" / f"{notes_path.stem}-progress.json"
            if path.exists():
                raise ProgressError(
                    f"Progress file already exists; refusing to overwrite: {path}"
                )
            state = {
                "source": args.source,
                "notes": args.notes,
                "pending_assessment": None,
                "assessment_history": [],
                "session_preferences": {
                    "assessment_emphasis": args.assessment_emphasis,
                    "response_format": args.response_format,
                },
                "note_review_queue": [],
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
        if args.command == "set-pending":
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
            }
        elif args.command == "record-answer":
            pending = state["pending_assessment"]
            if pending is None:
                raise ProgressError("No pending assessment exists")
            answer = _read_text_argument(args.answer, args.answer_file, "answer")
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
                }
            )
            state["pending_assessment"] = None
        elif args.command == "set-preferences":
            state["session_preferences"] = {
                "assessment_emphasis": args.assessment_emphasis,
                "response_format": args.response_format,
            }
        elif args.command == "enqueue-review":
            explanation = None
            if (
                args.confirmed_explanation is not None
                or args.confirmed_explanation_file is not None
            ):
                explanation = _read_text_argument(
                    args.confirmed_explanation,
                    args.confirmed_explanation_file,
                    "confirmed explanation",
                )
            state["note_review_queue"].append(
                {
                    "learning_objective": args.learning_objective,
                    "note_location": args.note_location,
                    "confirmed_explanation": explanation,
                }
            )
        elif args.command == "clear-reviews":
            if args.count < 1:
                raise ProgressError("--count must be at least 1")
            queue_length = len(state["note_review_queue"])
            if args.count > queue_length:
                raise ProgressError(
                    f"Cannot clear {args.count} reviews; queue contains {queue_length}"
                )
            del state["note_review_queue"][: args.count]
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
