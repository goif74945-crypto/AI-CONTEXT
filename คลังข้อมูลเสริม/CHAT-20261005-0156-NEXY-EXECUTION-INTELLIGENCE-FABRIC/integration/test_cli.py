import json
import subprocess
import sys
import unittest
from pathlib import Path

from integration.test_fabric import safe_payload

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, payload):
        return subprocess.run(
            [sys.executable, "cli.py"],
            cwd=ROOT,
            input=json.dumps(payload),
            text=True,
            capture_output=True,
        )

    def test_ready_exit_code_and_json(self):
        completed = self.run_cli(safe_payload())
        self.assertEqual(completed.returncode, 0)
        body = json.loads(completed.stdout)
        self.assertEqual(body["status"], "READY")

    def test_ask_exit_code(self):
        payload = safe_payload()
        payload["uncertainty"] = {
            "requirements": [{"id": "r", "blocked_by": ["branch"]}],
            "known": [],
            "probes": [{"id": "q", "cost": 1, "resolves": ["branch"], "question": "Which branch?"}],
        }
        completed = self.run_cli(payload)
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(json.loads(completed.stdout)["status"], "ASK")

    def test_invalid_input_fail_closed(self):
        completed = subprocess.run(
            [sys.executable, "cli.py"], cwd=ROOT, input="{bad", text=True, capture_output=True
        )
        self.assertEqual(completed.returncode, 64)
        self.assertEqual(json.loads(completed.stdout)["status"], "FREEZE")


if __name__ == "__main__":
    unittest.main()
