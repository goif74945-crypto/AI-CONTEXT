import unittest

from nexy_lo4_lab.witness import (
    RequirementBoundaryWitnessEngine,
    RequirementSpec,
    WitnessError,
)


class RequirementBoundaryWitnessEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = RequirementBoundaryWitnessEngine()

    def test_max_generates_positive_negative_and_missing(self):
        spec = RequirementSpec("max-attempts", "attempts", "max", 5, True)
        witnesses = self.engine.generate(spec)
        self.assertEqual(tuple(w.kind for w in witnesses), ("positive", "negative", "missing"))
        for witness in witnesses:
            self.assertEqual(
                self.engine.evaluate(spec, witness.payload), witness.should_pass
            )

    def test_eq_witnesses_execute_as_declared(self):
        spec = RequirementSpec("mode", "mode", "eq", "safe")
        for witness in self.engine.generate(spec):
            self.assertEqual(self.engine.evaluate(spec, witness.payload), witness.should_pass)

    def test_in_witnesses_execute_as_declared(self):
        spec = RequirementSpec("tier", "tier", "in", ("E2", "E3"))
        for witness in self.engine.generate(spec):
            self.assertEqual(self.engine.evaluate(spec, witness.payload), witness.should_pass)

    def test_min_max_contradiction_detected(self):
        contradictions = self.engine.detect_contradictions(
            [
                RequirementSpec("min", "x", "min", 10),
                RequirementSpec("max", "x", "max", 5),
            ]
        )
        self.assertEqual(len(contradictions), 1)
        self.assertIn("minimum exceeds maximum", contradictions[0][2])

    def test_eq_neq_contradiction_detected(self):
        contradictions = self.engine.detect_contradictions(
            [
                RequirementSpec("eq", "mode", "eq", "safe"),
                RequirementSpec("neq", "mode", "neq", "safe"),
            ]
        )
        self.assertEqual(len(contradictions), 1)

    def test_wrong_runtime_type_fails_closed(self):
        spec = RequirementSpec("limit", "x", "max", 5)
        self.assertFalse(self.engine.evaluate(spec, {"x": "not-a-number"}))

    def test_non_finite_numeric_boundary_is_rejected(self):
        with self.assertRaisesRegex(WitnessError, "finite numeric boundary"):
            self.engine.generate(RequirementSpec("nan", "x", "min", float("nan")))

    def test_unsupported_operator_fails(self):
        with self.assertRaisesRegex(WitnessError, "unsupported operator"):
            self.engine.generate(RequirementSpec("x", "x", "regex", ".*"))


if __name__ == "__main__":
    unittest.main()
