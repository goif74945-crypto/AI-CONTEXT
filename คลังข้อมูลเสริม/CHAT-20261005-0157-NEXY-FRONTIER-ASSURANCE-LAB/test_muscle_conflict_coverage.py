import importlib
import random
import unittest

from frontier_assurance_lab import Constraint, FreezeError
from muscle_input_assurance import MuscleInputAssurance, MuscleSearchBudget


def api(testcase):
    try:
        return importlib.import_module("muscle_conflict_coverage")
    except ModuleNotFoundError:
        testcase.fail("muscle_conflict_coverage implementation is missing")


def budget():
    return MuscleSearchBudget(
        max_variables=8,
        max_domain_values=32,
        max_constraints=32,
        max_constraint_values=64,
        max_subset_checks=4095,
    )


def contract(testcase, **overrides):
    module = api(testcase)
    values = {"max_cores_per_variable": 64, "max_total_cores": 128}
    values.update(overrides)
    return module.ConflictCoverageContract(**values)


def independent_conflicts():
    return {
        "domains": {"a": ("safe", "fast"), "b": ("on", "off")},
        "constraints": [
            Constraint("a-fast", "a", "EQ", ("fast",)),
            Constraint("a-safe", "a", "EQ", ("safe",)),
            Constraint("b-off", "b", "EQ", ("off",)),
            Constraint("b-on", "b", "EQ", ("on",)),
        ],
    }


class ConflictCoveragePositiveTests(unittest.TestCase):
    def test_reports_every_independently_unsat_variable(self):
        request = independent_conflicts()
        result = api(self).MuscleConflictCoverageAssurance().assess(
            request["domains"], request["constraints"], budget(), contract(self)
        )
        self.assertEqual(result["status"], "UNSAT")
        self.assertEqual(result["reason"], "EXHAUSTIVE_MINIMUM_CONFLICT_COVERAGE")
        self.assertEqual(result["unsat_variables"], ["a", "b"])
        self.assertEqual(set(result["conflict_families"]), {"a", "b"})

    def test_reports_all_alternate_minimum_cores(self):
        constraints = [
            Constraint("deny-a", "mode", "DENY", ("a",)),
            Constraint("deny-b", "mode", "DENY", ("b",)),
            Constraint("eq-a", "mode", "EQ", ("a",)),
            Constraint("eq-b", "mode", "EQ", ("b",)),
        ]
        result = api(self).MuscleConflictCoverageAssurance().assess(
            {"mode": ("a", "b")}, constraints, budget(), contract(self)
        )
        cores = [item["core_ids"] for item in result["conflict_families"]["mode"]["cores"]]
        self.assertEqual(
            cores,
            [
                ["deny-a", "deny-b"],
                ["deny-a", "eq-a"],
                ["deny-b", "eq-b"],
                ["eq-a", "eq-b"],
            ],
        )

    def test_each_core_has_satisfiable_deletion_witnesses(self):
        request = independent_conflicts()
        result = api(self).MuscleConflictCoverageAssurance().assess(
            request["domains"], request["constraints"], budget(), contract(self)
        )
        for family in result["conflict_families"].values():
            for core in family["cores"]:
                self.assertEqual(
                    [item["removed"] for item in core["deletion_witnesses"]],
                    core["core_ids"],
                )
                self.assertTrue(
                    all(item["remaining_domain"] for item in core["deletion_witnesses"])
                )

    def test_sat_input_has_bound_empty_coverage(self):
        result = api(self).MuscleConflictCoverageAssurance().assess(
            {"mode": ("safe", "fast")},
            [Constraint("safe", "mode", "EQ", ("safe",))],
            budget(),
            contract(self),
        )
        self.assertEqual(result["status"], "SAT")
        self.assertEqual(result["reason"], "NO_CONFLICTS")
        self.assertEqual(result["conflict_families"], {})
        self.assertRegex(result["coverage_hash"], r"^[0-9a-f]{64}$")


