from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from nexy_intent_guard.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


class CliTests(unittest.TestCase):
    def run_cli(self, argv: list[str]) -> tuple[int, dict]:
        out = io.StringIO()
        with redirect_stdout(out):
            rc = main(argv)
        return rc, json.loads(out.getvalue())

    def test_digest_command(self) -> None:
        rc, payload = self.run_cli(["digest", str(FIXTURES / "base_contract.json")])
        self.assertEqual(rc, 0)
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(len(payload["contract_digest"]), 64)

    def test_check_proposal_freezes_invalid_path(self) -> None:
        rc, payload = self.run_cli([
            "check-proposal",
            str(FIXTURES / "base_contract.json"),
            str(FIXTURES / "protected_touch_proposal.json"),
        ])
        self.assertEqual(rc, 2)
        self.assertEqual(payload["decision"], "FREEZE")

    def test_create_and_verify_seal_commands(self) -> None:
        contract = str(FIXTURES / "base_contract.json")
        proposal = str(FIXTURES / "passing_proposal.json")
        rc, seal = self.run_cli([
            "create-seal", contract, proposal,
            "--revision", "abc123", "--ref", "main",
        ])
        self.assertEqual(rc, 0)
        with tempfile.TemporaryDirectory() as td:
            seal_path = Path(td) / "seal.json"
            seal_path.write_text(json.dumps(seal), encoding="utf-8")
            rc, payload = self.run_cli([
                "verify-seal", str(seal_path), contract, proposal,
                "--repository", "goif74945-crypto/AI-CONTEXT",
                "--ref", "main",
                "--revision", "abc123",
            ])
        self.assertEqual(rc, 0)
        self.assertEqual(payload["decision"], "PASS")

    def test_verify_seal_freezes_stale_revision(self) -> None:
        contract = str(FIXTURES / "base_contract.json")
        proposal = str(FIXTURES / "passing_proposal.json")
        _, seal = self.run_cli([
            "create-seal", contract, proposal,
            "--revision", "abc123", "--ref", "main",
        ])
        with tempfile.TemporaryDirectory() as td:
            seal_path = Path(td) / "seal.json"
            seal_path.write_text(json.dumps(seal), encoding="utf-8")
            rc, payload = self.run_cli([
                "verify-seal", str(seal_path), contract, proposal,
                "--repository", "goif74945-crypto/AI-CONTEXT",
                "--ref", "main",
                "--revision", "def456",
            ])
        self.assertEqual(rc, 2)
        self.assertEqual(payload["decision"], "FREEZE")
        self.assertIn("REPOSITORY_REVISION_CHANGED", {f["code"] for f in payload["findings"]})


if __name__ == "__main__":
    unittest.main()
