#!/usr/bin/env python3
"""Inspect test-prep state and initialize targeted passes."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILLS = Path(__file__).parents[2]
PROGRESS_MANAGER = SKILLS / "study-session-manager/scripts/manage_progress.py"
PASS_NAME = re.compile(r"^pass_(\d+)$")
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
DEFAULT_ASSESSMENT_EMPHASIS = "balanced mix"
DEFAULT_RESPONSE_FORMAT = "short answer"


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    status = commands.add_parser("status", help="Return the next workflow action")
    status.add_argument("--root", required=True, type=Path)
    initialize = commands.add_parser(
        "init-pass", help="Initialize progress files for a targeted pass"
    )
    initialize.add_argument("--root", required=True, type=Path)
    initialize.add_argument("--pass-number", required=True, type=int)
    initialize.add_argument(
        "--assessment-emphasis", choices=ASSESSMENT_EMPHASIS
    )
    initialize.add_argument("--question-type", action="append", choices=QUESTION_TYPES)
    initialize.add_argument(
        "--response-format", default=DEFAULT_RESPONSE_FORMAT, choices=RESPONSE_FORMATS
    )
    return root


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def manager(*arguments: str) -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, str(PROGRESS_MANAGER), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip())
    return json.loads(result.stdout)


def pass_path(root: Path, number: int) -> Path:
    return root / "progress" / f"pass_{number:02d}"


def highest_pass(root: Path) -> int:
    progress_root = root / "progress"
    numbers = [
        int(match.group(1))
        for path in progress_root.iterdir()
        if path.is_dir() and (match := PASS_NAME.fullmatch(path.name))
    ]
    if not numbers:
        raise ValueError("no numbered pass directories found")
    return max(numbers)


def entries(root: Path, number: int) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    directory = pass_path(root, number)
    if number == 1:
        plan = load_json(root / "test-plan.json")
        return [
            {
                **topic,
                "progress": directory / "progress" / f"{topic['id']}-progress.json",
                "gaps": None,
            }
            for topic in plan["topics"]
        ], None

    gaps_directory = directory / "gaps"
    manifest_path = gaps_directory / "_manifest.json"
    if not manifest_path.is_file():
        return [], None
    manifest = load_json(manifest_path)
    result = []
    for item in manifest["files"]:
        gaps_path = gaps_directory / item["gaps_file"]
        gap_data = load_json(gaps_path)
        topic_id = item["gaps_file"].removesuffix("-gaps.json")
        result.append(
            {
                "id": topic_id,
                "source": gap_data["source"],
                "notes": gap_data["notes"],
                "progress": directory / "progress" / f"{topic_id}-progress.json",
                "gaps": gaps_path,
            }
        )
    return result, manifest


def status(root: Path) -> dict[str, Any]:
    number = highest_pass(root)
    pass_directory = pass_path(root, number)
    topic_entries, manifest = entries(root, number)

    if number > 1 and manifest is None:
        previous = pass_path(root, number - 1)
        return {
            "next_action": "extract_gaps",
            "completed_pass": number - 1,
            "progress_directory": str(previous / "progress"),
            "gaps_directory": str(pass_directory / "gaps"),
        }
    if manifest is not None and manifest["assessment_count"] == 0:
        return {
            "next_action": "workflow_complete",
            "completed_pass": number - 1,
            "manifest": str(pass_directory / "gaps" / "_manifest.json"),
        }

    missing = [entry for entry in topic_entries if not entry["progress"].is_file()]
    if missing:
        return {
            "next_action": "setup_required" if number == 1 else "initialize_pass",
            "pass_number": number,
            "topics": [entry["id"] for entry in missing],
        }

    for entry in topic_entries:
        state = manager("show", "--file", str(entry["progress"]))["state"]
        session_status = state["session_status"]
        if session_status == "complete":
            continue
        if state["pending_assessment"] is not None:
            action = "resume_pending"
        elif session_status == "active":
            action = "resume_quiz"
        else:
            action = "start_quiz"
        result = {
            "next_action": action,
            "pass_number": number,
            "topic": entry["id"],
            "source": entry["source"],
            "notes": entry["notes"],
            "progress_file": str(entry["progress"]),
        }
        if entry["gaps"] is not None:
            result["gaps_file"] = str(entry["gaps"])
        return result

    next_pass = pass_path(root, number + 1)
    return {
        "next_action": "extract_gaps",
        "completed_pass": number,
        "progress_directory": str(pass_directory / "progress"),
        "gaps_directory": str(next_pass / "gaps"),
    }


def initialize_pass(
    root: Path,
    number: int,
    assessment_emphasis: str | None,
    question_types: list[str] | None,
    response_format: str,
) -> dict[str, Any]:
    if number < 2:
        raise ValueError("Pass 1 must be initialized by test-prep-setup")
    topic_entries, manifest = entries(root, number)
    if manifest is None or manifest["assessment_count"] == 0:
        raise ValueError(f"Pass {number} has no gap targets")
    created: list[str] = []
    for entry in topic_entries:
        progress = entry["progress"]
        if progress.exists():
            manager("validate", "--file", str(progress))
            continue
        preference_arguments = ["--response-format", response_format]
        if assessment_emphasis is not None:
            preference_arguments.extend(
                ("--assessment-emphasis", assessment_emphasis)
            )
        elif not question_types:
            preference_arguments.extend(
                ("--assessment-emphasis", DEFAULT_ASSESSMENT_EMPHASIS)
            )
        for question_type in question_types or []:
            preference_arguments.extend(("--question-type", question_type))
        manager(
            "init",
            "--file",
            str(progress),
            "--source",
            entry["source"],
            "--notes",
            entry["notes"],
            *preference_arguments,
        )
        created.append(str(progress))
    return {"ok": True, "pass_number": number, "created": created}


def main() -> None:
    args = parser().parse_args()
    if args.command == "status":
        result = status(args.root)
    else:
        result = initialize_pass(
            args.root,
            args.pass_number,
            args.assessment_emphasis,
            args.question_type,
            args.response_format,
        )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
