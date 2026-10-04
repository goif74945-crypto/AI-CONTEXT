from __future__ import annotations

import unittest

from c3_evidence_acquisition.implementation import ClaimNeed, Probe, plan_evidence_acquisition


class EvidenceAcquisitionTests(unittest.TestCase):
    def test_exact_minimum_cost_cover(self) -> None:
        needs = [ClaimNeed("syntax", "E1"), ClaimNeed("api", "E3")]
        probes = [
            Probe("lint", 2, {"syntax": "E1"}),
            Probe("integration", 5, {"api": "E3"}),
            Probe("combo", 6, {"syntax": "E1", "api": "E3"}),
        ]
        result = plan_evidence_acquisition(needs, probes)
        self.assertEqual(result.status, "PLANNED")
        self.assertEqual(result.details["selected_probes"], ["combo"])
        self.assertEqual(result.details["total_cost"], 6)

    def test_lower_class_does_not_substitute(self) -> None:
        result = plan_evidence_acquisition(
            [ClaimNeed("api", "E3")], [Probe("unit", 1, {"api": "E2"})]
        )
        self.assertEqual(result.status, "FREEZE")
        self.assertEqual(result.details["uncovered_claims"], ["api"])

    def test_prerequisite_gate(self) -> None:
        probe = Probe("db-int", 1, {"db": "E3"}, frozenset({"postgres"}))
        blocked = plan_evidence_acquisition([ClaimNeed("db", "E3")], [probe])
        ready = plan_evidence_acquisition(
            [ClaimNeed("db", "E3")], [probe], available_prerequisites=frozenset({"postgres"})
        )
        self.assertEqual(blocked.status, "FREEZE")
        self.assertEqual(ready.status, "PLANNED")

    def test_tie_break_is_lexicographic_and_order_independent(self) -> None:
        needs = [ClaimNeed("x", "E2")]
        a = Probe("a", 1, {"x": "E2"})
        b = Probe("b", 1, {"x": "E2"})
        left = plan_evidence_acquisition(needs, [b, a])
        right = plan_evidence_acquisition(needs, [a, b])
        self.assertEqual(left.details["selected_probes"], ["a"])
        self.assertEqual(left.details, right.details)

    def test_empty_needs_is_zero_cost(self) -> None:
        result = plan_evidence_acquisition([], [Probe("unused", 99, {"x": "E7"})])
        self.assertEqual(result.reason, "NO_EVIDENCE_NEEDED")
        self.assertEqual(result.details["total_cost"], 0)


if __name__ == "__main__":
    unittest.main()