class ConflictCoverageNegativeTests(unittest.TestCase):
    def test_boolean_core_limit_rejected(self):
        module = api(self)
        with self.assertRaises(FreezeError):
            module.ConflictCoverageContract(True, 4)

    def test_foreign_contract_rejected(self):
        request = independent_conflicts()
        with self.assertRaises(FreezeError):
            api(self).MuscleConflictCoverageAssurance().assess(
                request["domains"], request["constraints"], budget(), object()
            )

    def test_base_input_rejection_is_preserved(self):
        with self.assertRaises(FreezeError):
            api(self).MuscleConflictCoverageAssurance().assess(
                {"mode": ("safe",)},
                [Constraint("bad", "mode", "NEQ", ("unknown",))],
                budget(),
                contract(self),
            )


class ConflictCoverageAdversarialTests(unittest.TestCase):
    def test_per_variable_core_explosion_freezes_without_partial_certificate(self):
        constraints = [
            Constraint("deny-a", "mode", "DENY", ("a",)),
            Constraint("deny-b", "mode", "DENY", ("b",)),
            Constraint("eq-a", "mode", "EQ", ("a",)),
            Constraint("eq-b", "mode", "EQ", ("b",)),
        ]
        result = api(self).MuscleConflictCoverageAssurance().assess(
            {"mode": ("a", "b")},
            constraints,
            budget(),
            contract(self, max_cores_per_variable=3),
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "CONFLICT_COVERAGE_BUDGET_EXCEEDED")
        self.assertIn("PER_VARIABLE_CORE_BUDGET_EXCEEDED:mode", result["gaps"])
        self.assertEqual(result["conflict_families"], {})

    def test_total_core_explosion_freezes(self):
        request = independent_conflicts()
        result = api(self).MuscleConflictCoverageAssurance().assess(
            request["domains"],
            request["constraints"],
            budget(),
            contract(self, max_total_cores=1),
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertIn("TOTAL_CORE_BUDGET_EXCEEDED", result["gaps"])

    def test_input_permutations_are_deterministic(self):
        request = independent_conflicts()
        assurance = api(self).MuscleConflictCoverageAssurance()
        expected = assurance.assess(
            request["domains"], request["constraints"], budget(), contract(self)
        )
        rng = random.Random(74945)
        for _ in range(100):
            sample = request["constraints"][:]
            rng.shuffle(sample)
            self.assertEqual(
                assurance.assess(request["domains"], sample, budget(), contract(self)),
                expected,
            )

    def test_contract_change_changes_certificate(self):
        request = independent_conflicts()
        assurance = api(self).MuscleConflictCoverageAssurance()
        left = assurance.assess(
            request["domains"], request["constraints"], budget(), contract(self)
        )
        right = assurance.assess(
            request["domains"],
            request["constraints"],
            budget(),
            contract(self, max_total_cores=129),
        )
        self.assertEqual(left["conflict_families"], right["conflict_families"])
        self.assertNotEqual(left["contract_hash"], right["contract_hash"])
        self.assertNotEqual(left["result_hash"], right["result_hash"])


class ConflictCoverageIntegrationTests(unittest.TestCase):
    def test_original_selected_core_is_member_of_certified_family(self):
        request = independent_conflicts()
        result = api(self).MuscleConflictCoverageAssurance().assess(
            request["domains"], request["constraints"], budget(), contract(self)
        )
        original = result["base"]["original"]
        family = result["conflict_families"][original["variable"]]["cores"]
        self.assertIn(original["core_ids"], [item["core_ids"] for item in family])

    def test_base_gap_is_reproduced_and_closed(self):
        request = independent_conflicts()
        base = MuscleInputAssurance().solve(
            request["domains"], request["constraints"], budget()
        )
        self.assertEqual(base["original"]["variable"], "a")
        self.assertEqual(base["original"]["final_domains"]["b"], [])
        result = api(self).MuscleConflictCoverageAssurance().assess(
            request["domains"], request["constraints"], budget(), contract(self)
        )
        self.assertIn("b", result["conflict_families"])


if __name__ == "__main__":
    unittest.main()
