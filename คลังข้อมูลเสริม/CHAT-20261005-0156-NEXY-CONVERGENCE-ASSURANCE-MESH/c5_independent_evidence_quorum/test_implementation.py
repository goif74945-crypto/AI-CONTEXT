from __future__ import annotations

import unittest

from c5_independent_evidence_quorum.implementation import (
    EvidenceRecord,
    QuorumNeed,
    evaluate_independent_quorum,
)


def ev(eid, *, klass="E3", producer, domains, derived=()):
    return EvidenceRecord(eid, "claim-x", klass, producer, frozenset(domains), tuple(derived))


class IndependentEvidenceQuorumTests(unittest.TestCase):
    def test_two_independent_witnesses_pass(self) -> None:
        result = evaluate_independent_quorum(
            QuorumNeed("claim-x", "E3", 2),
            [
                ev("a", producer="vitest", domains={"ci-a"}),
                ev("b", producer="playwright", domains={"browser-b"}),
            ],
        )
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.details["selected_evidence"], ["a", "b"])

    def test_common_failure_domain_freezes(self) -> None:
        result = evaluate_independent_quorum(
            QuorumNeed("claim-x", "E3", 2),
            [
                ev("a", producer="tool-a", domains={"same-runner"}),
                ev("b", producer="tool-b", domains={"same-runner"}),
            ],
        )
        self.assertEqual(result.status, "FREEZE")

    def test_shared_producer_freezes_even_with_different_domains(self) -> None:
        result = evaluate_independent_quorum(
            QuorumNeed("claim-x", "E3", 2),
            [
                ev("a", producer="same-tool", domains={"runner-a"}),
                ev("b", producer="same-tool", domains={"runner-b"}),
            ],
        )
        self.assertEqual(result.status, "FREEZE")

    def test_derived_evidence_inherits_parent_failure_domain(self) -> None:
        result = evaluate_independent_quorum(
            QuorumNeed("claim-x", "E3", 2),
            [
                ev("root", producer="tool-root", domains={"runner-a"}),
                ev("derived", producer="tool-b", domains={"runner-b"}, derived=("root",)),
            ],
        )
        self.assertEqual(result.status, "FREEZE")

    def test_dependency_cycle_is_blocked(self) -> None:
        result = evaluate_independent_quorum(
            QuorumNeed("claim-x", "E1", 1),
            [
                ev("a", klass="E1", producer="a", domains={"a"}, derived=("b",)),
                ev("b", klass="E1", producer="b", domains={"b"}, derived=("a",)),
            ],
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.reason, "INVALID_EVIDENCE_DEPENDENCY_GRAPH")

    def test_lower_evidence_class_is_not_eligible(self) -> None:
        result = evaluate_independent_quorum(
            QuorumNeed("claim-x", "E4", 1),
            [ev("a", klass="E3", producer="a", domains={"a"})],
        )
        self.assertEqual(result.status, "FREEZE")
        self.assertEqual(result.details["eligible_evidence"], [])


if __name__ == "__main__":
    unittest.main()
