#!/usr/bin/env python3
"""Extract assessment-history records that contain one or more gaps."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Keep only assessment records with non-empty gaps."
    )
    parser.add_argument("progress_file", type=Path, help="Input progress JSON file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional output JSON file; otherwise print the filtered JSON",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing output file",
    )
    return parser.parse_args()


def has_gap(record: object) -> bool:
    if not isinstance(record, dict):
        return False
    gaps = record.get("gaps")
    return isinstance(gaps, list) and any(
        isinstance(gap, str) and gap.strip() for gap in gaps
    )


def build_result(progress: Any, input_path: Path) -> dict[str, Any]:
    if not isinstance(progress, dict):
        raise ValueError("progress file must contain a JSON object")
    history = progress.get("assessment_history")
    if not isinstance(history, list):
        raise ValueError("progress file must contain an assessment_history list")

    retained = [record for record in history if has_gap(record)]
    gap_count = sum(len(record["gaps"]) for record in retained)
    return {
        "schema_version": 1,
        "source": progress.get("source", ""),
        "notes": progress.get("notes", ""),
        "source_progress": str(input_path),
        "assessment_count": len(retained),
        "gap_count": gap_count,
        "assessment_history": retained,
    }


def write_output(path: Path, rendered: str, *, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"output already exists: {path}; pass --force to replace it")
    if not path.parent.is_dir():
        raise FileNotFoundError(f"output directory does not exist: {path.parent}")

    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    finally:
        if temporary_name is not None:
            temporary_path = Path(temporary_name)
            if temporary_path.exists():
                temporary_path.unlink()


def main() -> None:
    args = parse_args()
    input_path = args.progress_file
    if args.output and input_path.resolve() == args.output.resolve():
        raise ValueError("output path must differ from the input progress file")

    with input_path.open(encoding="utf-8") as handle:
        progress = json.load(handle)

    result = build_result(progress, input_path)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        write_output(args.output, rendered, force=args.force)
        print(
            json.dumps(
                {
                    "input": str(input_path),
                    "output": str(args.output),
                    "assessment_count": result["assessment_count"],
                    "gap_count": result["gap_count"],
                }
            )
        )
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
