from __future__ import annotations

import itertools
import unittest

from nexy_outcome.compiler import compile_contract
from nexy_outcome.frontier import satisfaction_frontier
from nexy_outcome.regression import benefit_regression_guard
from nexy_outcome.verifier import verify_outcome

from common import contract_spec, good_observation


class PropertyStyleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract, _ = compile_contract(contract_spec())

    def test_hard_failure_always_dominates_soft_success(self) -> None:
        for latency, satisfaction in itertools.product([100, 180], [8.5, 10.0]):
            obs = good_observation()
            obs["metrics"].update(
                availability=99.0,
                latency_ms=latency,
                satisfaction=satisfaction,
            )
            self.assertEqual(verify_outcome(self.contract, obs)["status"], "FAIL")

    def test_forbidden_effect_always_fails_when_observed_true(self) -> None:
        for availability in [99.9, 100.0]:
            obs = good_observation()
            obs["metrics"]["availability"] = availability
            obs["effects"]["data_loss"] = True
            self.assertEqual(verify_outcome(self.contract, obs)["status"], "FAIL")

    def test_frontier_never_contains_rejected_candidate(self) -> None:
        good = good_observation()
        bad = good_observation()
        bad["metrics"]["availability"] = 0
        result = satisfaction_frontier(
            self.contract,
            [
                {"candidate_id": "good", "observation": good},
                {"candidate_id": "bad", "observation": bad},
            ],
        )
        rejected_ids = {x["candidate_id"] for x in result["rejected"]}
        self.assertTrue(set(result["frontier"]).isdisjoint(rejected_ids))

    def test_guard_is_not_fooled_by_soft_score_improvement(self) -> None:
        baseline = good_observation()
        for satisfaction in [9.0, 9.5, 10.0]:
            candidate = good_observation()
            candidate["metrics"]["latency_ms"] = 195
            candidate["metrics"]["satisfaction"] = satisfaction
            result = benefit_regression_guard(self.contract, baseline, candidate)
            self.assertEqual(result["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
