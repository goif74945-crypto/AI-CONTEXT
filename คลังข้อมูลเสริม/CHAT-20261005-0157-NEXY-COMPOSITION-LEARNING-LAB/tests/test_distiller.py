import unittest

from nexy_aux.distiller import distill


class DistillerTests(unittest.TestCase):
    def test_distills_to_one_minimal_counterexample(self):
        items = ["noise1", "A", "noise2", "B", "noise3"]

        def oracle(candidate):
            return "FAIL_AB" if "A" in candidate and "B" in candidate else None

        result = distill(items, oracle, "FAIL_AB")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["minimal_items"], ["A", "B"])
        self.assertTrue(result["one_minimal"])

    def test_freezes_when_original_does_not_reproduce(self):
        result = distill([1, 2, 3], lambda _: None, "X")
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "TARGET_SIGNATURE_NOT_REPRODUCED")

    def test_handles_single_element_failure(self):
        result = distill(["A"], lambda xs: "X" if "A" in xs else None, "X")
        self.assertEqual(result["minimal_items"], ["A"])
        self.assertTrue(result["one_minimal"])

    def test_can_reduce_to_empty_if_empty_still_fails(self):
        result = distill(["A", "B"], lambda _: "X", "X")
        self.assertEqual(result["minimal_items"], [])
        self.assertTrue(result["one_minimal"])


if __name__ == "__main__":
    unittest.main()
