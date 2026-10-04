import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "fixtures" / "base.json"
CURRENT = ROOT / "fixtures" / "current.json"


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "context_delta_lab.cli", *map(str, args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
            check=False,
        )

    def test_cli_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "report.json"
            proc = self.run_cli(BASE, CURRENT, "--output", out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(out.read_text(encoding="utf-8"))
            self.assertGreater(report["summary"]["change_count"], 0)
            self.assertEqual(report["truth_boundary"], "REPORT_IS_ADVISORY; IMPLEMENTATION_AND_RUNTIME_REMAIN_NOT_VERIFIED")

    def test_fail_on_change_returns_4_after_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "report.json"
            proc = self.run_cli(BASE, CURRENT, "--output", out, "--fail-on-change")
            self.assertEqual(proc.returncode, 4)
            self.assertTrue(out.exists())

    def test_invalid_semantics_returns_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps({"snapshot_id": "x", "source_commit": "x", "requirements": [{"id": "R", "authority": "BAD", "scope": "CURRENT_BUILD", "statement": "x", "evidence_class": "E2"}]}), encoding="utf-8")
            proc = self.run_cli(bad, CURRENT)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("FREEZE", proc.stderr)

    def test_invalid_json_returns_3(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text("{", encoding="utf-8")
            proc = self.run_cli(bad, CURRENT)
            self.assertEqual(proc.returncode, 3)
            self.assertIn("INPUT_ERROR", proc.stderr)


if __name__ == "__main__":
    unittest.main()
