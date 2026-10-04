import unittest
from src import bisect_divergence, canonical_step_hash


class DeterminismDivergenceBisectorTests(unittest.TestCase):
    def test_volatile_keys_do_not_create_false_divergence(self):
        a = {"id": "s1", "output": {"value": 3}, "timestamp": "a"}
        b = {"id": "s1", "output": {"value": 3}, "timestamp": "b"}
        self.assertEqual(canonical_step_hash(a), canonical_step_hash(b))

    def test_finds_first_real_divergence_and_dependency_frontier(self):
        left = [
            {"id": "s1", "deps": [], "output": 1},
            {"id": "s2", "deps": ["s1"], "output": 2},
            {"id": "s3", "deps": ["s2"], "output": 3},
        ]
        right = [
            {"id": "s1", "deps": [], "output": 1},
            {"id": "s2", "deps": ["s1"], "output": 99},
            {"id": "s3", "deps": ["s2"], "output": 3},
        ]
        report = bisect_divergence(left, right)
        self.assertEqual(report["status"], "DIVERGED")
        self.assertEqual(report["first_index"], 1)
        self.assertEqual(report["step_id"], "s2")
        self.assertEqual(report["dependency_frontier"], ["s1"])

    def test_identical_traces_pass(self):
        trace = [{"id": "a", "deps": [], "output": {"x": 1}}]
        self.assertEqual(bisect_divergence(trace, trace)["status"], "EQUIVALENT")

    def test_length_divergence_is_reported(self):
        left = [{"id": "a", "deps": [], "output": 1}]
        right = left + [{"id": "b", "deps": ["a"], "output": 2}]
        report = bisect_divergence(left, right)
        self.assertEqual(report["first_index"], 1)
        self.assertEqual(report["reason"], "TRACE_LENGTH")


if __name__ == "__main__":
    unittest.main()
