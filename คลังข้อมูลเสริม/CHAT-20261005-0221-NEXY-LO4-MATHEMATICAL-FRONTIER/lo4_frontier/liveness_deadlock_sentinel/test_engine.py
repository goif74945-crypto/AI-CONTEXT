import unittest
from lo4_frontier.liveness_deadlock_sentinel.engine import analyze_liveness

class LivenessTests(unittest.TestCase):
    def test_detects_deadlock_cycle(self):
        items = [
            {"id":"a","state":"WAITING","waits_for":["b"]},
            {"id":"b","state":"WAITING","waits_for":["a"]},
        ]
        result = analyze_liveness(items)
        self.assertEqual(result["status"], "DEADLOCK")
        self.assertEqual(result["cycles"], (("a","b"),))

    def test_detects_starvation_risk_without_cycle(self):
        items = [
            {"id":"a","state":"WAITING","waits_for":["b"]},
            {"id":"b","state":"BLOCKED","waits_for":[]},
        ]
        self.assertEqual(analyze_liveness(items)["status"], "STARVATION_RISK")

    def test_progressable_and_quiescent(self):
        self.assertEqual(analyze_liveness([{"id":"a","state":"READY","waits_for":[]}])["status"], "PROGRESSABLE")
        self.assertEqual(analyze_liveness([{"id":"a","state":"PASS","waits_for":[]}])["status"], "QUIESCENT")

    def test_rejects_unknown_dependency(self):
        with self.assertRaises(ValueError):
            analyze_liveness([{"id":"a","state":"WAITING","waits_for":["missing"]}])

class LivenessScaleRegressionTests(unittest.TestCase):
    def test_large_cycle_does_not_depend_on_python_recursion_limit(self):
        size = 1500
        items = [
            {"id": f"n{i}", "state": "WAITING", "waits_for": [f"n{(i + 1) % size}"]}
            for i in range(size)
        ]
        result = analyze_liveness(items)
        self.assertEqual(result["status"], "DEADLOCK")
        self.assertEqual(len(result["cycles"]), 1)
        self.assertEqual(len(result["cycles"][0]), size)
