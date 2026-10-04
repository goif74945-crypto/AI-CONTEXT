from __future__ import annotations

import unittest

from nexy_outcome.compiler import compile_contract
from nexy_outcome.frontier import satisfaction_frontier

from common import contract_spec, good_observation


class FrontierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract, _ = compile_contract(contract_spec())

    def test_pareto_frontier_preserves_tradeoffs(self) -> None:
        a = good_observation()
        a["metrics"]["latency_ms"] = 150
        a["metrics"]["satisfaction"] = 8.1
        b = good_observation()
        b["metrics"]["latency_ms"] = 180
        b["metrics"]["satisfaction"] = 9.0
        c = good_observation()
        c["metrics"]["latency_ms"] = 190
        c["metrics"]["satisfaction"] = 8.2
        result = satisfaction_frontier(
            self.contract,
            [
                {"candidate_id": "a", "observation": a},
                {"candidate_id": "b", "observation": b},
                {"candidate_id": "c", "observation": c},
            ],
        )
        self.assertEqual(result["frontier"], ["a", "b"])
        self.assertEqual(result["dominated_by"]["c"], ["b"])

    def test_hard_failure_rejected(self) -> None:
        bad = good_observation()
        bad["metrics"]["availability"] = 90
        result = satisfaction_frontier(
            self.contract,
            [{"candidate_id": "bad", "observation": bad}],
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["rejected"], [{"candidate_id": "bad", "status": "FAIL"}])

    def test_duplicate_candidate_rejected(self) -> None:
        with self.assertRaises(Exception):
            satisfaction_frontier(
                self.contract,
                [
                    {"candidate_id": "x", "observation": good_observation()},
                    {"candidate_id": "x", "observation": good_observation()},
                ],
            )


if __name__ == "__main__":
    unittest.main()
