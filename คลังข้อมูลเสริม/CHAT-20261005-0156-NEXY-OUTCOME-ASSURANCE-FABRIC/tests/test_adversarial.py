from __future__ import annotations

import copy
import math
import unittest

from nexy_outcome.compiler import compile_contract, contract_from_dict
from nexy_outcome.errors import ContractValidationError, RecoveryPlanningError
from nexy_outcome.frontier import satisfaction_frontier
from nexy_outcome.recovery import plan_recovery
from nexy_outcome.verifier import verify_outcome

from common import contract_spec, good_observation


class AdversarialTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract, _ = compile_contract(contract_spec())

    def test_compiled_contract_unknown_field_rejected(self) -> None:
        payload = self.contract.to_dict()
        payload["hidden_authority"] = True
        with self.assertRaises(ContractValidationError):
            contract_from_dict(payload)

    def test_compiled_contract_missing_field_rejected(self) -> None:
        payload = self.contract.to_dict()
        del payload["objective"]
        with self.assertRaises(ContractValidationError):
            contract_from_dict(payload)

    def test_wrong_numeric_type_freezes_not_fails(self) -> None:
        obs = good_observation()
        obs["metrics"]["availability"] = "99.95"
        report = verify_outcome(self.contract, obs)
        self.assertEqual(report["status"], "FREEZE")
        self.assertEqual(report["invalid_observations"], ["metrics.availability"])
        self.assertEqual(report["hard_failures"], [])

    def test_nonfinite_observation_freezes(self) -> None:
        obs = good_observation()
        obs["metrics"]["latency_ms"] = math.inf
        report = verify_outcome(self.contract, obs)
        self.assertEqual(report["status"], "FREEZE")
        self.assertIn("metrics.latency_ms", report["invalid_observations"])

    def test_frontier_freeze_candidate_rejected(self) -> None:
        obs = good_observation()
        del obs["metrics"]["satisfaction"]
        result = satisfaction_frontier(self.contract, [{"candidate_id": "x", "observation": obs}])
        self.assertEqual(result["rejected"], [{"candidate_id": "x", "status": "FREEZE"}])

    def test_recovery_nan_cost_rejected(self) -> None:
        actions = [
            {
                "action_id": "bad",
                "cost": math.nan,
                "risk": 0.1,
                "reversible": True,
                "effects": {"metrics.availability": 100},
            }
        ]
        with self.assertRaises(RecoveryPlanningError):
            plan_recovery(self.contract, good_observation(), actions, max_cost=10, max_risk=0.5)

    def test_recovery_nan_budget_rejected(self) -> None:
        with self.assertRaises(RecoveryPlanningError):
            plan_recovery(self.contract, good_observation(), [], max_cost=math.nan, max_risk=0.5)

    def test_recovery_non_json_effect_rejected(self) -> None:
        actions = [
            {
                "action_id": "bad",
                "cost": 1,
                "risk": 0.1,
                "reversible": True,
                "effects": {"metrics.availability": object()},
            }
        ]
        with self.assertRaises(RecoveryPlanningError):
            plan_recovery(self.contract, good_observation(), actions, max_cost=10, max_risk=0.5)

    def test_recovery_conflicting_only_options_fail_closed(self) -> None:
        obs = good_observation()
        obs["metrics"]["availability"] = 99.0
        obs["metrics"]["latency_ms"] = 250
        actions = [
            {
                "action_id": "a",
                "cost": 1,
                "risk": 0.01,
                "reversible": True,
                "effects": {"metrics.availability": 99.95, "metrics.latency_ms": 260},
            },
            {
                "action_id": "b",
                "cost": 1,
                "risk": 0.01,
                "reversible": True,
                "effects": {"metrics.latency_ms": 180, "metrics.availability": 99.1},
            },
        ]
        result = plan_recovery(self.contract, obs, actions, max_cost=10, max_risk=0.5)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["reason"], "no_admissible_plan")

    def test_contract_hash_stable_through_roundtrip(self) -> None:
        original = self.contract.to_dict()
        rebuilt = contract_from_dict(copy.deepcopy(original))
        self.assertEqual(original, rebuilt.to_dict())


if __name__ == "__main__":
    unittest.main()
