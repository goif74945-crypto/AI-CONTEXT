from __future__ import annotations

import unittest

from nexy_outcome.compiler import compile_contract
from nexy_outcome.regression import benefit_regression_guard

from common import contract_spec, good_observation


class RegressionGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract, _ = compile_contract(contract_spec())

    def test_catches_guarded_regression_even_if_weighted_score_stays_high(self) -> None:
        baseline = good_observation()
        candidate = good_observation()
        candidate["metrics"]["latency_ms"] = 195  # +15, beyond allowed +10
        candidate["metrics"]["satisfaction"] = 9.8
        result = benefit_regression_guard(self.contract, baseline, candidate)
        self.assertEqual(result["candidate_status"], "PASS")
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["regressions"][0]["criterion_id"], "latency")

    def test_allows_bounded_regression(self) -> None:
        baseline = good_observation()
        candidate = good_observation()
        candidate["metrics"]["latency_ms"] = 189
        result = benefit_regression_guard(self.contract, baseline, candidate)
        self.assertEqual(result["status"], "PASS")

    def test_missing_data_freezes(self) -> None:
        baseline = good_observation()
        candidate = good_observation()
        del candidate["metrics"]["satisfaction"]
        result = benefit_regression_guard(self.contract, baseline, candidate)
        self.assertEqual(result["status"], "FREEZE")


if __name__ == "__main__":
    unittest.main()
