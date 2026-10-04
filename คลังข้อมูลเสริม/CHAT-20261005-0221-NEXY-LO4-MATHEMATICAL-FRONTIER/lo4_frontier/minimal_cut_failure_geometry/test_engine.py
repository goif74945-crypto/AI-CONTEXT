import unittest
from lo4_frontier.minimal_cut_failure_geometry.engine import minimal_failure_cut_sets

class MinimalCutTests(unittest.TestCase):
    def test_finds_minimal_hitting_sets(self):
        result = minimal_failure_cut_sets([{"a", "b"}, {"b", "c"}])
        self.assertEqual(result, (("b",), ("a", "c")))

    def test_rejects_empty_or_oversized_inputs(self):
        with self.assertRaises(ValueError):
            minimal_failure_cut_sets([])
        with self.assertRaises(ValueError):
            minimal_failure_cut_sets([set()])
        with self.assertRaises(ValueError):
            minimal_failure_cut_sets([{str(i) for i in range(21)}], max_nodes=20)

    def test_is_deterministic_under_input_order(self):
        a = minimal_failure_cut_sets([{"a", "b"}, {"b", "c"}])
        b = minimal_failure_cut_sets([{"c", "b"}, {"b", "a"}])
        self.assertEqual(a, b)
