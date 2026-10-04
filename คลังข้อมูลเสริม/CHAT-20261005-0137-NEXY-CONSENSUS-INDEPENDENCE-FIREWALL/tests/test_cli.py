from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_cli_emits_json_and_zero_for_candidate(self) -> None:
        payload = {
            "claim_id": "cli-claim",
            "evidence": [
                {"evidence_id": "r1", "kind": "runtime", "source_identity": "run:a", "parents": [], "correlation_keys": []},
                {"evidence_id": "r2", "kind": "runtime", "source_identity": "run:b", "parents": [], "correlation_keys": []},
            ],
            "votes": [
                {"actor_id": "a", "stance": "SUPPORT", "evidence_ids": ["r1"], "correlation_keys": []},
                {"actor_id": "b", "stance": "SUPPORT", "evidence_ids": ["r2"], "correlation_keys": []},
            ],
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "in.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "ncif.cli", str(path), "--min-support-groups", "2"],
                cwd=ROOT,
                env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "CONSENSUS_CANDIDATE")
        self.assertEqual(out["verification_status"], "NOT_VERIFIED_FINAL_AUTHORITY")

    def test_cli_returns_two_for_freeze(self) -> None:
        fixture = ROOT / "fixtures" / "correlated_false_consensus.json"
        proc = subprocess.run(
            [sys.executable, "-m", "ncif.cli", str(fixture), "--min-support-groups", "2"],
            cwd=ROOT,
            env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "FREEZE")


if __name__ == "__main__":
    unittest.main()
