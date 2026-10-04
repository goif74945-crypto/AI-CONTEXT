from __future__ import annotations

import unittest

from nexy_outcome.compiler import compile_contract
from nexy_outcome.errors import RecoveryPlanningError
from nexy_outcome.recovery import plan_recovery

from common import contract_spec, good_observation


class RecoveryPlannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract, _ = compile_contract(contract_spec())

    def test_selects_minimum_cost_valid_plan(self) -> None:
        obs = good_observation()
        obs["metrics"]["availability"] = 99.0
        actions = [
            {
                "action_id": "expensive",
                "cost": 10,
                "risk": 0.01,
                "reversible": True,
                "effects": {"metrics.availability": 99.99},
            },
            {
                "action_id": "cheap-a",
                "cost": 2,
                "risk": 0.02,
                "reversible": True,
                "effects": {"metrics.availability": 99.95},
            },
        ]
        result = plan_recovery(self.contract, obs, actions, max_cost=20, max_risk=0.2)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["plan"], ["cheap-a"])

    def test_combines_complementary_actions(self) -> None:
        obs = good_observation()
        obs["metrics"]["availability"] = 99.0
        obs["metrics"]["latency_ms"] = 250
        actions = [
            {
                "action_id": "availability-fix",
                "cost": 2,
                "risk": 0.02,
                "reversible": True,
                "effects": {"metrics.availability": 99.95},
            },
            {
                "action_id": "latency-fix",
                "cost": 3,
                "risk": 0.03,
                "reversible": True,
                "effects": {"metrics.latency_ms": 180},
            },
        ]
        result = plan_recovery(self.contract, obs, actions, max_cost=10, max_risk=0.2)
        self.assertEqual(result["plan"], ["availability-fix", "latency-fix"])

    def test_rejects_irreversible_when_required(self) -> None:
        obs = good_observation()
        obs["metrics"]["availability"] = 99.0
        result = plan_recovery(
            self.contract,
            obs,
            [
                {
                    "action_id": "irreversible",
                    "cost": 1,
                    "risk": 0.01,
                    "reversible": False,
                    "effects": {"metrics.availability": 100},
                }
            ],
            max_cost=5,
            max_risk=0.2,
            require_reversible=True,
        )
        self.assertEqual(result["status"], "FAIL")

    def test_conflicting_actions_not_combined(self) -> None:
        obs = good_observation()
        obs["metrics"]["availability"] = 99.0
        obs["metrics"]["latency_ms"] = 250
        actions = [
            {"action_id": "a", "cost": 1, "risk": 0.01, "reversible": True, "effects": {"metrics.availability": 99.95, "metrics.latency_ms": 180}},
            {"action_id": "b", "cost": 1, "risk": 0.01, "reversible": True, "effects": {"metrics.latency_ms": 170}},
        ]
        result = plan_recovery(self.contract, obs, actions, max_cost=5, max_risk=0.2)
        self.assertEqual(result["plan"], ["a"])

    def test_exact_search_limit(self) -> None:
        obs = good_observation()
        actions = [
            {"action_id": f"a{i}", "cost": 1, "risk": 0.0, "reversible": True, "effects": {f"x.v{i}": i}}
            for i in range(17)
        ]
        with self.assertRaises(RecoveryPlanningError):
            plan_recovery(self.contract, obs, actions, max_cost=100, max_risk=1)


if __name__ == "__main__":
    unittest.main()
