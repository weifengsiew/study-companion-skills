#!/usr/bin/env python3
"""Create immutable per-topic gap manifests from a completed pass directory."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from extract_gaps import build_result, write_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("progress_directory", type=Path)
    parser.add_argument("gaps_directory", type=Path)
    return parser.parse_args()


def load_result(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return build_result(json.load(handle), path)


def output_name(progress_path: Path) -> str:
    suffix = "-progress.json"
    if not progress_path.name.endswith(suffix):
        raise ValueError(f"unexpected progress filename: {progress_path.name}")
    return f"{progress_path.name[:-len(suffix)]}-gaps.json"


def main() -> None:
    args = parse_args()
    source_directory = args.progress_directory
    output_directory = args.gaps_directory

    if not source_directory.is_dir():
        raise FileNotFoundError(f"progress directory does not exist: {source_directory}")
    if output_directory.exists():
        raise FileExistsError(
            f"gaps directory already exists; refusing to replace it: {output_directory}"
        )
    if source_directory.resolve() == output_directory.resolve():
        raise ValueError("gaps directory must differ from the progress directory")

    progress_paths = sorted(source_directory.glob("*-progress.json"))
    if not progress_paths:
        raise ValueError(f"no *-progress.json files found in {source_directory}")

    extracted = [(path, load_result(path)) for path in progress_paths]
    retained = [(path, result) for path, result in extracted if result["assessment_count"]]
    manifest_files = [
        {
            "source_progress": str(path),
            "gaps_file": output_name(path),
            "assessment_count": result["assessment_count"],
            "gap_count": result["gap_count"],
        }
        for path, result in retained
    ]
    manifest = {
        "schema_version": 1,
        "source_progress_directory": str(source_directory),
        "progress_file_count": len(progress_paths),
        "topic_count": len(retained),
        "assessment_count": sum(item["assessment_count"] for item in manifest_files),
        "gap_count": sum(item["gap_count"] for item in manifest_files),
        "files": manifest_files,
    }

    output_directory.parent.mkdir(parents=True, exist_ok=True)
    temporary_directory = Path(
        tempfile.mkdtemp(
            prefix=f".{output_directory.name}.", dir=output_directory.parent
        )
    )
    try:
        for path, result in retained:
            rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
            write_output(
                temporary_directory / output_name(path), rendered, force=False
            )
        write_output(
            temporary_directory / "_manifest.json",
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            force=False,
        )
        os.replace(temporary_directory, output_directory)
    except Exception:
        shutil.rmtree(temporary_directory, ignore_errors=True)
        raise

    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
