from __future__ import annotations

import copy
import json
import unittest

from ncif.engine import evaluate_consensus
from ncif.models import ContractError, ConsensusPolicy


def payload(*, roots: list[str], votes: list[dict], evidence_extra: list[dict] | None = None) -> dict:
    evidence = [
        {
            "evidence_id": root,
            "kind": "runtime",
            "source_identity": root,
            "parents": [],
            "correlation_keys": [],
        }
        for root in roots
    ]
    evidence.extend(evidence_extra or [])
    return {"claim_id": "claim-1", "evidence": evidence, "votes": votes}


def vote(actor: str, stance: str, evidence_ids: list[str], correlation_keys: list[str] | None = None) -> dict:
    return {
        "actor_id": actor,
        "stance": stance,
        "evidence_ids": evidence_ids,
        "correlation_keys": correlation_keys or [],
    }


class ConsensusEngineTests(unittest.TestCase):
    def test_distinct_roots_form_independent_support_groups(self) -> None:
        data = payload(
            roots=["r1", "r2", "r3"],
            votes=[vote("a", "SUPPORT", ["r1"]), vote("b", "SUPPORT", ["r2"]), vote("c", "SUPPORT", ["r3"])],
        )
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=3))
        self.assertEqual(result.decision, "CONSENSUS_CANDIDATE")
        self.assertEqual(result.support_group_count, 3)
        self.assertEqual(result.freeze_reasons, ())

    def test_many_agents_on_one_root_count_as_one_group(self) -> None:
        data = payload(
            roots=["shared"],
            votes=[vote("a", "SUPPORT", ["shared"]), vote("b", "SUPPORT", ["shared"]), vote("c", "SUPPORT", ["shared"])],
        )
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=2))
        self.assertEqual(result.decision, "FREEZE")
        self.assertEqual(result.support_group_count, 1)
        self.assertIn("INSUFFICIENT_INDEPENDENT_SUPPORT", result.freeze_reasons)

    def test_transitive_bridge_correlation_collapses_all_connected_votes(self) -> None:
        data = payload(
            roots=["r1", "r2", "r3"],
            votes=[
                vote("a", "SUPPORT", ["r1"], ["ctx:x"]),
                vote("b", "SUPPORT", ["r2"], ["ctx:x", "tool:y"]),
                vote("c", "SUPPORT", ["r3"], ["tool:y"]),
            ],
        )
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=2))
        self.assertEqual(result.support_group_count, 1)
        self.assertEqual(result.decision, "FREEZE")

    def test_shared_declared_correlation_key_collapses_distinct_evidence_roots(self) -> None:
        data = payload(
            roots=["r1", "r2"],
            votes=[vote("a", "SUPPORT", ["r1"], ["snapshot:42"]), vote("b", "SUPPORT", ["r2"], ["snapshot:42"])],
        )
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=2))
        self.assertEqual(result.support_group_count, 1)
        self.assertIn("INSUFFICIENT_INDEPENDENT_SUPPORT", result.freeze_reasons)

    def test_evidence_parent_lineage_propagates_root_correlation(self) -> None:
        derived = [
            {"evidence_id": "d1", "kind": "derived", "source_identity": "calc-a", "parents": ["r1"], "correlation_keys": []},
            {"evidence_id": "d2", "kind": "derived", "source_identity": "calc-b", "parents": ["r1"], "correlation_keys": []},
        ]
        data = payload(
            roots=["r1"],
            evidence_extra=derived,
            votes=[vote("a", "SUPPORT", ["d1"]), vote("b", "SUPPORT", ["d2"])],
        )
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=2))
        self.assertEqual(result.support_group_count, 1)
        self.assertEqual(result.support_groups[0].root_evidence_ids, ("r1",))

    def test_missing_parent_fails_closed(self) -> None:
        data = {
            "claim_id": "claim-1",
            "evidence": [
                {"evidence_id": "d1", "kind": "derived", "source_identity": "calc", "parents": ["missing"], "correlation_keys": []}
            ],
            "votes": [vote("a", "SUPPORT", ["d1"])],
        }
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=1))
        self.assertEqual(result.decision, "FREEZE")
        self.assertIn("MISSING_EVIDENCE_PARENT", result.freeze_reasons)

    def test_cycle_fails_closed(self) -> None:
        data = {
            "claim_id": "claim-1",
            "evidence": [
                {"evidence_id": "a", "kind": "derived", "source_identity": "a", "parents": ["b"], "correlation_keys": []},
                {"evidence_id": "b", "kind": "derived", "source_identity": "b", "parents": ["a"], "correlation_keys": []},
            ],
            "votes": [vote("actor", "SUPPORT", ["a"])],
        }
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=1))
        self.assertEqual(result.decision, "FREEZE")
        self.assertIn("EVIDENCE_LINEAGE_CYCLE", result.freeze_reasons)

    def test_support_without_evidence_fails_closed(self) -> None:
        data = payload(roots=[], votes=[vote("a", "SUPPORT", [])])
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=1))
        self.assertEqual(result.decision, "FREEZE")
        self.assertIn("SUPPORT_WITHOUT_EVIDENCE", result.freeze_reasons)

    def test_independently_evidenced_opposition_blocks_candidate(self) -> None:
        data = payload(
            roots=["s1", "s2", "o1"],
            votes=[vote("a", "SUPPORT", ["s1"]), vote("b", "SUPPORT", ["s2"]), vote("c", "OPPOSE", ["o1"])],
        )
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=2, max_opposition_groups=0))
        self.assertEqual(result.decision, "FREEZE")
        self.assertEqual(result.opposition_group_count, 1)
        self.assertIn("INDEPENDENT_OPPOSITION_PRESENT", result.freeze_reasons)

    def test_abstain_does_not_count_for_or_against_consensus(self) -> None:
        data = payload(
            roots=["r1", "r2"],
            votes=[vote("a", "SUPPORT", ["r1"]), vote("b", "SUPPORT", ["r2"]), vote("c", "ABSTAIN", [])],
        )
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=2))
        self.assertEqual(result.decision, "CONSENSUS_CANDIDATE")
        self.assertEqual(result.abstain_count, 1)

    def test_duplicate_actor_vote_is_contract_error(self) -> None:
        data = payload(
            roots=["r1", "r2"],
            votes=[vote("a", "SUPPORT", ["r1"]), vote("a", "SUPPORT", ["r2"])],
        )
        with self.assertRaises(ContractError):
            evaluate_consensus(data, ConsensusPolicy(min_support_groups=1))

    def test_unknown_vote_evidence_is_contract_error(self) -> None:
        data = payload(roots=["r1"], votes=[vote("a", "SUPPORT", ["missing"])])
        with self.assertRaises(ContractError):
            evaluate_consensus(data, ConsensusPolicy(min_support_groups=1))

    def test_order_invariance_and_fingerprint_determinism(self) -> None:
        data = payload(
            roots=["r1", "r2", "r3"],
            votes=[vote("a", "SUPPORT", ["r1"]), vote("b", "SUPPORT", ["r2"]), vote("c", "ABSTAIN", ["r3"])],
        )
        policy = ConsensusPolicy(min_support_groups=2)
        a = evaluate_consensus(data, policy)
        shuffled = copy.deepcopy(data)
        shuffled["evidence"].reverse()
        shuffled["votes"].reverse()
        b = evaluate_consensus(shuffled, policy)
        self.assertEqual(a.to_dict(), b.to_dict())
        self.assertEqual(a.fingerprint, b.fingerprint)

    def test_single_root_resilience_can_be_required(self) -> None:
        data = payload(
            roots=["r1", "r2", "r3"],
            votes=[vote("a", "SUPPORT", ["r1"]), vote("b", "SUPPORT", ["r2"]), vote("c", "SUPPORT", ["r3"])],
        )
        result = evaluate_consensus(
            data,
            ConsensusPolicy(min_support_groups=2, require_single_root_resilience=True),
        )
        self.assertEqual(result.decision, "CONSENSUS_CANDIDATE")
        self.assertEqual(result.single_root_resilience_min_support_groups, 2)

    def test_single_root_resilience_freezes_brittle_two_root_consensus(self) -> None:
        data = payload(
            roots=["r1", "r2"],
            votes=[vote("a", "SUPPORT", ["r1"]), vote("b", "SUPPORT", ["r2"])],
        )
        result = evaluate_consensus(
            data,
            ConsensusPolicy(min_support_groups=2, require_single_root_resilience=True),
        )
        self.assertEqual(result.decision, "FREEZE")
        self.assertEqual(result.single_root_resilience_min_support_groups, 1)
        self.assertIn("SINGLE_ROOT_RESILIENCE_FAILED", result.freeze_reasons)

    def test_same_root_support_and_opposition_is_reported_as_interpretation_conflict(self) -> None:
        data = payload(
            roots=["r1", "r2"],
            votes=[vote("a", "SUPPORT", ["r1"]), vote("b", "SUPPORT", ["r2"]), vote("c", "OPPOSE", ["r1"])],
        )
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=2, max_opposition_groups=1))
        self.assertEqual(result.decision, "FREEZE")
        self.assertIn("SHARED_ROOT_STANCE_CONFLICT", result.freeze_reasons)

    def test_invalid_policy_is_rejected(self) -> None:
        with self.assertRaises(ContractError):
            ConsensusPolicy(min_support_groups=0)


if __name__ == "__main__":
    unittest.main()
