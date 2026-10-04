from __future__ import annotations

import copy
import json
import random
import unittest
from pathlib import Path

from nexy_intent_guard import (
    ContractError,
    GuardDecision,
    compare_contracts,
    evaluate_proposal,
    semantic_digest,
)

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class ProposalGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load("base_contract.json")

    def test_passing_proposal_passes(self) -> None:
        report = evaluate_proposal(self.contract, load("passing_proposal.json"))
        self.assertEqual(report.decision, GuardDecision.PASS)
        self.assertEqual([f.code for f in report.findings], ["INTENT_INTEGRITY_PRESERVED"])

    def test_protected_path_freezes(self) -> None:
        report = evaluate_proposal(self.contract, load("protected_touch_proposal.json"))
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("PROTECTED_SCOPE_TOUCH", {f.code for f in report.findings})

    def test_protected_repository_identity_freezes(self) -> None:
        proposal = load("passing_proposal.json")
        proposal["target_repository"] = "goif74945-crypto/NEXY.AI-CORE"
        report = evaluate_proposal(self.contract, proposal)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("PROTECTED_REPOSITORY_TARGET", {f.code for f in report.findings})

    def test_unlisted_repository_identity_freezes(self) -> None:
        proposal = load("passing_proposal.json")
        proposal["target_repository"] = "goif74945-crypto/SOME-OTHER-REPO"
        report = evaluate_proposal(self.contract, proposal)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("UNAUTHORIZED_REPOSITORY_TARGET", {f.code for f in report.findings})

    def test_repository_matching_is_case_insensitive(self) -> None:
        proposal = load("passing_proposal.json")
        proposal["target_repository"] = "GOIF74945-CRYPTO/ai-context"
        report = evaluate_proposal(self.contract, proposal)
        self.assertEqual(report.decision, GuardDecision.PASS)

    def test_out_of_scope_path_freezes(self) -> None:
        proposal = load("passing_proposal.json")
        proposal["touch_paths"] = ["projects/NEXY.AI/overview.md"]
        report = evaluate_proposal(self.contract, proposal)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("OUT_OF_SCOPE_TOUCH", {f.code for f in report.findings})

    def test_unlisted_path_freezes(self) -> None:
        proposal = load("passing_proposal.json")
        proposal["touch_paths"] = ["README.md"]
        report = evaluate_proposal(self.contract, proposal)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("UNAUTHORIZED_SCOPE_EXPANSION", {f.code for f in report.findings})

    def test_missing_requirement_coverage_freezes(self) -> None:
        proposal = load("passing_proposal.json")
        proposal["covered_requirement_ids"].remove("REQ-003")
        report = evaluate_proposal(self.contract, proposal)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("REQUIREMENT_COVERAGE_GAP", {f.code for f in report.findings})

    def test_unknown_requirement_reference_freezes(self) -> None:
        proposal = load("passing_proposal.json")
        proposal["covered_requirement_ids"].append("REQ-999")
        report = evaluate_proposal(self.contract, proposal)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("UNKNOWN_REQUIREMENT_REFERENCE", {f.code for f in report.findings})

    def test_evidence_downgrade_freezes(self) -> None:
        report = evaluate_proposal(self.contract, load("evidence_downgrade_proposal.json"))
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("EVIDENCE_DOWNGRADE", {f.code for f in report.findings})

    def test_missing_evidence_freezes(self) -> None:
        proposal = load("passing_proposal.json")
        del proposal["evidence"]["AC-002"]
        report = evaluate_proposal(self.contract, proposal)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("MISSING_ACCEPTANCE_EVIDENCE", {f.code for f in report.findings})

    def test_assumption_cannot_be_labeled_fact(self) -> None:
        report = evaluate_proposal(self.contract, load("assumption_fact_proposal.json"))
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("ASSUMPTION_ESCALATED_TO_FACT", {f.code for f in report.findings})

    def test_unverified_completion_claim_freezes(self) -> None:
        proposal = load("passing_proposal.json")
        proposal["claims"] = [{
            "id": "CLM-NV",
            "truth_class": "NOT_VERIFIED",
            "basis": "Code exists but runtime evidence is unavailable.",
            "completion_claim": True,
        }]
        report = evaluate_proposal(self.contract, proposal)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("UNVERIFIED_COMPLETION_CLAIM", {f.code for f in report.findings})

    def test_unknown_evidence_key_requires_review(self) -> None:
        proposal = load("passing_proposal.json")
        proposal["evidence"]["AC-UNBOUND"] = "unit"
        report = evaluate_proposal(self.contract, proposal)
        self.assertEqual(report.decision, GuardDecision.REVIEW)
        self.assertIn("UNBOUND_EVIDENCE", {f.code for f in report.findings})

    def test_path_escape_is_invalid_input(self) -> None:
        proposal = load("passing_proposal.json")
        proposal["touch_paths"] = ["../outside.txt"]
        with self.assertRaises(ContractError):
            evaluate_proposal(self.contract, proposal)


