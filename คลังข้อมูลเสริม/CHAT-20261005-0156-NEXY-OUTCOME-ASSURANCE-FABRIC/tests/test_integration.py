from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest

from nexy_outcome.compiler import compile_contract
from nexy_outcome.pipeline import run_outcome_pipeline

from common import contract_spec, good_observation


class IntegrationTests(unittest.TestCase):
    def test_five_engine_pipeline(self) -> None:
        baseline = good_observation()
        candidate = good_observation()
        candidate["metrics"]["availability"] = 99.0
        alternatives = [
            {"candidate_id": "baseline", "observation": baseline},
            {"candidate_id": "candidate", "observation": candidate},
        ]
        actions = [
            {
                "action_id": "restore-availability",
                "cost": 1,
                "risk": 0.01,
                "reversible": True,
                "effects": {"metrics.availability": 99.95},
            }
        ]
        result = run_outcome_pipeline(
            contract_spec(),
            baseline=baseline,
            candidate=candidate,
            alternatives=alternatives,
            recovery_actions=actions,
            max_cost=5,
            max_risk=0.2,
        )
        self.assertEqual(result["candidate_report"]["status"], "FAIL")
        self.assertEqual(result["frontier"]["frontier"], ["baseline"])
        self.assertEqual(result["benefit_regression"]["status"], "FAIL")
        self.assertEqual(result["recovery"]["status"], "PASS")
        self.assertEqual(result["recovery"]["plan"], ["restore-availability"])

    def test_cli_compile_and_verify(self) -> None:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.join(os.path.dirname(__file__), "..", "src")
        compile_payload = {"operation": "compile", "spec": contract_spec()}
        proc = subprocess.run(
            [sys.executable, "-m", "nexy_outcome.cli"],
            input=json.dumps(compile_payload),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        compiled = json.loads(proc.stdout)
        self.assertEqual(compiled["status"], "PASS")

        verify_payload = {
            "operation": "verify",
            "contract": compiled["contract"],
            "observation": good_observation(),
        }
        proc2 = subprocess.run(
            [sys.executable, "-m", "nexy_outcome.cli"],
            input=json.dumps(verify_payload),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(proc2.returncode, 0, proc2.stderr)
        verified = json.loads(proc2.stdout)
        self.assertEqual(verified["status"], "PASS")
        self.assertEqual(verified["contract_hash"], compiled["contract_hash"])

    def test_cli_malformed_freezes_closed(self) -> None:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.join(os.path.dirname(__file__), "..", "src")
        proc = subprocess.run(
            [sys.executable, "-m", "nexy_outcome.cli"],
            input='{"operation":"compile","spec":{"oops":true}}',
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        result = json.loads(proc.stdout)
        self.assertEqual(result["status"], "FREEZE")

    def test_100_replays_identical(self) -> None:
        contract, digest = compile_contract(contract_spec())
        self.assertTrue(digest)
        from nexy_outcome.verifier import verify_outcome
        reports = [json.dumps(verify_outcome(contract, good_observation()), sort_keys=True) for _ in range(100)]
        self.assertEqual(len(set(reports)), 1)


if __name__ == "__main__":
    unittest.main()
