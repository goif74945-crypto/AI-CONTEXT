from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from nexy_intent_guard import ContractError, GuardDecision
from nexy_intent_guard.state_binding import create_execution_seal, verify_execution_seal

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class ExecutionSealTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load("base_contract.json")
        self.proposal = load("passing_proposal.json")
        self.revision = "0123456789abcdef"
        self.seal = create_execution_seal(
            self.contract,
            self.proposal,
            target_revision=self.revision,
            target_ref="main",
        )

    def verify(self, **overrides):
        args = {
            "current_repository": "goif74945-crypto/AI-CONTEXT",
            "current_ref": "main",
            "current_revision": self.revision,
        }
        args.update(overrides)
        return verify_execution_seal(
            self.seal,
            self.contract,
            self.proposal,
            **args,
        )

    def test_exact_state_passes(self) -> None:
        report = self.verify()
        self.assertEqual(report.decision, GuardDecision.PASS)
        self.assertEqual([f.code for f in report.findings], ["EXECUTION_SEAL_VALID"])

    def test_repository_revision_change_freezes(self) -> None:
        report = self.verify(current_revision="fedcba9876543210")
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("REPOSITORY_REVISION_CHANGED", {f.code for f in report.findings})

    def test_repository_identity_change_freezes(self) -> None:
        report = self.verify(current_repository="goif74945-crypto/OTHER")
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("REPOSITORY_IDENTITY_CHANGED", {f.code for f in report.findings})

    def test_repository_ref_change_freezes(self) -> None:
        report = self.verify(current_ref="release")
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("REPOSITORY_REF_CHANGED", {f.code for f in report.findings})

    def test_contract_change_freezes(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["objective"] += " altered"
        report = verify_execution_seal(
            self.seal,
            changed,
            self.proposal,
            current_repository="goif74945-crypto/AI-CONTEXT",
            current_ref="main",
            current_revision=self.revision,
        )
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("STALE_CONTRACT_DIGEST", {f.code for f in report.findings})

    def test_proposal_change_freezes(self) -> None:
        changed = copy.deepcopy(self.proposal)
        changed["touch_paths"].append("คลังข้อมูลเสริม/NEXY-INTENT-INTEGRITY-LAB-20261005/new.md")
        report = verify_execution_seal(
            self.seal,
            self.contract,
            changed,
            current_repository="goif74945-crypto/AI-CONTEXT",
            current_ref="main",
            current_revision=self.revision,
        )
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("STALE_PROPOSAL_DIGEST", {f.code for f in report.findings})

    def test_tampered_seal_freezes(self) -> None:
        tampered = self.seal.to_dict()
        tampered["target_revision"] = "tampered"
        report = verify_execution_seal(
            tampered,
            self.contract,
            self.proposal,
            current_repository="goif74945-crypto/AI-CONTEXT",
            current_ref="main",
            current_revision="tampered",
        )
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("SEAL_INTEGRITY_MISMATCH", {f.code for f in report.findings})

    def test_non_passing_proposal_cannot_be_sealed(self) -> None:
        invalid = load("protected_touch_proposal.json")
        with self.assertRaises(ContractError):
            create_execution_seal(
                self.contract,
                invalid,
                target_revision=self.revision,
                target_ref="main",
            )

    def test_case_only_repository_identity_change_is_tolerated(self) -> None:
        report = self.verify(current_repository="GOIF74945-CRYPTO/ai-context")
        self.assertEqual(report.decision, GuardDecision.PASS)


if __name__ == "__main__":
    unittest.main()
