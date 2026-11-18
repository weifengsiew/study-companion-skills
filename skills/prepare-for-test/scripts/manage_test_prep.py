#!/usr/bin/env python3
"""Inspect test-prep state and initialize targeted passes."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILLS = Path(__file__).parents[2]
PROGRESS_MANAGER = SKILLS / "study-session-manager/scripts/manage_progress.py"
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
    initialize.add_argument("--topic", required=True)
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


def pass_path(root: Path, topic_id: str, number: int) -> Path:
    return root / "progress" / topic_id / f"pass_{number:02d}"


def status(root: Path) -> dict[str, Any]:
    plan = load_json(root / "test-plan.json")
    for topic in plan["topics"]:
        number = 1
        while True:
            directory = pass_path(root, topic["id"], number)
            progress = directory / "progress.json"
            gaps = None if number == 1 else directory / "gaps.json"
            if not progress.is_file():
                return {
                    "next_action": "setup_required" if number == 1 else "initialize_pass",
                    "pass_number": number,
                    "topic": topic["id"],
                }

            state = manager("show", "--file", str(progress))["state"]
            session_status = state["session_status"]
            if session_status != "complete":
                if state["pending_assessment"] is not None:
                    action = "resume_pending"
                elif session_status == "active":
                    action = "resume_quiz"
                else:
                    action = "start_quiz"
                result = {
                    "next_action": action,
                    "pass_number": number,
                    "topic": topic["id"],
                    "source": topic["source"],
                    "notes": topic["notes"],
                    "progress_file": str(progress),
                }
                if gaps is not None:
                    result["gaps_file"] = str(gaps)
                return result

            target = pass_path(root, topic["id"], number + 1) / "gaps.json"
            if not target.is_file():
                return {
                    "next_action": "extract_gaps",
                    "topic": topic["id"],
                    "completed_pass": number,
                    "target_pass": number + 1,
                    "progress_file": str(progress),
                    "gaps_file": str(target),
                }
            if load_json(target)["assessment_count"] == 0:
                break
            number += 1

    return {"next_action": "workflow_complete"}


def initialize_pass(
    root: Path,
    number: int,
    topic_id: str,
    assessment_emphasis: str | None,
    question_types: list[str] | None,
    response_format: str,
) -> dict[str, Any]:
    if number < 2:
        raise ValueError("Pass 1 must be initialized by test-prep-setup")
    plan = load_json(root / "test-plan.json")
    topic = next((item for item in plan["topics"] if item["id"] == topic_id), None)
    if topic is None:
        raise ValueError(f"Unknown topic: {topic_id}")
    directory = pass_path(root, topic_id, number)
    gaps = directory / "gaps.json"
    if not gaps.is_file() or load_json(gaps)["assessment_count"] == 0:
        raise ValueError(f"Pass {number} has no gap targets for {topic_id}")
    progress = directory / "progress.json"
    if progress.exists():
        manager("validate", "--file", str(progress))
        return {"ok": True, "pass_number": number, "topic": topic_id, "created": []}
    preference_arguments = ["--response-format", response_format]
    if assessment_emphasis is not None:
        preference_arguments.extend(("--assessment-emphasis", assessment_emphasis))
    elif not question_types:
        preference_arguments.extend(("--assessment-emphasis", DEFAULT_ASSESSMENT_EMPHASIS))
    for question_type in question_types or []:
        preference_arguments.extend(("--question-type", question_type))
    manager(
        "init", "--file", str(progress), "--source", topic["source"],
        "--notes", topic["notes"], *preference_arguments,
    )
    return {"ok": True, "pass_number": number, "topic": topic_id, "created": [str(progress)]}


def main() -> None:
    args = parser().parse_args()
    if args.command == "status":
        result = status(args.root)
    else:
        result = initialize_pass(
            args.root,
            args.pass_number,
            args.topic,
            args.assessment_emphasis,
            args.question_type,
            args.response_format,
        )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
