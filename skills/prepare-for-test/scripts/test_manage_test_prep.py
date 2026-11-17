#!/usr/bin/env python3
"""Integration tests for manage_test_prep.py."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("manage_test_prep.py")
SKILLS = Path(__file__).parents[2]
SETUP = SKILLS / "test-prep-setup/scripts/manage_test_plan.py"
PROGRESS = SKILLS / "study-session-manager/scripts/manage_progress.py"
EXTRACT = SKILLS / "gaps-extractor/scripts/extract_gap_directory.py"


class ManageTestPrepTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        base = Path(self.temporary_directory.name)
        self.root = base / "test-prep"
        self.topics = base / "topics.md"
        self.source = base / "source.md"
        self.notes = base / "notes.md"
        self.source_two = base / "source-two.md"
        self.notes_two = base / "notes-two.md"
        self.topics.write_text("# Topics\n", encoding="utf-8")
        self.source.write_text("source", encoding="utf-8")
        self.notes.write_text("notes", encoding="utf-8")
        self.source_two.write_text("source two", encoding="utf-8")
        self.notes_two.write_text("notes two", encoding="utf-8")
        self.run_cli(
            SETUP,
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
            "--topic",
            "topic-02",
            str(self.source_two),
            str(self.notes_two),
        )
        self.progress = self.root / "progress/pass_01/progress/topic-01-progress.json"
        self.progress_two = self.root / "progress/pass_01/progress/topic-02-progress.json"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_cli(self, script: Path, *arguments: str) -> dict:
        result = subprocess.run(
            ["python3", str(script), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def answer_and_complete(
        self, progress: Path, assessment: str, gap: str | None = None
    ) -> None:
        self.run_cli(
            PROGRESS,
            "set-pending",
            "--file",
            str(progress),
            "--question",
            "Explain the concept.",
            "--source-citation",
            "Section 1",
            "--notes-citation",
            "Topic 1",
        )
        arguments = [
            "record-answer",
            "--file",
            str(progress),
            "--answer",
            "Answer",
            "--assessment",
            assessment,
        ]
        if gap:
            arguments.extend(("--gap", gap))
        self.run_cli(PROGRESS, *arguments)
        self.run_cli(PROGRESS, "complete", "--file", str(progress))

    def test_status_resumes_and_advances_first_pass(self) -> None:
        self.assertEqual(
            self.run_cli(SCRIPT, "status", "--root", str(self.root))["next_action"],
            "start_quiz",
        )
        self.run_cli(
            PROGRESS,
            "set-pending",
            "--file",
            str(self.progress),
            "--question",
            "Question",
            "--source-citation",
            "Section 1",
            "--notes-citation",
            "Topic 1",
        )
        self.assertEqual(
            self.run_cli(SCRIPT, "status", "--root", str(self.root))["next_action"],
            "resume_pending",
        )
        self.run_cli(
            PROGRESS,
            "record-answer",
            "--file",
            str(self.progress),
            "--answer",
            "Answer",
            "--assessment",
            "correct",
        )
        self.assertEqual(
            self.run_cli(SCRIPT, "status", "--root", str(self.root))["next_action"],
            "resume_quiz",
        )
        self.run_cli(PROGRESS, "complete", "--file", str(self.progress))
        status = self.run_cli(SCRIPT, "status", "--root", str(self.root))
        self.assertEqual(status["next_action"], "start_quiz")
        self.assertEqual(status["topic"], "topic-02")
        self.answer_and_complete(self.progress_two, "correct")
        self.assertEqual(
            self.run_cli(SCRIPT, "status", "--root", str(self.root))["next_action"],
            "extract_gaps",
        )

    def test_zero_gap_extraction_completes_workflow(self) -> None:
        self.answer_and_complete(self.progress, "correct")
        self.answer_and_complete(self.progress_two, "correct")
        self.run_cli(
            EXTRACT,
            str(self.root / "progress/pass_01/progress"),
            str(self.root / "progress/pass_02/gaps"),
        )
        status = self.run_cli(SCRIPT, "status", "--root", str(self.root))
        self.assertEqual(status["next_action"], "workflow_complete")

    def test_gaps_initialize_targeted_pass(self) -> None:
        self.answer_and_complete(self.progress, "incorrect", "Missing mechanism.")
        self.answer_and_complete(self.progress_two, "correct")
        self.run_cli(
            EXTRACT,
            str(self.root / "progress/pass_01/progress"),
            str(self.root / "progress/pass_02/gaps"),
        )
        status = self.run_cli(SCRIPT, "status", "--root", str(self.root))
        self.assertEqual(status["next_action"], "initialize_pass")
        self.run_cli(
            SCRIPT,
            "init-pass",
            "--root",
            str(self.root),
            "--pass-number",
            "2",
            "--question-type",
            "transfer",
            "--question-type",
            "diagnosis and troubleshooting",
            "--response-format",
            "short answer",
        )
        status = self.run_cli(SCRIPT, "status", "--root", str(self.root))
        self.assertEqual(status["next_action"], "start_quiz")
        self.assertTrue(status["gaps_file"].endswith("topic-01-gaps.json"))
        progress = self.root / "progress/pass_02/progress/topic-01-progress.json"
        preferences = json.loads(progress.read_text())["session_preferences"]
        self.assertEqual(
            preferences["question_types"],
            ["transfer", "diagnosis and troubleshooting"],
        )

    def test_targeted_pass_uses_defaults(self) -> None:
        self.answer_and_complete(self.progress, "incorrect", "Missing mechanism.")
        self.answer_and_complete(self.progress_two, "correct")
        self.run_cli(
            EXTRACT,
            str(self.root / "progress/pass_01/progress"),
            str(self.root / "progress/pass_02/gaps"),
        )
        self.run_cli(
            SCRIPT,
            "init-pass",
            "--root",
            str(self.root),
            "--pass-number",
            "2",
        )
        progress = self.root / "progress/pass_02/progress/topic-01-progress.json"
        preferences = json.loads(progress.read_text())["session_preferences"]
        self.assertEqual(preferences["assessment_emphasis"], "balanced mix")
        self.assertEqual(preferences["response_format"], "short answer")
        self.assertEqual(len(preferences["question_types"]), 8)


if __name__ == "__main__":
    unittest.main()
