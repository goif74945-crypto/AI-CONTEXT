import unittest

from ticm import TraceInvariantCandidateMiner


class TraceInvariantCandidateMinerTests(unittest.TestCase):
    def test_mines_candidates_but_does_not_promote_them_to_law(self):
        train = [
            {"phase": "verify", "step": 1, "workers": 3},
            {"phase": "verify", "step": 2, "workers": 4},
            {"phase": "verify", "step": 3, "workers": 5},
        ]
        result = TraceInvariantCandidateMiner.mine(train)
        self.assertTrue(all(c.status == "CANDIDATE_NOT_VERIFIED" for c in result))
        self.assertTrue(any(c.kind == "constant" and c.field == "phase" for c in result))
        self.assertTrue(any(c.kind == "nondecreasing" and c.field == "step" for c in result))

    def test_holdout_refutes_false_monotonic_candidate(self):
        train = [{"step": 1}, {"step": 2}, {"step": 3}]
        holdout = [{"step": 4}, {"step": 2}]
        result = TraceInvariantCandidateMiner.mine(train, holdout)
        mono = next(c for c in result if c.kind == "nondecreasing" and c.field == "step")
        self.assertEqual(mono.status, "REFUTED_BY_HOLDOUT")
        self.assertEqual(mono.holdout_violations, 1)

    def test_constant_candidate_can_be_supported_by_holdout(self):
        train = [{"mode": "safe"}, {"mode": "safe"}]
        holdout = [{"mode": "safe"}, {"mode": "safe"}]
        result = TraceInvariantCandidateMiner.mine(train, holdout)
        constant = next(c for c in result if c.kind == "constant")
        self.assertEqual(constant.status, "SUPPORTED_BY_HOLDOUT")
        self.assertEqual(constant.holdout_violations, 0)

    def test_requires_multiple_training_records(self):
        with self.assertRaises(ValueError):
            TraceInvariantCandidateMiner.mine([{"x": 1}])


if __name__ == "__main__":
    unittest.main()
