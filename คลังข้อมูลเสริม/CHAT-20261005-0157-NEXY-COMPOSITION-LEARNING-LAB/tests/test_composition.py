import unittest

from nexy_aux.composition import compose


class CompositionTests(unittest.TestCase):
    def test_composes_assume_guarantee_chain(self):
        components = [
            {"id": "judge", "assumptions": ["evidence_valid"], "guarantees": ["release_eligible"]},
            {"id": "verify", "assumptions": ["input_valid"], "guarantees": ["evidence_valid"]},
        ]
        result = compose(components, ["input_valid"])
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["admitted_order"], ["verify", "judge"])
        self.assertIn("release_eligible", result["facts"])

    def test_component_input_order_does_not_change_result(self):
        a = {"id": "a", "assumptions": ["root"], "guarantees": ["a_ok"]}
        b = {"id": "b", "assumptions": ["root"], "guarantees": ["b_ok"]}
        r1 = compose([a, b], ["root"])
        r2 = compose([b, a], ["root"])
        self.assertEqual(r1, r2)

    def test_freezes_on_unsatisfied_assumption(self):
        result = compose([{"id": "x", "assumptions": ["missing"], "guarantees": ["ok"]}], [])
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "UNSATISFIED_ASSUMPTIONS")
        self.assertEqual(result["unresolved"]["x"]["missing_assumptions"], ["missing"])

    def test_reports_contradicted_assumption(self):
        result = compose([{"id": "x", "assumptions": ["safe"], "guarantees": ["ok"]}], ["!safe"])
        self.assertEqual(result["unresolved"]["x"]["contradicted_assumptions"], ["safe"])

    def test_freezes_on_cross_component_contradiction(self):
        result = compose([
            {"id": "a", "assumptions": ["root"], "guarantees": ["safe"]},
            {"id": "b", "assumptions": ["root"], "guarantees": ["!safe"]},
        ], ["root"])
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "CONTRADICTORY_GUARANTEE")

    def test_rejects_duplicate_ids(self):
        with self.assertRaises(ValueError):
            compose([{"id": "x"}, {"id": "x"}], [])


if __name__ == "__main__":
    unittest.main()
