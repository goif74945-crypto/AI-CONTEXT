import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def run_cli(self, args, payload):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "input.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            env = dict(os.environ)
            env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
            proc = subprocess.run([sys.executable, "-m", "nexy_aux.cli", *args, str(path)] if args[0] != "distill-risk" else [sys.executable, "-m", "nexy_aux.cli", "distill-risk", str(path), args[1]], capture_output=True, text=True, env=env, check=False)
            return proc, json.loads(proc.stdout)

    def test_compose_cli(self):
        proc, out = self.run_cli(["compose"], {"initial_facts": ["root"], "components": [{"id": "x", "assumptions": ["root"], "guarantees": ["ok"]}]})
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(out["status"], "PASS")

    def test_risk_cli_returns_nonzero_on_freeze(self):
        proc, out = self.run_cli(["risk"], {"artifacts": {"x": ["SECRET"]}, "steps": [{"id": "s", "consumes": ["x"], "produces": [], "capabilities": ["EXTERNAL_EGRESS"]}]})
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(out["status"], "FREEZE")


    def test_portability_reverify_is_nonzero_gate(self):
        payload = {
            "evidence": {
                "claim_id": "C",
                "evidence_class": "E2",
                "source_context": {"runtime": "A"},
            },
            "target": {
                "claim_id": "C",
                "required_evidence_classes": ["E2"],
                "target_context": {"runtime": "B"},
            },
            "policy": {"runtime": "REVERIFY_IF_DIFFERENT"},
        }
        proc, out = self.run_cli(["portability"], payload)
        self.assertEqual(out["status"], "REVERIFY")
        self.assertEqual(proc.returncode, 2)

    def test_cli_input_error_is_machine_readable_freeze(self):
        proc, out = self.run_cli(["compose"], {"components": "not-a-list"})
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(out["status"], "FREEZE")
        self.assertEqual(out["reason"], "INPUT_ERROR")
        self.assertIn("fingerprint", out)

    def test_distill_risk_cli(self):
        payload = {"artifacts": {"x": ["SECRET"]}, "steps": [
            {"id": "copy", "consumes": ["x"], "produces": ["y"], "capabilities": []},
            {"id": "send", "consumes": ["y"], "produces": [], "capabilities": ["EXTERNAL_EGRESS"]},
        ]}
        proc, out = self.run_cli(["distill-risk", "E_SECRET_EGRESS"], payload)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(out["minimal_size"], 2)


if __name__ == "__main__":
    unittest.main()
