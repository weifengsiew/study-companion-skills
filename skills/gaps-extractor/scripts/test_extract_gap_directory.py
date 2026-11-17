#!/usr/bin/env python3
"""Tests for extract_gap_directory.py."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("extract_gap_directory.py")


def progress(history: list[dict[str, object]], topic: str) -> dict[str, object]:
    return {
        "source": f"{topic}.md",
        "notes": f"notes/{topic}-notes.md",
        "pending_assessment": None,
        "assessment_history": history,
        "session_preferences": {
            "assessment_emphasis": "balanced mix",
            "response_format": "short answer",
        },
    }


def assessment(value: str, gaps: list[str]) -> dict[str, object]:
    return {
        "question": "Explain the mechanism.",
        "answer": "An answer.",
        "assessment": value,
        "gaps": gaps,
        "citations": {"source": ["Section 1"], "notes": ["Mechanism"]},
    }


class ExtractGapDirectoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.input_directory = self.root / "pass_01" / "progress"
        self.input_directory.mkdir(parents=True)
        (self.input_directory / "topic-a-progress.json").write_text(
            json.dumps(progress([assessment("incorrect", ["Missing causal step."])], "a")),
            encoding="utf-8",
        )
        (self.input_directory / "topic-b-progress.json").write_text(
            json.dumps(progress([assessment("correct", [])], "b")),
            encoding="utf-8",
        )
        self.output_directory = self.root / "pass_02" / "gaps"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_cli(self, *, expected_code: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["python3", str(SCRIPT), str(self.input_directory), str(self.output_directory)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected_code, result.stderr)
        return result

    def test_creates_only_gapped_topic_files_and_manifest(self) -> None:
        result = self.run_cli()
        manifest = json.loads(result.stdout)
        self.assertEqual(manifest["progress_file_count"], 2)
        self.assertEqual(manifest["topic_count"], 1)
        self.assertEqual(manifest["assessment_count"], 1)
        self.assertEqual(manifest["gap_count"], 1)
        self.assertTrue((self.output_directory / "topic-a-gaps.json").is_file())
        self.assertFalse((self.output_directory / "topic-b-gaps.json").exists())
        self.assertEqual(
            json.loads((self.output_directory / "_manifest.json").read_text())["files"],
            manifest["files"],
        )

    def test_refuses_to_replace_existing_gap_directory(self) -> None:
        self.output_directory.mkdir(parents=True)
        result = self.run_cli(expected_code=1)
        self.assertIn("refusing to replace", result.stderr)

    def test_zero_gap_pass_creates_terminal_manifest_only(self) -> None:
        (self.input_directory / "topic-a-progress.json").write_text(
            json.dumps(progress([assessment("correct", [])], "a")),
            encoding="utf-8",
        )
        result = self.run_cli()
        manifest = json.loads(result.stdout)
        self.assertEqual(manifest["topic_count"], 0)
        self.assertEqual(manifest["assessment_count"], 0)
        self.assertEqual(manifest["gap_count"], 0)
        self.assertEqual(
            [path.name for path in self.output_directory.iterdir()],
            ["_manifest.json"],
        )


if __name__ == "__main__":
    unittest.main()
