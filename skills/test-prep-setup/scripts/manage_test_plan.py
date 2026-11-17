#!/usr/bin/env python3
"""Create and validate a test-preparation workspace."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


TOPIC_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
PROGRESS_MANAGER = (
    Path(__file__).parents[2]
    / "study-session-manager"
    / "scripts"
    / "manage_progress.py"
)
ASSESSMENT_EMPHASIS = (
    "conceptual understanding",
    "technical fluency",
    "balanced mix",
)
RESPONSE_FORMATS = ("multiple choice", "short answer", "mix")
QUESTION_TYPES = (
    "recall",
    "explanation",
    "comparison",
    "transfer",
    "code or command interpretation",
    "code or result tracing",
    "workflow sequencing",
    "diagnosis and troubleshooting",
)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    initialize = commands.add_parser("init", help="Create a test-prep workspace")
    initialize.add_argument("--root", required=True, type=Path)
    initialize.add_argument("--topics-file", required=True, type=Path)
    initialize.add_argument(
        "--assessment-emphasis", choices=ASSESSMENT_EMPHASIS
    )
    initialize.add_argument("--question-type", action="append", choices=QUESTION_TYPES)
    initialize.add_argument(
        "--response-format", required=True, choices=RESPONSE_FORMATS
    )
    initialize.add_argument(
        "--topic",
        action="append",
        nargs=3,
        required=True,
        metavar=("ID", "SOURCE", "NOTES"),
    )

    for command in ("show", "check"):
        child = commands.add_parser(command, help=f"{command.title()} an existing plan")
        child.add_argument("--root", required=True, type=Path)
    return root


def plan_path(root: Path) -> Path:
    return root / "test-plan.json"


def validate(plan: Any) -> list[str]:
    if not isinstance(plan, dict):
        return ["test plan must be a JSON object"]
    if set(plan) != {"schema_version", "topics_file", "topics"}:
        return ["test plan must contain schema_version, topics_file, and topics"]
    errors: list[str] = []
    if plan["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if not isinstance(plan["topics_file"], str) or not plan["topics_file"].strip():
        errors.append("topics_file must be a non-empty string")
    topics = plan["topics"]
    if not isinstance(topics, list) or not topics:
        errors.append("topics must be a non-empty array")
        return errors
    seen: set[str] = set()
    for index, topic in enumerate(topics):
        location = f"topics[{index}]"
        if not isinstance(topic, dict) or set(topic) != {"id", "source", "notes"}:
            errors.append(f"{location} must contain id, source, and notes")
            continue
        identifier = topic["id"]
        if not isinstance(identifier, str) or not TOPIC_ID.fullmatch(identifier):
            errors.append(f"{location}.id must be filename-safe")
        elif identifier in seen:
            errors.append(f"duplicate topic id: {identifier}")
        else:
            seen.add(identifier)
        for key in ("source", "notes"):
            if not isinstance(topic[key], str) or not topic[key].strip():
                errors.append(f"{location}.{key} must be a non-empty string")
    return errors


def readable(path: Path, label: str) -> str | None:
    try:
        with path.open("rb") as handle:
            handle.read(1)
    except OSError as error:
        return f"{label} is not readable: {path}: {error}"
    return None


def check_access(plan: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    paths = [(Path(plan["topics_file"]), "topics_file")]
    for topic in plan["topics"]:
        paths.extend(
            (Path(topic[key]), f"{topic['id']} {key}") for key in ("source", "notes")
        )
    errors.extend(error for path, label in paths if (error := readable(path, label)))
    progress_directory = root / "progress" / "pass_01" / "progress"
    for topic in plan["topics"]:
        progress = progress_directory / f"{topic['id']}-progress.json"
        result = subprocess.run(
            [sys.executable, str(PROGRESS_MANAGER), "validate", "--file", str(progress)],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            errors.append(f"{topic['id']} progress is missing or invalid: {result.stderr.strip()}")
    return errors


def write_atomic(path: Path, text: str) -> None:
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
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    errors = validate(value)
    if errors:
        raise ValueError("; ".join(errors))
    return value


def main() -> None:
    args = parser().parse_args()
    path = plan_path(args.root)
    if args.command in {"show", "check"}:
        plan = load(path)
        if args.command == "check":
            errors = check_access(plan, args.root)
            if errors:
                raise ValueError("; ".join(errors))
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return

    canonical_topics = args.root / "test-topics.md"
    initial_progress = args.root / "progress" / "pass_01" / "progress"
    same_topics_file = args.topics_file.resolve() == canonical_topics.resolve()
    if path.exists() or initial_progress.exists() or (
        canonical_topics.exists() and not same_topics_file
    ):
        raise FileExistsError(
            f"setup already exists; refusing to replace files under: {args.root}"
        )
    topics_error = readable(args.topics_file, "topics file")
    plan = {
        "schema_version": 1,
        "topics_file": str(canonical_topics),
        "topics": [
            {"id": identifier, "source": source, "notes": notes}
            for identifier, source, notes in args.topic
        ],
    }
    errors = validate(plan)
    if topics_error:
        errors.append(topics_error)
    for topic in plan["topics"]:
        for key in ("source", "notes"):
            error = readable(Path(topic[key]), f"{topic['id']} {key}")
            if error:
                errors.append(error)
    if errors:
        raise ValueError("; ".join(errors))

    if not same_topics_file:
        topics_text = args.topics_file.read_text(encoding="utf-8")
        write_atomic(canonical_topics, topics_text)
    rendered = json.dumps(plan, indent=2, ensure_ascii=False) + "\n"
    write_atomic(path, rendered)
    initial_progress.mkdir(parents=True, exist_ok=False)
    for topic in plan["topics"]:
        progress = initial_progress / f"{topic['id']}-progress.json"
        preference_arguments = ["--response-format", args.response_format]
        if args.assessment_emphasis is not None:
            preference_arguments.extend(
                ("--assessment-emphasis", args.assessment_emphasis)
            )
        for question_type in args.question_type or []:
            preference_arguments.extend(("--question-type", question_type))
        result = subprocess.run(
            [
                sys.executable,
                str(PROGRESS_MANAGER),
                "init",
                "--file",
                str(progress),
                "--source",
                topic["source"],
                "--notes",
                topic["notes"],
                *preference_arguments,
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise RuntimeError(result.stderr.strip())
    print(json.dumps(plan, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
