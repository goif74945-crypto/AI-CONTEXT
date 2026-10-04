from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from nexy_proposal_forge.canon import canonical_json
from nexy_proposal_forge.engine import evaluate_proposal
from nexy_proposal_forge.models import Proposal, ProposalValidationError

ROOT = Path(__file__).resolve().parents[1]


def load_example() -> dict:
    return json.loads((ROOT / "examples" / "proposal-forge-self.json").read_text(encoding="utf-8"))


class EvaluationTests(unittest.TestCase):
    def test_valid_candidate_is_advisory_human_review_only(self) -> None:
        proposal = Proposal.from_dict(load_example())
        result = evaluate_proposal(proposal)
        self.assertEqual(result.recommendation, "PROMOTE_FOR_HUMAN_REVIEW")
        self.assertTrue(result.advisory_only)
        self.assertFalse(result.authoritative)
        self.assertTrue(result.deterministic)
        self.assertEqual(result.evidence_gap_count, 0)

    def test_exact_duplicate_is_rejected(self) -> None:
        proposal = Proposal.from_dict(load_example())
        result = evaluate_proposal(proposal, (proposal,))
        self.assertEqual(result.recommendation, "REJECT_DUPLICATE")
        self.assertGreaterEqual(result.top_overlaps[0].score_bp, 9_500)

    def test_near_duplicate_is_not_silently_novel(self) -> None:
        original_data = load_example()
        near_data = copy.deepcopy(original_data)
        near_data["proposal_id"] = "NPF-NEAR"
        near_data["title"] = "NEXY Proposal Forge Review Gate"
        near_data["summary"] = "A deterministic sandbox for reviewing AI feature proposals."
        original = Proposal.from_dict(original_data)
        near = Proposal.from_dict(near_data)
        result = evaluate_proposal(near, (original,))
        self.assertIn(result.recommendation, {"MERGE_WITH_EXISTING", "REJECT_DUPLICATE"})
        self.assertGreaterEqual(result.top_overlaps[0].score_bp, 7_000)

    def test_missing_evidence_forces_needs_evidence(self) -> None:
        data = load_example()
        data["proposal_id"] = "NPF-GAPS"
        data["evidence"] = []
        proposal = Proposal.from_dict(data)
        result = evaluate_proposal(proposal)
        self.assertEqual(result.recommendation, "NEEDS_EVIDENCE")
        self.assertGreater(result.evidence_gap_count, 0)

    def test_authority_conflict_forces_freeze(self) -> None:
        data = load_example()
        data["proposal_id"] = "NPF-CONFLICT"
        data["authority_conflicts"] = ["DOC-C interpretation conflicts with a candidate assumption"]
        proposal = Proposal.from_dict(data)
        result = evaluate_proposal(proposal)
        self.assertEqual(result.recommendation, "FREEZE_CONFLICT")

    def test_invalid_status_is_rejected_at_validation_boundary(self) -> None:
        data = load_example()
        data["status"] = "APPROVED"
        with self.assertRaises(ProposalValidationError):
            Proposal.from_dict(data)

    def test_identical_evaluation_serializes_identically(self) -> None:
        proposal = Proposal.from_dict(load_example())
        first = canonical_json(evaluate_proposal(proposal).to_dict())
        second = canonical_json(evaluate_proposal(proposal).to_dict())
        self.assertEqual(first, second)

    def test_unknown_proposal_field_is_rejected(self) -> None:
        data = load_example()
        data["surprise_authority"] = "silently ignore me"
        with self.assertRaises(ProposalValidationError):
            Proposal.from_dict(data)

    def test_unknown_evidence_field_is_rejected(self) -> None:
        data = load_example()
        data["evidence"][0]["hidden"] = "extra"
        with self.assertRaises(ProposalValidationError):
            Proposal.from_dict(data)

    def test_duplicate_evidence_ref_id_is_rejected(self) -> None:
        data = load_example()
        data["evidence"][1]["ref_id"] = data["evidence"][0]["ref_id"]
        with self.assertRaises(ProposalValidationError):
            Proposal.from_dict(data)

    def test_reused_identity_with_different_content_freezes(self) -> None:
        original = Proposal.from_dict(load_example())
        changed_data = load_example()
        changed_data["summary"] = "Divergent content under the same proposal id."
        changed = Proposal.from_dict(changed_data)
        result = evaluate_proposal(changed, (original,))
        self.assertEqual(result.recommendation, "FREEZE_CONFLICT")



if __name__ == "__main__":
    unittest.main()
