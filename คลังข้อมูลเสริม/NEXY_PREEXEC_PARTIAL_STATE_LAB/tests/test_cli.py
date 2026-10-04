from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from nexy_pepsa.cli import main


class CliTests(unittest.TestCase):
    def _write(self, root: Path, name: str, value: dict) -> Path:
        path = root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_ready_returns_zero_and_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = self._write(
                root,
                "plan.json",
                {
                    "plan_id": "read",
                    "steps": [{"id": "r", "kind": "READ", "resource": "x", "boundary": "B"}],
                },
            )
            policy = self._write(
                root,
                "policy.json",
                {"policy_id": "p", "allowed_boundaries": ["B"], "protected_resources": []},
            )
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main(["analyze", "--plan", str(plan), "--policy", str(policy)])
            self.assertEqual(code, 0)
            payload = json.loads(out.getvalue())
            self.assertEqual(payload["verdict"], "READY")

    def test_freeze_returns_two(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = self._write(
                root,
                "plan.json",
                {
                    "plan_id": "write",
                    "steps": [
                        {
                            "id": "w",
                            "kind": "UPDATE",
                            "resource": "protected:x",
                            "boundary": "B",
                            "reversible": True,
                            "rollback_strategy": "restore",
                            "postcondition": "changed",
                            "evidence_required": ["E1_STATIC"],
                        }
                    ],
                },
            )
            policy = self._write(
                root,
                "policy.json",
                {"policy_id": "p", "allowed_boundaries": ["B"], "protected_resources": ["protected:*"]},
            )
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main(["analyze", "--plan", str(plan), "--policy", str(policy)])
            self.assertEqual(code, 2)
            payload = json.loads(out.getvalue())
            self.assertEqual(payload["verdict"], "FREEZE")

    def test_invalid_input_returns_three_and_stderr(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bad_plan = root / "plan.json"
            bad_plan.write_text('{"plan_id":"x","steps":[],"float":0.1}', encoding="utf-8")
            policy = self._write(
                root,
                "policy.json",
                {"policy_id": "p", "allowed_boundaries": ["B"], "protected_resources": []},
            )
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = main(["analyze", "--plan", str(bad_plan), "--policy", str(policy)])
            self.assertEqual(code, 3)
            payload = json.loads(err.getvalue())
            self.assertEqual(payload["status"], "INVALID_INPUT")


if __name__ == "__main__":
    unittest.main()
