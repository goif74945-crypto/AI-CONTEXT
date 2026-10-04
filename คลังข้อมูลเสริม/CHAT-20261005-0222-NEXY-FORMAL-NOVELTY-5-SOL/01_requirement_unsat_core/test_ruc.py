import unittest

from ruc import ModelTooLargeError, Requirement, RequirementUnsatCore, Rule


class RequirementUnsatCoreTests(unittest.TestCase):
    def test_extracts_irreducible_conflict_and_drops_irrelevant_requirement(self):
        solver = RequirementUnsatCore({"region": ["EU", "US"], "mode": ["safe", "fast"]})
        reqs = [
            Requirement("R-EU", (Rule("eq", "region", value="EU"),)),
            Requirement("R-US", (Rule("eq", "region", value="US"),)),
            Requirement("R-SAFE", (Rule("eq", "mode", value="safe"),)),
        ]
        result = solver.solve(reqs)
        self.assertFalse(result.satisfiable)
        self.assertEqual(set(result.core_ids), {"R-EU", "R-US"})

    def test_supports_cross_variable_implication(self):
        solver = RequirementUnsatCore({"risk": ["low", "high"], "approval": ["none", "human"]})
        reqs = [
            Requirement("HIGH", (Rule("eq", "risk", value="high"),)),
            Requirement("HIGH_REQUIRES_HUMAN", (Rule("implies", "risk", value="high", right="approval", right_value="human"),)),
            Requirement("NO_APPROVAL", (Rule("eq", "approval", value="none"),)),
        ]
        result = solver.solve(reqs)
        self.assertFalse(result.satisfiable)
        self.assertEqual(set(result.core_ids), {"HIGH", "HIGH_REQUIRES_HUMAN", "NO_APPROVAL"})

    def test_returns_witness_for_satisfiable_set(self):
        solver = RequirementUnsatCore({"region": ["EU", "US"], "mode": ["safe", "fast"]})
        result = solver.solve([
            Requirement("R1", (Rule("eq", "region", value="EU"),)),
            Requirement("R2", (Rule("neq", "mode", value="fast"),)),
        ])
        self.assertTrue(result.satisfiable)
        self.assertEqual(result.witness, {"mode": "safe", "region": "EU"})
        self.assertEqual(result.core_ids, ())

    def test_fails_closed_when_state_space_is_too_large(self):
        solver = RequirementUnsatCore({"a": range(100), "b": range(100)}, max_assignments=9_999)
        with self.assertRaises(ModelTooLargeError):
            solver.solve([Requirement("R", (Rule("neq", "a", value=-1),))])


if __name__ == "__main__":
    unittest.main()
