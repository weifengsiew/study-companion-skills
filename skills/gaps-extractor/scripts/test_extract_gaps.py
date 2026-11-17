#!/usr/bin/env python3
"""Tests for extract_gaps.py."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("extract_gaps.py")


class ExtractGapsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.progress = self.root / "lesson-progress.json"
        self.records = [
            {
                "question": "What is regularization?",
                "answer": "It makes a model smaller.",
                "assessment": "partially_correct",
                "gaps": ["Did not explain the penalty mechanism."],
                "citations": {"source": ["4.2"], "notes": ["Regularization"]},
            },
            {
                "question": "What does the penalty discourage?",
                "answer": "Excessively large weights.",
                "assessment": "correct",
                "gaps": [],
                "citations": {"source": ["4.2"], "notes": ["Regularization"]},
            },
        ]
        self.progress.write_text(
            json.dumps(
                {
                    "source": "lesson.md",
                    "notes": "notes/lesson-notes.md",
                    "assessment_history": self.records,
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_cli(self, *arguments: str, expected_code: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["python3", str(SCRIPT), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected_code, result.stderr)
        return result

    def test_prints_only_assessments_with_gaps(self) -> None:
        result = self.run_cli(str(self.progress))
        extracted = json.loads(result.stdout)
        self.assertEqual(extracted["assessment_count"], 1)
        self.assertEqual(extracted["gap_count"], 1)
        self.assertEqual(extracted["assessment_history"], [self.records[0]])
        self.assertEqual(extracted["source_progress"], str(self.progress))

    def test_writes_output_and_refuses_unapproved_replacement(self) -> None:
        output = self.root / "lesson-progress-gaps.json"
        result = self.run_cli(str(self.progress), "--output", str(output))
        summary = json.loads(result.stdout)
        self.assertEqual(summary["assessment_count"], 1)
        self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["assessment_count"], 1)

        refused = self.run_cli(
            str(self.progress), "--output", str(output), expected_code=1
        )
        self.assertIn("output already exists", refused.stderr)

    def test_rejects_non_object_progress(self) -> None:
        self.progress.write_text("[]", encoding="utf-8")
        result = self.run_cli(str(self.progress), expected_code=1)
        self.assertIn("progress file must contain a JSON object", result.stderr)

    def test_refuses_to_replace_input(self) -> None:
        result = self.run_cli(
            str(self.progress), "--output", str(self.progress), "--force", expected_code=1
        )
        self.assertIn("output path must differ", result.stderr)

    def test_corrected_assessment_does_not_propagate_old_gap(self) -> None:
        corrected = self.records[0]
        corrected["assessment"] = "correct"
        corrected["gaps"] = []
        corrected["revisions"] = [
            {
                "previous_assessment": "partially_correct",
                "previous_gaps": ["Did not explain the penalty mechanism."],
                "rationale": "The learner justified the mechanism.",
                "reason": "The original grading was too strict.",
            }
        ]
        self.progress.write_text(
            json.dumps(
                {
                    "source": "lesson.md",
                    "notes": "notes/lesson-notes.md",
                    "assessment_history": [corrected],
                }
            ),
            encoding="utf-8",
        )
        extracted = json.loads(self.run_cli(str(self.progress)).stdout)
        self.assertEqual(extracted["assessment_count"], 0)
        self.assertEqual(extracted["gap_count"], 0)


if __name__ == "__main__":
    unittest.main()
