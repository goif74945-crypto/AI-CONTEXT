from __future__ import annotations

import itertools
import unittest

from ncif.engine import evaluate_consensus
from ncif.models import ConsensusPolicy, ContractError


def root(evidence_id: str, source_identity: str, keys: list[str] | None = None) -> dict:
    return {
        "evidence_id": evidence_id,
        "kind": "runtime",
        "source_identity": source_identity,
        "parents": [],
        "correlation_keys": keys or [],
    }


def support(actor: str, evidence_id: str, keys: list[str] | None = None) -> dict:
    return {
        "actor_id": actor,
        "stance": "SUPPORT",
        "evidence_ids": [evidence_id],
        "correlation_keys": keys or [],
    }


class AdversarialTests(unittest.TestCase):
    def test_result_does_not_echo_raw_source_identity_or_correlation_key(self) -> None:
        secretish_source = "https://internal.example/private?token=do-not-echo"
        secretish_key = "tenant-secretish-correlation-value"
        data = {
            "claim_id": "privacy",
            "evidence": [root("r1", secretish_source, [secretish_key])],
            "votes": [support("actor", "r1", [secretish_key])],
        }
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=1))
        rendered = str(result.to_dict())
        self.assertNotIn(secretish_source, rendered)
        self.assertNotIn(secretish_key, rendered)

    def test_cloned_evidence_ids_from_same_source_do_not_create_fake_independence(self) -> None:
        data = {
            "claim_id": "clone-source",
            "evidence": [root("copy-a", "same-runtime"), root("copy-b", "same-runtime")],
            "votes": [support("a", "copy-a"), support("b", "copy-b")],
        }
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=2))
        self.assertEqual(result.support_group_count, 1)
        self.assertEqual(result.decision, "FREEZE")

    def test_evidence_level_correlation_key_propagates_to_voters(self) -> None:
        data = {
            "claim_id": "evidence-correlation",
            "evidence": [root("a", "source-a", ["dataset:shared"]), root("b", "source-b", ["dataset:shared"])],
            "votes": [support("actor-a", "a"), support("actor-b", "b")],
        }
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=2))
        self.assertEqual(result.support_group_count, 1)

    def test_bridge_chain_of_ten_votes_is_one_connected_group(self) -> None:
        evidence = [root(f"r{i}", f"source-{i}") for i in range(10)]
        votes = []
        for i in range(10):
            keys = []
            if i > 0:
                keys.append(f"bridge:{i-1}")
            if i < 9:
                keys.append(f"bridge:{i}")
            votes.append(support(f"a{i}", f"r{i}", keys))
        result = evaluate_consensus(
            {"claim_id": "bridge-chain", "evidence": evidence, "votes": votes},
            ConsensusPolicy(min_support_groups=2),
        )
        self.assertEqual(result.support_group_count, 1)

    def test_deep_lineage_does_not_depend_on_python_recursion_limit(self) -> None:
        depth = 1500
        evidence = []
        for i in range(depth):
            evidence_id = f"n{i:05d}"
            parents = [] if i == depth - 1 else [f"n{i+1:05d}"]
            evidence.append({
                "evidence_id": evidence_id,
                "kind": "runtime" if not parents else "derived",
                "source_identity": "source-root" if not parents else f"derived-{i}",
                "parents": parents,
                "correlation_keys": [],
            })
        data = {
            "claim_id": "deep-lineage",
            "evidence": evidence,
            "votes": [support("actor", "n00000")],
        }
        result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=1))
        self.assertEqual(result.decision, "CONSENSUS_CANDIDATE")
        self.assertEqual(result.support_groups[0].root_evidence_ids, (f"n{depth-1:05d}",))

    def test_duplicate_evidence_id_is_rejected(self) -> None:
        data = {
            "claim_id": "dup",
            "evidence": [root("r1", "a"), root("r1", "b")],
            "votes": [],
        }
        with self.assertRaises(ContractError):
            evaluate_consensus(data)

    def test_invalid_evidence_kind_is_rejected(self) -> None:
        data = {
            "claim_id": "bad-kind",
            "evidence": [{**root("r1", "a"), "kind": "magic"}],
            "votes": [],
        }
        with self.assertRaises(ContractError):
            evaluate_consensus(data)

    def test_all_vote_permutations_produce_same_result(self) -> None:
        evidence = [root("r1", "s1"), root("r2", "s2"), root("r3", "s3")]
        votes = [support("a", "r1"), support("b", "r2"), support("c", "r3")]
        baseline = evaluate_consensus(
            {"claim_id": "perm", "evidence": evidence, "votes": votes},
            ConsensusPolicy(min_support_groups=3),
        ).to_dict()
        for permutation in itertools.permutations(votes):
            observed = evaluate_consensus(
                {"claim_id": "perm", "evidence": evidence, "votes": list(permutation)},
                ConsensusPolicy(min_support_groups=3),
            ).to_dict()
            self.assertEqual(observed, baseline)

    def test_adding_same_root_supporters_never_increases_independent_group_count(self) -> None:
        evidence = [root("r1", "s1"), root("r2", "s2")]
        base = {"claim_id": "monotonic", "evidence": evidence, "votes": [support("a", "r1"), support("b", "r2")]}
        base_count = evaluate_consensus(base, ConsensusPolicy(min_support_groups=2)).support_group_count
        for n in range(1, 31):
            votes = list(base["votes"]) + [support(f"clone-{i}", "r1") for i in range(n)]
            result = evaluate_consensus(
                {"claim_id": "monotonic", "evidence": evidence, "votes": votes},
                ConsensusPolicy(min_support_groups=2),
            )
            self.assertEqual(result.support_group_count, base_count)


if __name__ == "__main__":
    unittest.main()
