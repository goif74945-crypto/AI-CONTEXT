import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'systems' / 'assumption_burndown_planner'))
from assumption_burndown_planner import Assumption, Probe, plan_burndown


class AssumptionBurndownPlannerTests(unittest.TestCase):
    def setUp(self):
        self.assumptions = [
            Assumption('schema-current', 5, 1.0, True),
            Assumption('endpoint-fast', 2, .5, False),
            Assumption('user-authorized', 5, .9, True),
        ]
        self.probes = [
            Probe('check-schema', frozenset({'schema-current'}), 1, .1),
            Probe('check-auth', frozenset({'user-authorized'}), 1, .1),
            Probe('benchmark', frozenset({'endpoint-fast'}), 5, .2),
            Probe('combined', frozenset({'schema-current', 'user-authorized'}), 1.5, .15),
        ]

    def test_covers_blockers_with_best_bounded_plan(self):
        result = plan_burndown(self.assumptions, self.probes, max_cost=2, max_risk=.3)
        self.assertEqual(result.status, 'PASS')
        self.assertEqual(result.probes, ('combined',))
        self.assertNotIn('schema-current', result.residual_assumptions)
        self.assertNotIn('user-authorized', result.residual_assumptions)

    def test_freezes_when_blocker_uncoverable(self):
        result = plan_burndown(self.assumptions, [self.probes[0]], max_cost=10, max_risk=10)
        self.assertEqual(result.status, 'FREEZE')

    def test_optional_probe_selected_if_budget_allows_and_adds_risk_burn(self):
        result = plan_burndown(self.assumptions, self.probes, max_cost=10, max_risk=1)
        self.assertEqual(result.status, 'PASS')
        self.assertIn('benchmark', result.probes)


if __name__ == '__main__':
    unittest.main()
