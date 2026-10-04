import os
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from eecp import Claim, Evidence, EvidenceGraph, GraphError, PlanningLimitExceeded


class ExactEvidenceCutPlannerTests(unittest.TestCase):
    def test_and_claim_requires_union(self):
        g = EvidenceGraph([
            Evidence("E1", 2), Evidence("E2", 3), Claim("C", "AND", ("E1", "E2"))
        ])
        plan = g.plan_acquisition("C")
        self.assertEqual(plan.required_new_evidence, ("E1", "E2"))
        self.assertEqual(plan.total_cost, 5)

    def test_or_claim_chooses_cheapest(self):
        g = EvidenceGraph([
            Evidence("E1", 5), Evidence("E2", 1), Claim("C", "OR", ("E1", "E2"))
        ])
        plan = g.plan_acquisition("C")
        self.assertEqual(plan.required_new_evidence, ("E2",))
        self.assertEqual(plan.total_cost, 1)

    def test_shared_dependency_not_double_counted(self):
        g = EvidenceGraph([
            Evidence("A", 2), Evidence("B", 2), Evidence("C", 2),
            Claim("X", "AND", ("A", "B")),
            Claim("Y", "AND", ("A", "C")),
            Claim("T", "AND", ("X", "Y")),
        ])
        plan = g.plan_acquisition("T")
        self.assertEqual(plan.required_new_evidence, ("A", "B", "C"))
        self.assertEqual(plan.total_cost, 6)

    def test_proven_evidence_is_removed_from_plan(self):
        g = EvidenceGraph([Evidence("A", 2), Evidence("B", 3), Claim("T", "AND", ("A", "B"))])
        plan = g.plan_acquisition("T", proven_evidence=["A"])
        self.assertEqual(plan.required_new_evidence, ("B",))
        self.assertEqual(plan.total_cost, 3)

    def test_all_proven_returns_already_proven(self):
        g = EvidenceGraph([Evidence("A"), Claim("T", "OR", ("A",))])
        self.assertEqual(g.plan_acquisition("T", proven_evidence=["A"]).status, "ALREADY_PROVEN")

    def test_subset_superset_proofs_are_pruned(self):
        g = EvidenceGraph([
            Evidence("A"), Evidence("B"),
            Claim("AB", "AND", ("A", "B")),
            Claim("T", "OR", ("A", "AB")),
        ])
        frontier = g.proof_frontier("T")
        self.assertEqual(frontier, (frozenset({"A"}),))

    def test_exact_cutsets_for_alternative_proofs(self):
        g = EvidenceGraph([
            Evidence("A"), Evidence("B"), Evidence("C"),
            Claim("P1", "AND", ("A", "B")),
            Claim("P2", "AND", ("A", "C")),
            Claim("T", "OR", ("P1", "P2")),
        ])
        cuts = g.minimal_cutsets("T")
        self.assertEqual(cuts, (("A",), ("B", "C")))

    def test_cycle_rejected(self):
        with self.assertRaises(GraphError):
            EvidenceGraph([Claim("A", "OR", ("B",)), Claim("B", "OR", ("A",))])

    def test_unknown_child_rejected(self):
        with self.assertRaises(GraphError):
            EvidenceGraph([Claim("A", "OR", ("missing",))])

    def test_non_evidence_proven_id_rejected(self):
        g = EvidenceGraph([Evidence("A"), Claim("T", "OR", ("A",))])
        with self.assertRaises(GraphError):
            g.plan_acquisition("T", proven_evidence=["T"])

    def test_cutset_bound_is_fail_closed(self):
        leaves = [Evidence(f"E{i}") for i in range(8)]
        g = EvidenceGraph(leaves + [Claim("T", "OR", tuple(x.node_id for x in leaves))])
        with self.assertRaises(PlanningLimitExceeded):
            g.minimal_cutsets("T", max_enumerations=2)

    def test_fingerprint_order_independent_for_node_input(self):
        nodes_a = [Evidence("A", 2), Evidence("B", 1), Claim("T", "OR", ("A", "B"))]
        nodes_b = [Claim("T", "OR", ("B", "A")), Evidence("B", 1), Evidence("A", 2)]
        a = EvidenceGraph(nodes_a).plan_acquisition("T")
        b = EvidenceGraph(nodes_b).plan_acquisition("T")
        self.assertEqual(a.fingerprint, b.fingerprint)


if __name__ == "__main__":
    unittest.main()
