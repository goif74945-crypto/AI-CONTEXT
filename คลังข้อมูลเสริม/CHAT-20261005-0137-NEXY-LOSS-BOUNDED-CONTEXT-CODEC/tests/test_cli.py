from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "sample_bundle.json"
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


class CliIntegrationTests(unittest.TestCase):
    def test_compact_then_verify(self) -> None:
        compact = subprocess.run(
            [
                sys.executable, "-m", "lbcc.cli", "compact", str(FIXTURE),
                "--max-bytes", "5000", "--max-loss-ppm", "350000",
            ],
            cwd=ROOT,
            env=ENV,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(compact.stdout)
        self.assertEqual(payload["status"], "PASS")
        with tempfile.TemporaryDirectory() as td:
            result_path = Path(td) / "result.json"
            result_path.write_text(compact.stdout, encoding="utf-8")
            verify = subprocess.run(
                [
                    sys.executable, "-m", "lbcc.cli", "verify", str(FIXTURE), str(result_path),
                    "--max-bytes", "5000", "--max-loss-ppm", "350000",
                ],
                cwd=ROOT,
                env=ENV,
                check=True,
                capture_output=True,
                text=True,
            )
            report = json.loads(verify.stdout)
            self.assertTrue(report["passed"])

    def test_freeze_returns_nonzero(self) -> None:
        run = subprocess.run(
            [
                sys.executable, "-m", "lbcc.cli", "compact", str(FIXTURE),
                "--max-bytes", "200", "--max-loss-ppm", "0",
            ],
            cwd=ROOT,
            env=ENV,
            capture_output=True,
            text=True,
        )
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)["status"], "FREEZE")

    def test_unknown_input_field_fails_closed(self) -> None:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        data["surprise"] = True
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.json"
            bad.write_text(json.dumps(data), encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-m", "lbcc.cli", "compact", str(bad), "--max-bytes", "5000"],
                cwd=ROOT,
                env=ENV,
                capture_output=True,
                text=True,
            )
        self.assertEqual(run.returncode, 64)
        self.assertIn("unknown field", run.stderr)


if __name__ == "__main__":
    unittest.main()
