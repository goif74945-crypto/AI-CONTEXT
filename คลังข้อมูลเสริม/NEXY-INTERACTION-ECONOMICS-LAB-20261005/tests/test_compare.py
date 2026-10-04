from __future__ import annotations

import unittest

from nexy_ixlab.compare import ComparisonVerdict, compare_plans
from nexy_ixlab.model import InteractionPlan


def plan(name, steps, score=100):
    return InteractionPlan.from_mapping({
        "name": name,
        "budget": {"max_friction_score": score, "max_blocking_touches": 10, "max_choice_bits": 20, "max_context_switches": 20, "max_wait_ms": 100000},
        "steps": steps,
    })


class CompareTests(unittest.TestCase):
    def test_clean_friction_reduction_is_improvement(self):
        baseline = plan("b", [{"id": "q", "kind": "clarification", "blocking": True, "justification": "needed"}])
        candidate = plan("c", [{"id": "auto", "kind": "automatic"}])
        r = compare_plans(baseline, candidate)
        self.assertEqual(r.verdict, ComparisonVerdict.IMPROVEMENT)
        self.assertLess(r.friction_delta, 0)

    def test_new_safety_error_forces_regression_even_if_friction_drops(self):
        baseline = plan("b", [
            {"id": "confirm", "kind": "confirmation", "guards_step_id": "delete", "required_by_law": True, "justification": "law"},
            {"id": "delete", "kind": "irreversible_action", "reversible": False},
        ])
        candidate = plan("c", [{"id": "delete", "kind": "irreversible_action", "reversible": False}])
        r = compare_plans(baseline, candidate)
        self.assertEqual(r.verdict, ComparisonVerdict.REGRESSION)
        self.assertIn("IXF-UNGUARDED-IRREVERSIBLE", r.new_error_codes)

    def test_tradeoff_is_mixed(self):
        baseline = plan("b", [
            {"id": "q", "kind": "clarification", "blocking": True, "justification": "needed"},
            {"id": "wait", "kind": "wait", "estimated_wait_ms": 1000},
        ])
        candidate = plan("c", [
            {"id": "q", "kind": "clarification", "blocking": False, "justification": "needed", "context_switches": 2},
        ])
        r = compare_plans(baseline, candidate)
        self.assertEqual(r.verdict, ComparisonVerdict.MIXED)

    def test_identical_plan_is_equivalent(self):
        p = plan("same", [{"id": "auto", "kind": "automatic"}])
        self.assertEqual(compare_plans(p, p).verdict, ComparisonVerdict.EQUIVALENT)


if __name__ == "__main__":
    unittest.main()
