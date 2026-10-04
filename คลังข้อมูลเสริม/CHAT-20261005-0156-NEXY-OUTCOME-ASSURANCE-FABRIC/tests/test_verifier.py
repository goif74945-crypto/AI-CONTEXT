from __future__ import annotations

import copy
import unittest

from nexy_outcome.compiler import compile_contract
from nexy_outcome.verifier import verify_outcome

from common import contract_spec, good_observation


class VerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract, _ = compile_contract(contract_spec())

    def test_pass(self) -> None:
        report = verify_outcome(self.contract, good_observation())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["soft_score"], 1.0)

    def test_missing_observation_freezes(self) -> None:
        obs = good_observation()
        del obs["effects"]["data_loss"]
        report = verify_outcome(self.contract, obs)
        self.assertEqual(report["status"], "FREEZE")
        self.assertIn("effects.data_loss", report["missing_observations"])

    def test_hard_failure_fails(self) -> None:
        obs = good_observation()
        obs["metrics"]["availability"] = 99.0
        report = verify_outcome(self.contract, obs)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("availability", report["hard_failures"])

    def test_soft_failure_partial(self) -> None:
        obs = good_observation()
        obs["metrics"]["latency_ms"] = 250
        report = verify_outcome(self.contract, obs)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual(report["soft_score"], 3 / 5)

    def test_forbidden_effect_fails(self) -> None:
        obs = good_observation()
        obs["effects"]["data_loss"] = True
        report = verify_outcome(self.contract, obs)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["forbidden_violations"][0]["effect_id"], "no_data_loss")

    def test_report_hash_stable(self) -> None:
        obs = good_observation()
        hashes = {verify_outcome(self.contract, copy.deepcopy(obs))["report_hash"] for _ in range(20)}
        self.assertEqual(len(hashes), 1)


if __name__ == "__main__":
    unittest.main()
