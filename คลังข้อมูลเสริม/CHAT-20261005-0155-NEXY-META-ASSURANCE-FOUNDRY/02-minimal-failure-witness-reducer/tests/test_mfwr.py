import os
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from mfwr import (
    EvaluationLimitExceeded,
    InitialCaseDoesNotFail,
    OracleUnstableError,
    ReductionError,
    reduce_failure,
)


class MinimalFailureWitnessReducerTests(unittest.TestCase):
    def test_reduces_to_required_pair(self):
        items = ["noise-1", "A", "noise-2", "B", "noise-3"]
        result = reduce_failure(items, lambda xs: "A" in xs and "B" in xs)
        self.assertEqual(result.witness, ("A", "B"))
        self.assertEqual(result.status, "ONE_MINIMAL")

    def test_preserves_order_of_witness(self):
        items = [1, 2, 3, 4, 5]
        result = reduce_failure(items, lambda xs: tuple(xs).index(2) < tuple(xs).index(5) if 2 in xs and 5 in xs else False)
        self.assertEqual(result.witness, (2, 5))

    def test_single_required_element(self):
        result = reduce_failure(["x", "boom", "y"], lambda xs: "boom" in xs)
        self.assertEqual(result.witness, ("boom",))

    def test_empty_witness_is_valid_when_empty_case_fails(self):
        result = reduce_failure([1, 2, 3], lambda xs: True)
        self.assertEqual(result.witness, ())

    def test_initial_non_failure_is_rejected(self):
        with self.assertRaises(InitialCaseDoesNotFail):
            reduce_failure([1, 2], lambda xs: False)

    def test_unstable_oracle_is_detected(self):
        calls = {"n": 0}
        def unstable(_):
            calls["n"] += 1
            return calls["n"] % 2 == 1
        with self.assertRaises(OracleUnstableError):
            reduce_failure([1], unstable)

    def test_budget_exhaustion_is_explicit(self):
        with self.assertRaises(EvaluationLimitExceeded):
            reduce_failure(list(range(20)), lambda xs: len(xs) >= 10, max_evaluations=2)

    def test_non_json_items_rejected(self):
        with self.assertRaises(ReductionError):
            reduce_failure([object()], lambda xs: True)

    def test_fingerprint_is_deterministic(self):
        oracle = lambda xs: "x" in xs
        a = reduce_failure(["a", "x", "b"], oracle)
        b = reduce_failure(["a", "x", "b"], oracle)
        self.assertEqual(a.witness_fingerprint, b.witness_fingerprint)
        self.assertEqual(a.original_fingerprint, b.original_fingerprint)

    def test_result_is_one_minimal_for_multi_condition(self):
        def fails(xs):
            s = set(xs)
            return ({"a", "b"} <= s) or ({"c", "d", "e"} <= s)
        result = reduce_failure(["n", "a", "b", "c", "d", "e"], fails)
        self.assertTrue(fails(result.witness))
        for i in range(len(result.witness)):
            candidate = result.witness[:i] + result.witness[i + 1 :]
            self.assertFalse(fails(candidate))


if __name__ == "__main__":
    unittest.main()
