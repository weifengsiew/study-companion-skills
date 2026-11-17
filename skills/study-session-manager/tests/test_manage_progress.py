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
                "session_status",
                "pending_assessment",
                "assessment_history",
                "session_preferences",
            ],
        )
        self.assertIsNone(state["pending_assessment"])
        self.assertEqual(state["session_status"], "not_started")
        self.assertEqual(state["assessment_history"], [])

    def test_init_uses_supplied_progress_path_exactly(self) -> None:
        supplied_progress = (
            self.root
            / "Test-1-Prep"
            / "progress"
            / "L2"
            / "04_improve_retrieval-progress.json"
        )
        output = self.run_cli(
            "init",
            "--file",
            str(supplied_progress),
            "--source",
            str(self.source),
            "--notes",
            str(self.notes),
            "--assessment-emphasis",
            "conceptual understanding",
            "--response-format",
            "short answer",
        )

        self.assertEqual(output["file"], str(supplied_progress))
        self.assertTrue(supplied_progress.is_file())
        self.assertFalse(self.progress.exists())

    def test_question_types_derive_and_persist_balanced_emphasis(self) -> None:
        output = self.run_cli(
            "init",
            "--source",
            str(self.source),
            "--notes",
            str(self.notes),
            "--question-type",
            "recall",
            "--question-type",
            "code or result tracing",
            "--response-format",
            "mix",
        )
        self.assertEqual(output["summary"]["session_status"], "not_started")
        preferences = self.run_cli("show", "--file", str(self.progress))["state"][
            "session_preferences"
        ]
        self.assertEqual(preferences["assessment_emphasis"], "balanced mix")
        self.assertEqual(
            preferences["question_types"], ["recall", "code or result tracing"]
        )

    def test_legacy_preferences_gain_default_question_types(self) -> None:
        self.initialize()
        state = json.loads(self.progress.read_text(encoding="utf-8"))
        del state["session_preferences"]["question_types"]
        self.progress.write_text(json.dumps(state), encoding="utf-8")

        shown = self.run_cli("show", "--file", str(self.progress))["state"]
        self.assertEqual(
            shown["session_preferences"]["question_types"],
            [
                "recall",
                "explanation",
                "comparison",
                "transfer",
            ],
        )

    def test_legacy_note_review_queue_is_dropped_on_next_write(self) -> None:
        self.initialize()
        state = json.loads(self.progress.read_text(encoding="utf-8"))
        state["note_review_queue"] = [
            {
                "learning_objective": "Legacy objective",
                "note_location": "## Legacy location",
                "confirmed_explanation": None,
            }
        ]
        self.progress.write_text(json.dumps(state), encoding="utf-8")

        self.run_cli(
            "set-preferences",
            "--file",
            str(self.progress),
            "--assessment-emphasis",
            "balanced mix",
            "--response-format",
            "mix",
        )

        migrated = json.loads(self.progress.read_text(encoding="utf-8"))
        self.assertNotIn("note_review_queue", migrated)

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

    def test_question_and_answer_transition(self) -> None:
        self.initialize()
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
                "session_status": "active",
                "has_pending_assessment": False,
                "assessment_count": 1,
            },
        )
        state = self.run_cli("show", "--file", str(self.progress))["state"]
        self.assertIsNone(state["pending_assessment"])
        self.assertEqual(len(state["assessment_history"]), 1)
        self.assertEqual(state["assessment_history"][0]["assessment"], "partially_correct")

    def test_complete_transition_requires_no_pending_assessment(self) -> None:
        self.initialize()
        not_started = self.run_cli(
            "complete", "--file", str(self.progress), expected_code=1
        )
        self.assertIn("has not started", not_started["errors"][0])
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
        refused = self.run_cli(
            "complete", "--file", str(self.progress), expected_code=1
        )
        self.assertIn("pending assessment", refused["errors"][0])
        self.run_cli(
            "record-answer",
            "--file",
            str(self.progress),
            "--answer",
            "Answer",
            "--assessment",
            "correct",
        )
        completed = self.run_cli("complete", "--file", str(self.progress))
        self.assertEqual(completed["summary"]["session_status"], "complete")

        refused_question = self.run_cli(
            "set-pending",
            "--file",
            str(self.progress),
            "--question",
            "Another question",
            "--source-citation",
            "Source section",
            "--notes-citation",
            "Notes section",
            expected_code=1,
        )
        self.assertIn("completed session", refused_question["errors"][0])

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

    def test_clarifications_persist_without_recording_and_rephrasing_is_free(self) -> None:
        self.initialize()
        self.run_cli(
            "set-pending",
            "--file",
            str(self.progress),
            "--question",
            "Original question",
            "--source-citation",
            "Source section",
            "--notes-citation",
            "Notes section",
        )
        self.run_cli(
            "replace-question",
            "--file",
            str(self.progress),
            "--question",
            "Clearer question",
        )
        for index in range(6):
            self.run_cli(
                "add-clarification",
                "--file",
                str(self.progress),
                "--response",
                f"Incomplete response {index}",
                "--prompt",
                f"Neutral prompt {index}",
            )
        state = self.run_cli("show", "--file", str(self.progress))["state"]
        pending = state["pending_assessment"]
        self.assertEqual(pending["question"], "Clearer question")
        self.assertEqual(pending["clarification_count"], 6)
        self.assertEqual(state["assessment_history"], [])

        exhausted = self.run_cli(
            "add-clarification",
            "--file",
            str(self.progress),
            "--response",
            "Still incomplete",
            "--prompt",
            "Another prompt",
            expected_code=1,
        )
        self.assertIn("six-prompt", exhausted["errors"][0])

        self.run_cli(
            "record-answer",
            "--file",
            str(self.progress),
            "--answer",
            "Final independent answer",
            "--assessment",
            "correct",
        )
        history = self.run_cli("show", "--file", str(self.progress))["state"][
            "assessment_history"
        ]
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["assessment"], "correct")
        self.assertEqual(history[0]["gaps"], [])
        self.assertIn("Incomplete response 0", history[0]["answer"])
        self.assertIn("Final independent answer", history[0]["answer"])

    def test_latest_assessment_can_be_corrected_with_audit_trail(self) -> None:
        self.initialize()
        self.run_cli(
            "set-pending",
            "--file",
            str(self.progress),
            "--question",
            "Which rule applies?",
            "--source-citation",
            "Source section",
            "--notes-citation",
            "Notes section",
        )
        self.run_cli(
            "record-answer",
            "--file",
            str(self.progress),
            "--answer",
            "The learner's original answer",
            "--assessment",
            "incorrect",
            "--gap",
            "Applied the wrong rule.",
        )
        self.run_cli(
            "revise-latest",
            "--file",
            str(self.progress),
            "--rationale",
            "The cited exception applies under the stated condition.",
            "--reason",
            "The question was ambiguous and the original answer was valid.",
        )
        latest = self.run_cli("show", "--file", str(self.progress))["state"][
            "assessment_history"
        ][-1]
        self.assertEqual(latest["assessment"], "correct")
        self.assertEqual(latest["gaps"], [])
        self.assertEqual(len(latest["revisions"]), 1)
        self.assertEqual(
            latest["revisions"][0]["previous_gaps"], ["Applied the wrong rule."]
        )

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
