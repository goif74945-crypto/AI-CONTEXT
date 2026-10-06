import importlib
import random
import unittest

from frontier_assurance_lab import Constraint, ConstraintEngine, FreezeError


def api(testcase):
    try:
        return importlib.import_module("muscle_input_assurance")
    except ModuleNotFoundError:
        testcase.fail("muscle_input_assurance implementation is missing")


def default_budget(testcase, **overrides):
    module = api(testcase)
    values = {
        "max_variables": 8,
        "max_domain_values": 32,
        "max_constraints": 32,
        "max_constraint_values": 64,
        "max_subset_checks": 4095,
    }
    values.update(overrides)
    return module.MuscleSearchBudget(**values)


class MuscleInputPositiveTests(unittest.TestCase):
    def test_valid_sat_is_delegated(self):
        module = api(self)
        result = module.MuscleInputAssurance().solve(
            {"mode": ("safe", "fast")},
            [Constraint("a", "mode", "NEQ", ("fast",))],
            default_budget(self),
        )
        self.assertEqual(result["status"], "SAT")
        self.assertEqual(result["original"]["final_domains"], {"mode": ["safe"]})

    def test_valid_unsat_preserves_minimum_core(self):
        module = api(self)
        constraints = [
            Constraint("a", "mode", "EQ", ("safe",)),
            Constraint("b", "mode", "EQ", ("fast",)),
        ]
        result = module.MuscleInputAssurance().solve(
            {"mode": ("safe", "fast")}, constraints, default_budget(self)
        )
        self.assertEqual(result["status"], "UNSAT")
        self.assertEqual(result["original"]["core_ids"], ["a", "b"])

    def test_budget_certificate_uses_all_variable_counts(self):
        module = api(self)
        constraints = [
            Constraint("a1", "a", "DENY", ("x",)),
            Constraint("a2", "a", "ALLOW", ("x",)),
            Constraint("a3", "a", "NEQ", ("y",)),
            Constraint("b1", "b", "DENY", ("m",)),
            Constraint("b2", "b", "ALLOW", ("m",)),
        ]
        result = module.MuscleInputAssurance().solve(
            {"a": ("x", "y"), "b": ("m", "n")},
            constraints,
            default_budget(self),
        )
        self.assertEqual(result["budget"]["subset_checks_upper_bound"], 10)
        self.assertEqual(result["budget"]["constraints_per_variable"], {"a": 3, "b": 2})

    def test_input_hash_distinguishes_same_original_result(self):
        module = api(self)
        domains = {"mode": ("safe", "fast")}
        left = [
            Constraint("a", "mode", "EQ", ("safe",)),
            Constraint("b", "mode", "EQ", ("fast",)),
            Constraint("c", "mode", "DENY", ("safe",)),
        ]
        right = [
            Constraint("a", "mode", "EQ", ("safe",)),
            Constraint("b", "mode", "EQ", ("fast",)),
            Constraint("c", "mode", "NEQ", ("safe",)),
        ]
        engine = module.MuscleInputAssurance()
        left_result = engine.solve(domains, left, default_budget(self))
        right_result = engine.solve(domains, right, default_budget(self))
        self.assertEqual(
            left_result["original"]["result_hash"], right_result["original"]["result_hash"]
        )
        self.assertNotEqual(left_result["input_hash"], right_result["input_hash"])


class MuscleInputNegativeTests(unittest.TestCase):
    def test_unknown_constraint_literal_rejected(self):
        module = api(self)
        with self.assertRaises(FreezeError):
            module.MuscleInputAssurance().solve(
                {"mode": ("safe", "fast")},
                [Constraint("typo", "mode", "NEQ", ("saef",))],
                default_budget(self),
            )

    def test_string_domain_collection_rejected(self):
        module = api(self)
        with self.assertRaises(FreezeError):
            module.MuscleInputAssurance().solve(
                {"mode": "safe"}, [], default_budget(self)
            )

    def test_duplicate_domain_value_rejected(self):
        module = api(self)
        with self.assertRaises(FreezeError):
            module.MuscleInputAssurance().solve(
                {"mode": ("safe", "safe")}, [], default_budget(self)
            )

    def test_blank_domain_value_rejected(self):
        module = api(self)
        with self.assertRaises(FreezeError):
            module.MuscleInputAssurance().solve(
                {"mode": ("safe", " ")}, [], default_budget(self)
            )

    def test_string_constraint_values_rejected(self):
        module = api(self)
        malformed = Constraint("a", "mode", "EQ", "x")
        with self.assertRaises(FreezeError):
            module.MuscleInputAssurance().solve(
                {"mode": ("x", "y")}, [malformed], default_budget(self)
            )

    def test_duplicate_constraint_value_rejected(self):
        module = api(self)
        duplicate = Constraint("a", "mode", "ALLOW", ("safe", "safe"))
        with self.assertRaises(FreezeError):
            module.MuscleInputAssurance().solve(
                {"mode": ("safe", "fast")}, [duplicate], default_budget(self)
            )

    def test_foreign_constraint_rejected(self):
        module = api(self)
        with self.assertRaises(FreezeError):
            module.MuscleInputAssurance().solve(
                {"mode": ("safe",)}, [object()], default_budget(self)
            )

    def test_generator_constraint_collection_rejected(self):
        module = api(self)
        generated = (item for item in [Constraint("a", "mode", "EQ", ("safe",))])
        with self.assertRaises(FreezeError):
            module.MuscleInputAssurance().solve(
                {"mode": ("safe",)}, generated, default_budget(self)
            )

    def test_duplicate_constraint_id_rejected(self):
        module = api(self)
        constraints = [
            Constraint("a", "mode", "EQ", ("safe",)),
            Constraint("a", "mode", "NEQ", ("fast",)),
        ]
        with self.assertRaises(FreezeError):
            module.MuscleInputAssurance().solve(
                {"mode": ("safe", "fast")}, constraints, default_budget(self)
            )

    def test_boolean_budget_rejected(self):
        module = api(self)
        with self.assertRaises(FreezeError):
            module.MuscleSearchBudget(True, 32, 32, 64, 4095)


