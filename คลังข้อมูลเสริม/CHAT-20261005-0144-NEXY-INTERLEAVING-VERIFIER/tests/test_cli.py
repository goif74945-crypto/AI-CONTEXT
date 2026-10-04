from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from interleaving_verifier.cli import main


class CliTests(unittest.TestCase):
    def _run(self, payload):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "plan.json"
            if isinstance(payload, str):
                path.write_text(payload, encoding="utf-8")
            else:
                path.write_text(json.dumps(payload), encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                code = main([str(path)])
            text = output.getvalue().strip()
            return code, json.loads(text) if text else None

    def test_pass_exit_zero(self):
        code, report = self._run({
            "schema_version": "1.0",
            "initial_state": {"x": 0},
            "actions": [{"id": "A", "effects": [{"op": "add", "path": "/x", "value": 1}]}],
        })
        self.assertEqual(code, 0)
        self.assertEqual(report["verification_status"], "PASS")

    def test_counterexample_exit_two(self):
        code, report = self._run({
            "schema_version": "1.0",
            "initial_state": {"x": 0},
            "actions": [
                {"id": "A", "effects": [{"op": "set", "path": "/x", "value": 1}]},
                {"id": "B", "effects": [{"op": "set", "path": "/x", "value": 2}]},
            ],
        })
        self.assertEqual(code, 2)
        self.assertEqual(report["decision"], "DIVERGENT_TERMINAL_STATE")

    def test_model_freeze_exit_four(self):
        code, report = self._run({"schema_version": "1.0", "initial_state": {}, "actions": []})
        self.assertEqual(code, 4)
        self.assertEqual(report["decision"], "FREEZE_INVALID_INPUT")

    def test_malformed_json_exit_three(self):
        code, report = self._run("{broken")
        self.assertEqual(code, 3)
        self.assertEqual(report["decision"], "FREEZE_IO_OR_JSON")

    def test_output_file_round_trip(self):
        with tempfile.TemporaryDirectory() as td:
            input_path = Path(td) / "plan.json"
            output_path = Path(td) / "report.json"
            input_path.write_text(json.dumps({
                "schema_version": "1.0",
                "initial_state": {"x": 0},
                "actions": [{"id": "A", "effects": [{"op": "set", "path": "/x", "value": 1}]}],
            }), encoding="utf-8")
            code = main([str(input_path), "--output", str(output_path), "--pretty"])
            self.assertEqual(code, 0)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(report["decision"], "CONFLUENT")


if __name__ == "__main__":
    unittest.main()
