import unittest

from nexy_meta_assurance.spec_mutation import (
    Constraint,
    ConstraintOp,
    SpecMutationError,
    generate_illegal_mutations,
    run_mutation_sentinel,
    validate_spec,
)


class SpecMutationTests(unittest.TestCase):
    def setUp(self):
        self.spec = {
            "mode": "verify_only",
            "min_evidence": 2,
            "max_actions": 5,
            "authorities": ["user", "system"],
        }
        self.constraints = (
            Constraint("C1", "mode", ConstraintOp.EQ, "verify_only"),
            Constraint("C2", "min_evidence", ConstraintOp.MIN_INT, 2),
            Constraint("C3", "max_actions", ConstraintOp.MAX_INT, 5),
            Constraint("C4", "authorities", ConstraintOp.NONEMPTY),
        )

    def validator(self, spec):
        return not validate_spec(spec, self.constraints)

    def test_generated_mutations_are_all_rejected_by_strict_validator(self):
        report = run_mutation_sentinel(self.spec, self.constraints, self.validator)
        self.assertTrue(report.passed)
        self.assertEqual(len(report.generated), 4)
        self.assertEqual(len(report.killed), 4)
        self.assertEqual(report.survivors, ())

    def test_weak_validator_exposes_survivor(self):
        def weak(spec):
            return spec.get("mode") == "verify_only"

        report = run_mutation_sentinel(self.spec, self.constraints, weak)
        self.assertFalse(report.passed)
        self.assertGreaterEqual(len(report.survivors), 1)

    def test_invalid_baseline_fails_closed(self):
        bad = dict(self.spec)
        bad["min_evidence"] = 0
        with self.assertRaises(SpecMutationError):
            generate_illegal_mutations(bad, self.constraints)

    def test_missing_field_is_a_violation(self):
        bad = dict(self.spec)
        del bad["mode"]
        self.assertEqual(validate_spec(bad, self.constraints), ("C1",))

    def test_non_boolean_validator_result_fails_closed(self):
        with self.assertRaises(SpecMutationError):
            run_mutation_sentinel(self.spec, self.constraints, lambda spec: "yes")

    def test_duplicate_constraint_id_fails_closed(self):
        duplicate = self.constraints + (Constraint("C1", "mode", ConstraintOp.EQ, "verify_only"),)
        with self.assertRaises(SpecMutationError):
            validate_spec(self.spec, duplicate)


if __name__ == "__main__":
    unittest.main()
