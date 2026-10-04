import copy
import unittest
from src import Mutator, evaluate_gate


class AcceptanceMutationSentinelTests(unittest.TestCase):
    def test_strong_gate_kills_critical_mutations(self):
        baseline = {"status": "PASS", "evidence": "abc", "verified": True}
        mutators = [
            Mutator("flip-status", lambda x: {**x, "status": "FAIL"}),
            Mutator("erase-evidence", lambda x: {**x, "evidence": ""}),
            Mutator("unset-verified", lambda x: {**x, "verified": False}),
        ]
        gate = lambda x: x["status"] == "PASS" and bool(x["evidence"]) and x["verified"] is True
        report = evaluate_gate(baseline, gate, mutators)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["kill_rate"], 1.0)
        self.assertEqual(report["survivors"], [])

    def test_weak_gate_exposes_surviving_mutation(self):
        baseline = {"status": "PASS", "evidence": "abc"}
        mutators = [Mutator("erase-evidence", lambda x: {**x, "evidence": ""})]
        gate = lambda x: x["status"] == "PASS"
        report = evaluate_gate(baseline, gate, mutators)
        self.assertEqual(report["status"], "WEAK_GATE")
        self.assertEqual(report["survivors"], ["erase-evidence"])

    def test_baseline_rejection_is_configuration_error(self):
        baseline = {"status": "FAIL"}
        report = evaluate_gate(baseline, lambda x: x["status"] == "PASS", [])
        self.assertEqual(report["status"], "INVALID_BASELINE")

    def test_no_mutators_is_not_verified(self):
        baseline = {"status": "PASS"}
        report = evaluate_gate(baseline, lambda x: x["status"] == "PASS", [])
        self.assertEqual(report["status"], "NOT_VERIFIED")

    def test_mutator_must_not_modify_baseline_in_place(self):
        baseline = {"nested": {"value": 1}}
        def mutates_in_place(x):
            x["nested"]["value"] = 2
            return x
        report = evaluate_gate(
            baseline,
            lambda _: True,
            [Mutator("in-place", mutates_in_place)],
        )
        self.assertEqual(baseline, {"nested": {"value": 1}})
        self.assertEqual(report["survivors"], ["in-place"])


if __name__ == "__main__":
    unittest.main()
