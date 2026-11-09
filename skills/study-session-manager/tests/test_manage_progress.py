from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "manage_progress.py"


class ManageProgressCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.notes = self.root / "notes" / "topic-notes.md"
        self.source = self.root / "source.ipynb"
        self.notes.parent.mkdir(parents=True)
        self.notes.write_text("# Notes\n", encoding="utf-8")
        self.source.write_text("{}\n", encoding="utf-8")
        self.progress = self.notes.parent / "progress" / "topic-notes-progress.json"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_cli(self, *arguments: str, expected_code: int = 0) -> dict:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            expected_code,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        output = result.stdout if expected_code == 0 else result.stderr
        return json.loads(output)

    def initialize(self) -> dict:
        return self.run_cli(
            "init",
            "--source",
            str(self.source),
            "--notes",
            str(self.notes),
            "--assessment-emphasis",
            "conceptual understanding",
            "--response-format",
            "short answer",
        )

    def test_init_creates_complete_canonical_state(self) -> None:
        output = self.initialize()
        self.assertEqual(output["file"], str(self.progress))
        state = json.loads(self.progress.read_text(encoding="utf-8"))
        self.assertEqual(
            list(state),
            [
                "source",
                "notes",
                "pending_assessment",
                "assessment_history",
                "session_preferences",
                "note_review_queue",
            ],
        )
        self.assertIsNone(state["pending_assessment"])
        self.assertEqual(state["assessment_history"], [])
        self.assertEqual(state["note_review_queue"], [])

    def test_schema_exposes_types_keys_and_allowed_values(self) -> None:
        output = self.run_cli("schema")
        self.assertIn("pending_assessment", output["required_keys"]["progress"])
        self.assertEqual(
            output["field_types"]["pending_assessment"],
            "null or pending_assessment object",
        )
        self.assertEqual(
            output["allowed_values"]["assessment"],
            ["correct", "partially_correct", "incorrect"],
        )

    def test_init_refuses_to_overwrite(self) -> None:
        self.initialize()
        output = self.run_cli(
            "init",
            "--source",
            str(self.source),
            "--notes",
            str(self.notes),
            "--assessment-emphasis",
            "balanced mix",
            "--response-format",
            "mix",
            expected_code=1,
        )
        self.assertIn("refusing to overwrite", output["errors"][0])

    def test_question_and_answer_transition_preserves_review_queue(self) -> None:
        self.initialize()
        self.run_cli(
            "enqueue-review",
            "--file",
            str(self.progress),
            "--learning-objective",
            "Explain regularization",
            "--note-location",
            "## Regularization",
        )
        self.run_cli(
            "set-pending",
            "--file",
            str(self.progress),
            "--question",
            "Why does regularization help?",
            "--source-citation",
            "Section 4.2",
            "--notes-citation",
            "## Regularization",
        )
        output = self.run_cli(
            "record-answer",
            "--file",
            str(self.progress),
            "--answer",
            "It reduces model complexity.",
            "--assessment",
            "partially_correct",
            "--gap",
            "Did not explain the penalty mechanism.",
        )
        self.assertNotIn("state", output)
        self.assertEqual(
            output["summary"],
            {
                "has_pending_assessment": False,
                "assessment_count": 1,
                "note_review_count": 1,
            },
        )
        state = self.run_cli("show", "--file", str(self.progress))["state"]
        self.assertIsNone(state["pending_assessment"])
        self.assertEqual(len(state["assessment_history"]), 1)
        self.assertEqual(state["assessment_history"][0]["assessment"], "partially_correct")
        self.assertEqual(len(state["note_review_queue"]), 1)

    def test_validate_rejects_unknown_keys(self) -> None:
        self.initialize()
        state = json.loads(self.progress.read_text(encoding="utf-8"))
        state["completed_topics"] = []
        self.progress.write_text(json.dumps(state), encoding="utf-8")
        output = self.run_cli(
            "validate", "--file", str(self.progress), expected_code=1
        )
        self.assertIn("Unknown key: progress.completed_topics", output["errors"])

    def test_non_correct_answer_requires_gap(self) -> None:
        self.initialize()
        self.run_cli(
            "set-pending",
            "--file",
            str(self.progress),
            "--question",
            "Question",
            "--source-citation",
            "Source section",
            "--notes-citation",
            "Notes section",
        )
        output = self.run_cli(
            "record-answer",
            "--file",
            str(self.progress),
            "--answer",
            "Answer",
            "--assessment",
            "incorrect",
            expected_code=1,
        )
        self.assertIn("requires at least one gap", output["errors"][0])

    def test_clear_reviews_removes_exact_prefix(self) -> None:
        self.initialize()
        for index in range(3):
            self.run_cli(
                "enqueue-review",
                "--file",
                str(self.progress),
                "--learning-objective",
                f"Objective {index}",
                "--note-location",
                f"## Location {index}",
            )
        output = self.run_cli(
            "clear-reviews", "--file", str(self.progress), "--count", "2"
        )
        self.assertNotIn("state", output)
        self.assertEqual(output["summary"]["note_review_count"], 1)
        queue = self.run_cli("show", "--file", str(self.progress))["state"][
            "note_review_queue"
        ]
        self.assertEqual([entry["learning_objective"] for entry in queue], ["Objective 2"])

    def test_mutations_return_compact_summary_and_show_returns_full_state(self) -> None:
        init_output = self.initialize()
        self.assertNotIn("state", init_output)
        self.assertEqual(init_output["summary"]["assessment_count"], 0)

        pending_output = self.run_cli(
            "set-pending",
            "--file",
            str(self.progress),
            "--question",
            "Question",
            "--source-citation",
            "Source section",
            "--notes-citation",
            "Notes section",
        )
        self.assertNotIn("state", pending_output)
        self.assertTrue(pending_output["summary"]["has_pending_assessment"])

        show_output = self.run_cli("show", "--file", str(self.progress))
        self.assertIn("state", show_output)
        self.assertNotIn("summary", show_output)


if __name__ == "__main__":
    unittest.main()
