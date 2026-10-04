from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_invalid_json_is_input_error(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad.json"
            path.write_text("{not-json", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "nexy_gate", "validate", str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 64)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["decision"], "FREEZE")
            self.assertTrue(payload["error"].startswith("INPUT_ERROR:"))

    def test_manifest_command_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p1 = Path(td) / "a.json"
            p2 = Path(td) / "b.json"
            p1.write_text('{"b":2,"a":1}', encoding="utf-8")
            p2.write_text('{"a":1,"b":2}', encoding="utf-8")
            hashes = []
            for path in (p1, p2):
                proc = subprocess.run(
                    [sys.executable, "-m", "nexy_gate", "manifest", str(path)],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(proc.returncode, 0)
                hashes.append(json.loads(proc.stdout)["sha256"])
            self.assertEqual(hashes[0], hashes[1])


if __name__ == "__main__":
    unittest.main()
