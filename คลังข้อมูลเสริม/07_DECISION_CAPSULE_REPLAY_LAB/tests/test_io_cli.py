from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import authority_refs


class CliTests(unittest.TestCase):
    def _plan(self) -> dict:
        refs = [r.to_dict() for r in authority_refs()]
        from nexy_dcr.canonical import sha256_hex
        from nexy_dcr.model import authority_fingerprint

        fp = authority_fingerprint(authority_refs())
        return {
            "project_target": "goif74945-crypto/NEXY.AI-",
            "authority_refs": refs,
            "terminal_state": "PASS",
            "events": [
                {"kind": "REQUEST", "payload": {"request_id": "cli-1", "objective": "demo"}},
                {"kind": "CONTEXT_SELECTED", "payload": {"sources": ["spec"]}},
                {"kind": "AUTHORITY_RESOLVED", "payload": {"fingerprint": fp, "mode": "EXPLICIT"}},
                {"kind": "DECISION", "payload": {"decision": "ALLOW"}},
                {"kind": "VERIFICATION", "payload": {"status": "PASS", "claim": "demo"}},
                {
                    "kind": "FINAL",
                    "payload": {
                        "status": "PASS",
                        "output": {"ok": True},
                        "output_digest": sha256_hex({"ok": True}),
                    },
                },
            ],
        }

    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).parents[1] / "src")
        return subprocess.run(
            [sys.executable, "-m", "nexy_dcr.cli", *args],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_compile_verify_and_replay_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan_path = Path(tmp) / "plan.json"
            capsule_path = Path(tmp) / "capsule.json"
            plan_path.write_text(json.dumps(self._plan(), ensure_ascii=False), encoding="utf-8")

            compiled = self._run("compile", str(plan_path), str(capsule_path))
            self.assertEqual(compiled.returncode, 0, compiled.stderr)
            self.assertTrue(capsule_path.exists())

            verified = self._run("verify", str(capsule_path))
            self.assertEqual(verified.returncode, 0, verified.stderr)

            replayed = self._run("replay", str(capsule_path))
            self.assertEqual(replayed.returncode, 0, replayed.stderr)
            self.assertIn('"terminal_state": "PASS"', replayed.stdout)

    def test_cli_rejects_invalid_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan_path = Path(tmp) / "bad.json"
            capsule_path = Path(tmp) / "capsule.json"
            plan = self._plan()
            plan["events"] = [plan["events"][0]]
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            result = self._run("compile", str(plan_path), str(capsule_path))
            self.assertEqual(result.returncode, 1)
            self.assertIn('"status": "FAIL"', result.stderr)


if __name__ == "__main__":
    unittest.main()
