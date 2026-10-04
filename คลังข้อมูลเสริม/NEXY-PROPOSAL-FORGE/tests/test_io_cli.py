from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from nexy_proposal_forge.io import load_catalog
from nexy_proposal_forge.models import ProposalValidationError

ROOT = Path(__file__).resolve().parents[1]


class IoAndCliTests(unittest.TestCase):
    def test_synthetic_catalog_loads(self) -> None:
        catalog = load_catalog(ROOT / "examples" / "catalog.synthetic.json")
        self.assertEqual([item.proposal_id for item in catalog], ["SYN-0001", "SYN-0002"])

    def test_duplicate_catalog_ids_are_rejected(self) -> None:
        data = json.loads((ROOT / "examples" / "catalog.synthetic.json").read_text(encoding="utf-8"))
        data.append(data[0])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ProposalValidationError):
                load_catalog(path)

    def test_cli_validate_and_evaluate(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        proposal = ROOT / "examples" / "proposal-forge-self.json"
        catalog = ROOT / "examples" / "catalog.synthetic.json"

        validate = subprocess.run(
            [sys.executable, "-m", "nexy_proposal_forge", "validate", str(proposal)],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(validate.returncode, 0, validate.stderr)
        self.assertEqual(json.loads(validate.stdout)["status"], "PASS")

        evaluate = subprocess.run(
            [
                sys.executable,
                "-m",
                "nexy_proposal_forge",
                "evaluate",
                str(proposal),
                "--catalog",
                str(catalog),
            ],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(evaluate.returncode, 0, evaluate.stderr)
        payload = json.loads(evaluate.stdout)
        self.assertEqual(payload["recommendation"], "PROMOTE_FOR_HUMAN_REVIEW")
        self.assertTrue(payload["advisory_only"])

    def test_cli_collide(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        current = ROOT / "examples" / "work-manifest.current.json"
        catalog = ROOT / "examples" / "work-manifests.synthetic.json"
        result = subprocess.run(
            [sys.executable, "-m", "nexy_proposal_forge", "collide", str(current), "--catalog", str(catalog)],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["recommendation"], "CLEAR")
        self.assertTrue(payload["advisory_only"])

    def test_cli_invalid_proposal_fails_closed(self) -> None:
        data = json.loads((ROOT / "examples" / "proposal-forge-self.json").read_text(encoding="utf-8"))
        data["status"] = "APPROVED"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            result = subprocess.run(
                [sys.executable, "-m", "nexy_proposal_forge", "validate", str(path)],
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
