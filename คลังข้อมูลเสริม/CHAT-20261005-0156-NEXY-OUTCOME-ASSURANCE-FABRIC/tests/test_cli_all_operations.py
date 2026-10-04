from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest

from nexy_outcome.compiler import compile_contract

from common import contract_spec, good_observation


class CliAllOperationsTests(unittest.TestCase):
    @staticmethod
    def _run(payload: dict) -> tuple[int, dict]:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.join(os.path.dirname(__file__), "..", "src")
        proc = subprocess.run(
            [sys.executable, "-m", "nexy_outcome"],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        return proc.returncode, json.loads(proc.stdout)

    def setUp(self) -> None:
        self.contract, _ = compile_contract(contract_spec())
        self.contract_dict = self.contract.to_dict()

    def test_frontier_cli(self) -> None:
        a = good_observation()
        b = good_observation()
        b["metrics"]["latency_ms"] = 190
        code, result = self._run(
            {
                "operation": "frontier",
                "contract": self.contract_dict,
                "candidates": [
                    {"candidate_id": "a", "observation": a},
                    {"candidate_id": "b", "observation": b},
                ],
            }
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["frontier"], ["a"])

    def test_regression_cli(self) -> None:
        baseline = good_observation()
        candidate = good_observation()
        candidate["metrics"]["latency_ms"] = 195
        code, result = self._run(
            {
                "operation": "regression",
                "contract": self.contract_dict,
                "baseline": baseline,
                "candidate": candidate,
            }
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["regressions"][0]["criterion_id"], "latency")

    def test_recovery_cli(self) -> None:
        observation = good_observation()
        observation["metrics"]["availability"] = 99.0
        code, result = self._run(
            {
                "operation": "recover",
                "contract": self.contract_dict,
                "observation": observation,
                "actions": [
                    {
                        "action_id": "restore",
                        "cost": 1,
                        "risk": 0.01,
                        "reversible": True,
                        "effects": {"metrics.availability": 99.95},
                    }
                ],
                "max_cost": 5,
                "max_risk": 0.2,
            }
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["plan"], ["restore"])

    def test_unknown_operation_freezes(self) -> None:
        code, result = self._run({"operation": "mystery", "contract": self.contract_dict})
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "FREEZE")


if __name__ == "__main__":
    unittest.main()
