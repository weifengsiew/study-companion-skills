#!/usr/bin/env python3
"""Tests for manage_test_plan.py."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("manage_test_plan.py")


class ManageTestPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        base = Path(self.temporary_directory.name)
        self.root = base / "test-prep"
        self.topics = base / "provided-topics.md"
        self.source = base / "source.md"
        self.notes = base / "notes.md"
        self.topics.write_text("# Test Topics\n", encoding="utf-8")
        self.source.write_text("source", encoding="utf-8")
        self.notes.write_text("notes", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_cli(
        self, *arguments: str, expected_code: int = 0
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["python3", str(SCRIPT), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected_code, result.stderr)
        return result

    def init_arguments(self) -> tuple[str, ...]:
        return (
            "init",
            "--root",
            str(self.root),
            "--topics-file",
            str(self.topics),
            "--question-type",
            "recall",
            "--question-type",
            "code or result tracing",
            "--response-format",
            "short answer",
            "--topic",
            "topic-01",
            str(self.source),
            str(self.notes),
        )

    def test_creates_and_checks_workspace(self) -> None:
        plan = json.loads(self.run_cli(*self.init_arguments()).stdout)
        self.assertEqual(plan["topics_file"], str(self.root / "test-topics.md"))
        self.assertEqual((self.root / "test-topics.md").read_text(), "# Test Topics\n")
        progress = self.root / "progress/topic-01/pass_01/progress.json"
        state = json.loads(progress.read_text())
        self.assertEqual(state["session_status"], "not_started")
        self.assertEqual(
            state["session_preferences"]["question_types"],
            ["recall", "code or result tracing"],
        )
        checked = self.run_cli("check", "--root", str(self.root))
        self.assertEqual(json.loads(checked.stdout), plan)

    def test_uses_balanced_short_answer_defaults(self) -> None:
        arguments = list(self.init_arguments())
        question_start = arguments.index("--question-type")
        topic_start = arguments.index("--topic")
        del arguments[question_start:topic_start]
        self.run_cli(*arguments)
        progress = self.root / "progress/topic-01/pass_01/progress.json"
        preferences = json.loads(progress.read_text())["session_preferences"]
        self.assertEqual(preferences["assessment_emphasis"], "balanced mix")
        self.assertEqual(preferences["response_format"], "short answer")
        self.assertEqual(preferences["question_types"], [
            "recall",
            "explanation",
            "comparison",
            "transfer",
            "code or command interpretation",
            "code or result tracing",
            "workflow sequencing",
            "diagnosis and troubleshooting",
        ])

    def test_refuses_existing_setup(self) -> None:
        self.run_cli(*self.init_arguments())
        result = self.run_cli(*self.init_arguments(), expected_code=1)
        self.assertIn("refusing to replace", result.stderr)

    def test_uses_topics_file_already_at_root(self) -> None:
        self.root.mkdir()
        canonical = self.root / "test-topics.md"
        canonical.write_text("# Existing Test Topics\n", encoding="utf-8")
        arguments = list(self.init_arguments())
        arguments[arguments.index(str(self.topics))] = str(canonical)
        plan = json.loads(self.run_cli(*arguments).stdout)
        self.assertEqual(plan["topics_file"], str(canonical))
        self.assertEqual(canonical.read_text(), "# Existing Test Topics\n")

    def test_rejects_duplicate_ids(self) -> None:
        result = self.run_cli(
            *self.init_arguments(),
            "--topic",
            "topic-01",
            str(self.source),
            str(self.notes),
            expected_code=1,
        )
        self.assertIn("duplicate topic id", result.stderr)
        self.assertFalse(self.root.exists())

    def test_rejects_inaccessible_material(self) -> None:
        self.source.unlink()
        result = self.run_cli(*self.init_arguments(), expected_code=1)
        self.assertIn("source is not readable", result.stderr)
        self.assertFalse(self.root.exists())


if __name__ == "__main__":
    unittest.main()
