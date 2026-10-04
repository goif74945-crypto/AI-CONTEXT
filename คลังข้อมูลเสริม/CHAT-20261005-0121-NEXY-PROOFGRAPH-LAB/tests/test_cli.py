from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CLITests(unittest.TestCase):
    def policy(self, root: Path) -> Path:
        path = root / "policy.json"
        path.write_text(json.dumps({
            "proposal_root": "คลังข้อมูลเสริม",
            "nexy": {
                "current_requirement_rows": 837,
                "current_build_rows": 773,
                "deprecated_registry_count": 215,
                "historical_partial_registry_count": 262,
                "ontology_entity_count": 518
            }
        }), encoding="utf-8")
        return path

    def test_scan_exit_code_tracks_error_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = self.policy(root)
            (root / "x.md").write_text("Current total system count: 215", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "nexy_proofgraph", "scan", str(root), "--policy", str(policy), "--format", "json"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(proc.returncode, 1)
            payload = json.loads(proc.stdout)
            self.assertFalse(payload["ok"])
            self.assertGreaterEqual(payload["counts"]["CRITICAL"], 1)


if __name__ == "__main__":
    unittest.main()
