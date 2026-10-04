from __future__ import annotations

import unittest

from concepts.failure_atomizer.atomizer import ddmin


class FailureAtomizerTests(unittest.TestCase):
    def test_minimizes_trigger_pair(self) -> None:
        items = ("noise1", "A", "noise2", "B", "noise3")
        result = ddmin(items, lambda xs: "A" in xs and "B" in xs)
        self.assertEqual(result.status, "MINIMIZED_1_MINIMAL")
        self.assertEqual(set(result.minimal), {"A", "B"})
        self.assertEqual(len(result.minimal), 2)

    def test_baseline_not_failing_is_explicit(self) -> None:
        r = ddmin([1, 2, 3], lambda xs: 99 in xs)
        self.assertEqual(r.status, "BASELINE_NOT_FAILING")

    def test_empty_failure_is_explicit(self) -> None:
        r = ddmin([1, 2], lambda xs: True)
        self.assertEqual(r.status, "EMPTY_CAUSES_FAILURE")
        self.assertEqual(r.minimal, ())

    def test_deterministic(self) -> None:
        pred = lambda xs: 3 in xs and 7 in xs
        a = ddmin(tuple(range(10)), pred)
        b = ddmin(tuple(range(10)), pred)
        self.assertEqual(a.as_dict(), b.as_dict())

    def test_result_is_explicitly_one_minimal(self) -> None:
        r = ddmin(("x", "A", "B", "y", "C"), lambda xs: ("A" in xs and "B" in xs) or ("C" in xs and len(xs) > 3))
        self.assertTrue("A" in r.minimal and "B" in r.minimal)
        for i in range(len(r.minimal)):
            candidate = r.minimal[:i] + r.minimal[i+1:]
            self.assertFalse(("A" in candidate and "B" in candidate) or ("C" in candidate and len(candidate) > 3))

    def test_duplicate_values_and_order_sensitive_predicate(self) -> None:
        items = ("A", "B", "A", "C", "D")
        r = ddmin(items, lambda xs: tuple(xs[-2:]) == ("C", "D"))
        self.assertEqual(r.minimal, ("C", "D"))

    def test_budget_exhaustion_fails_closed(self) -> None:
        with self.assertRaises(RuntimeError):
            ddmin(range(20), lambda xs: 2 in xs and 19 in xs, max_evaluations=1)


if __name__ == "__main__":
    unittest.main()
