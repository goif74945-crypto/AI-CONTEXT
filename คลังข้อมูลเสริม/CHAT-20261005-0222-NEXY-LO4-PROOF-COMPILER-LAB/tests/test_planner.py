import unittest

from nexy_lo4_lab.planner import (
    ClaimRequirement,
    MinimumProofPlanner,
    Probe,
    ProofPlanError,
)


class MinimumProofPlannerTests(unittest.TestCase):
    def test_selects_minimum_total_cost(self):
        planner = MinimumProofPlanner()
        result = planner.plan(
            [ClaimRequirement("a", 2), ClaimRequirement("b", 2)],
            [
                Probe("both", 5, 2, frozenset({"a", "b"})),
                Probe("a-only", 2, 2, frozenset({"a"})),
                Probe("b-only", 2, 2, frozenset({"b"})),
            ],
        )
        self.assertEqual(result.selected_probe_ids, ("a-only", "b-only"))
        self.assertEqual(result.total_cost, 4)

    def test_insufficient_evidence_class_is_not_eligible(self):
        planner = MinimumProofPlanner()
        result = planner.plan(
            [ClaimRequirement("a", 3)],
            [
                Probe("cheap-e2", 1, 2, frozenset({"a"})),
                Probe("real-e3", 4, 3, frozenset({"a"})),
            ],
        )
        self.assertEqual(result.selected_probe_ids, ("real-e3",))

    def test_unavailable_probe_is_excluded(self):
        planner = MinimumProofPlanner()
        result = planner.plan(
            [ClaimRequirement("a", 2)],
            [
                Probe("offline", 1, 2, frozenset({"a"}), available=False),
                Probe("online", 3, 2, frozenset({"a"})),
            ],
        )
        self.assertEqual(result.selected_probe_ids, ("online",))

    def test_tie_break_is_lexicographic_and_deterministic(self):
        planner = MinimumProofPlanner()
        result = planner.plan(
            [ClaimRequirement("a", 1)],
            [
                Probe("z", 1, 1, frozenset({"a"})),
                Probe("a", 1, 1, frozenset({"a"})),
            ],
        )
        self.assertEqual(result.selected_probe_ids, ("a",))

    def test_impossible_plan_fails_closed(self):
        with self.assertRaisesRegex(ProofPlanError, "no available probe"):
            MinimumProofPlanner().plan(
                [ClaimRequirement("a", 4)],
                [Probe("e2", 1, 2, frozenset({"a"}))],
            )

    def test_claim_limit_fails_closed(self):
        planner = MinimumProofPlanner(max_exact_claims=2)
        with self.assertRaisesRegex(ProofPlanError, "claim limit exceeded"):
            planner.plan(
                [ClaimRequirement("a", 1), ClaimRequirement("b", 1), ClaimRequirement("c", 1)],
                [Probe("p", 1, 1, frozenset({"a", "b", "c"}))],
            )

    def test_irrelevant_probes_do_not_consume_candidate_bound(self):
        planner = MinimumProofPlanner(max_candidate_probes=1)
        result = planner.plan(
            [ClaimRequirement("a", 1)],
            [
                Probe("relevant", 1, 1, frozenset({"a"})),
                Probe("irrelevant-1", 1, 7, frozenset({"x"})),
                Probe("irrelevant-2", 1, 7, frozenset({"y"})),
            ],
        )
        self.assertEqual(result.selected_probe_ids, ("relevant",))

    def test_strictly_cheaper_superset_prunes_dominated_probe_without_changing_optimum(self):
        planner = MinimumProofPlanner()
        result = planner.plan(
            [ClaimRequirement("a", 2), ClaimRequirement("b", 2)],
            [
                Probe("dominator", 2, 2, frozenset({"a", "b"})),
                Probe("dominated", 5, 2, frozenset({"a"})),
                Probe("b", 10, 2, frozenset({"b"})),
            ],
        )
        self.assertEqual(result.selected_probe_ids, ("dominator",))
        self.assertEqual(result.total_cost, 2)

    def test_equal_cost_equal_coverage_keeps_lexicographically_smallest(self):
        planner = MinimumProofPlanner()
        result = planner.plan(
            [ClaimRequirement("a", 2)],
            [
                Probe("z", 2, 2, frozenset({"a"})),
                Probe("a", 2, 2, frozenset({"a"})),
            ],
        )
        self.assertEqual(result.selected_probe_ids, ("a",))

    def test_probe_input_order_does_not_change_plan(self):
        planner = MinimumProofPlanner()
        probes = [
            Probe("a", 2, 2, frozenset({"a"})),
            Probe("b", 2, 2, frozenset({"b"})),
            Probe("ab", 4, 2, frozenset({"a", "b"})),
        ]
        reqs = [ClaimRequirement("a", 2), ClaimRequirement("b", 2)]
        self.assertEqual(
            planner.plan(reqs, probes),
            planner.plan(reversed(reqs), reversed(probes)),
        )


if __name__ == "__main__":
    unittest.main()