class MuscleInputAdversarialTests(unittest.TestCase):
    def test_subset_search_budget_exhaustion_freezes(self):
        module = api(self)
        constraints = [
            Constraint(f"c{i}", "mode", "DENY", ("safe",)) for i in range(4)
        ]
        result = module.MuscleInputAssurance().solve(
            {"mode": ("safe", "fast")},
            constraints,
            default_budget(self, max_subset_checks=14),
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertIn("SUBSET_CHECK_BUDGET_EXCEEDED", result["gaps"])
        self.assertEqual(result["budget"]["subset_checks_upper_bound"], 15)

    def test_exact_subset_search_budget_boundary_is_admitted(self):
        module = api(self)
        constraints = [
            Constraint(f"c{i}", "mode", "DENY", ("safe",)) for i in range(4)
        ]
        result = module.MuscleInputAssurance().solve(
            {"mode": ("safe", "fast")},
            constraints,
            default_budget(self, max_subset_checks=15),
        )
        self.assertEqual(result["status"], "SAT")

    def test_domain_value_budget_exhaustion_freezes(self):
        module = api(self)
        result = module.MuscleInputAssurance().solve(
            {"mode": ("a", "b", "c")},
            [],
            default_budget(self, max_domain_values=2),
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertIn("DOMAIN_VALUE_BUDGET_EXCEEDED", result["gaps"])

    def test_constraint_value_budget_exhaustion_freezes(self):
        module = api(self)
        result = module.MuscleInputAssurance().solve(
            {"mode": ("a", "b", "c")},
            [Constraint("a", "mode", "ALLOW", ("a", "b", "c"))],
            default_budget(self, max_constraint_values=2),
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertIn("CONSTRAINT_VALUE_BUDGET_EXCEEDED", result["gaps"])

    def test_100_input_permutations_are_deterministic(self):
        module = api(self)
        constraints = [
            Constraint("a", "mode", "EQ", ("safe",)),
            Constraint("b", "mode", "EQ", ("fast",)),
            Constraint("c", "mode", "DENY", ("audit",)),
        ]
        domains = {"mode": ("safe", "fast", "audit")}
        engine = module.MuscleInputAssurance()
        expected = engine.solve(domains, constraints, default_budget(self))
        rng = random.Random(74945)
        for _ in range(100):
            sample = constraints[:]
            rng.shuffle(sample)
            self.assertEqual(engine.solve(domains, sample, default_budget(self)), expected)


class MuscleInputIntegrationTests(unittest.TestCase):
    def test_valid_result_matches_original_engine(self):
        module = api(self)
        domains = {"mode": ("safe", "fast")}
        constraints = [
            Constraint("a", "mode", "EQ", ("safe",)),
            Constraint("b", "mode", "EQ", ("fast",)),
        ]
        original = ConstraintEngine(domains).solve(constraints)
        assured = module.MuscleInputAssurance().solve(
            domains, constraints, default_budget(self)
        )
        self.assertEqual(assured["original"], original)

    def test_original_unknown_literal_sat_is_blocked(self):
        module = api(self)
        domains = {"mode": ("safe", "fast")}
        constraints = [Constraint("typo", "mode", "NEQ", ("saef",))]
        self.assertEqual(ConstraintEngine(domains).solve(constraints)["status"], "SAT")
        with self.assertRaises(FreezeError):
            module.MuscleInputAssurance().solve(
                domains, constraints, default_budget(self)
            )


if __name__ == "__main__":
    unittest.main()