class CanonicalizationTests(unittest.TestCase):
    def test_digest_is_independent_of_object_key_order_and_set_like_array_order(self) -> None:
        contract = load("base_contract.json")
        shuffled = copy.deepcopy(contract)
        shuffled["requirements"] = list(reversed(shuffled["requirements"]))
        shuffled["scope"]["in_scope"] = list(reversed(shuffled["scope"]["in_scope"]))
        shuffled = {k: shuffled[k] for k in reversed(list(shuffled))}
        self.assertEqual(semantic_digest(contract), semantic_digest(shuffled))

    def test_digest_changes_when_objective_changes(self) -> None:
        contract = load("base_contract.json")
        changed = copy.deepcopy(contract)
        changed["objective"] += " Changed semantics."
        self.assertNotEqual(semantic_digest(contract), semantic_digest(changed))

    def test_random_requirement_order_never_changes_digest(self) -> None:
        contract = load("base_contract.json")
        expected = semantic_digest(contract)
        for seed in range(50):
            candidate = copy.deepcopy(contract)
            random.Random(seed).shuffle(candidate["requirements"])
            random.Random(seed + 1000).shuffle(candidate["acceptance_criteria"])
            self.assertEqual(expected, semantic_digest(candidate), f"seed={seed}")


class TransitionGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = load("base_contract.json")

    def test_identical_contract_passes(self) -> None:
        report = compare_contracts(self.base, copy.deepcopy(self.base))
        self.assertEqual(report.decision, GuardDecision.PASS)
        self.assertEqual(report.change_ids, ())

    def test_objective_drift_freezes(self) -> None:
        candidate = copy.deepcopy(self.base)
        candidate["objective"] = "Do something else."
        report = compare_contracts(self.base, candidate)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("objective:main", report.change_ids)

    def test_normalization_only_change_does_not_create_drift(self) -> None:
        candidate = copy.deepcopy(self.base)
        candidate["objective"] = self.base["objective"] + "  \r\n"
        report = compare_contracts(self.base, candidate)
        self.assertEqual(report.decision, GuardDecision.PASS)
        self.assertNotIn("objective:main", report.change_ids)

    def test_immutable_requirement_removal_freezes(self) -> None:
        candidate = copy.deepcopy(self.base)
        candidate["requirements"] = [r for r in candidate["requirements"] if r["id"] != "REQ-001"]
        candidate["acceptance_criteria"][1]["requirement_ids"] = ["REQ-002"]
        report = compare_contracts(self.base, candidate)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        codes = {f.code for f in report.findings}
        self.assertIn("IMMUTABLE_INTENT_DRIFT", codes)

    def test_explicit_user_approval_authorizes_exact_change(self) -> None:
        candidate = copy.deepcopy(self.base)
        candidate["objective"] = "Create a revised supplemental research artifact."
        approval = {
            "approver": "user",
            "approved_change_ids": ["objective:main"]
        }
        report = compare_contracts(self.base, candidate, approval)
        self.assertEqual(report.decision, GuardDecision.PASS)
        self.assertIn("AUTHORIZED_INTENT_CHANGE", {f.code for f in report.findings})

    def test_approval_is_exact_not_blanket(self) -> None:
        candidate = copy.deepcopy(self.base)
        candidate["objective"] = "Changed objective."
        candidate["scope"]["in_scope"].append("another/**")
        approval = {
            "approver": "user",
            "approved_change_ids": ["objective:main"]
        }
        report = compare_contracts(self.base, candidate, approval)
        self.assertEqual(report.decision, GuardDecision.FREEZE)
        self.assertIn("scope.in_scope.add:another/**", report.change_ids)

    def test_stale_approval_requires_review(self) -> None:
        approval = {
            "approver": "user",
            "approved_change_ids": ["objective:main"]
        }
        report = compare_contracts(self.base, copy.deepcopy(self.base), approval)
        self.assertEqual(report.decision, GuardDecision.REVIEW)
        self.assertIn("STALE_OR_UNKNOWN_APPROVAL", {f.code for f in report.findings})


if __name__ == "__main__":
    unittest.main()
