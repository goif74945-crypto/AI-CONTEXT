import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from nexy_product_evidence.compiler import compile_experiment
from nexy_product_evidence.io import proposal_from_dict


class IoCliTests(unittest.TestCase):
    def test_proposal_from_dict(self):
        raw = {
            "experiment_id": "abc-123",
            "title": "t",
            "hypothesis": "h",
            "population": "p",
            "primary_metric": {"name":"rate","kind":"proportion","direction":"higher_is_better","baseline":0.4,"mde_abs":0.05,"alpha":0.05,"power":0.8},
            "guardrails": [{"name":"bad","direction":"lower_is_better","baseline":0.1,"max_degradation_abs":0.02}],
            "allocation_fraction": 0.5,
            "duration_days": 7,
            "risk_flags": []
        }
        p = proposal_from_dict(raw)
        self.assertEqual(compile_experiment(p).experiment_id, "abc-123")

    def test_cli_compile_example(self):
        root = Path(__file__).resolve().parents[1]
        env = dict(os.environ)
        env["PYTHONPATH"] = str(root / "src")
        proc = subprocess.run(
            [sys.executable, "-m", "nexy_product_evidence.cli", "compile", str(root / "examples" / "proposal.json")],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('"schema_version": "npel.contract.v1"', proc.stdout)
        self.assertIn('"contract_hash"', proc.stdout)

    def test_cli_freezes_invalid_proposal(self):
        root = Path(__file__).resolve().parents[1]
        env = dict(os.environ)
        env["PYTHONPATH"] = str(root / "src")
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.json"
            p.write_text(json.dumps({"experiment_id":"x"}), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "nexy_product_evidence.cli", "compile", str(p)],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(proc.returncode, 2)
        self.assertIn('"status": "FREEZE"', proc.stderr)


if __name__ == "__main__":
    unittest.main()
