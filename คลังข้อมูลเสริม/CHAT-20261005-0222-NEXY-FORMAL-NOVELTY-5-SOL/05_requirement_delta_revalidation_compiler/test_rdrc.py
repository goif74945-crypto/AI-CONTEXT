import unittest

from rdrc import FieldConstraint, RequirementDeltaRevalidationCompiler, RequirementSpec


def req(req_id, allowed, evidence=2):
    return RequirementSpec(req_id, {"mode": FieldConstraint("allowed_set", values=tuple(allowed))}, evidence)


class RequirementDeltaRevalidationCompilerTests(unittest.TestCase):
    def test_detects_tightening_and_requires_negative_regression_proof(self):
        result = RequirementDeltaRevalidationCompiler.compare(
            [req("R1", ["safe", "fast"], 2)],
            [req("R1", ["safe"], 3)],
        )
        delta = result[0]
        self.assertEqual(delta.change, "TIGHTENED")
        self.assertEqual(delta.required_evidence_class, 3)
        self.assertIn("negative", delta.gates)
        self.assertIn("regression", delta.gates)

    def test_detects_loosening_as_policy_sensitive(self):
        result = RequirementDeltaRevalidationCompiler.compare(
            [req("R1", ["safe"], 3)],
            [req("R1", ["safe", "fast"], 2)],
        )
        delta = result[0]
        self.assertEqual(delta.change, "LOOSENED")
        self.assertIn("policy-review", delta.gates)
        self.assertGreaterEqual(delta.required_evidence_class, 2)

    def test_added_and_removed_requirements_have_distinct_obligations(self):
        result = RequirementDeltaRevalidationCompiler.compare(
            [req("OLD", ["safe"])],
            [req("NEW", ["safe"], 4)],
        )
        by_id = {d.requirement_id: d for d in result}
        self.assertEqual(by_id["NEW"].change, "ADDED")
        self.assertEqual(by_id["NEW"].required_evidence_class, 4)
        self.assertEqual(by_id["OLD"].change, "REMOVED")
        self.assertIn("orphan-reference-audit", by_id["OLD"].gates)

    def test_interval_relation_handles_narrowing(self):
        old = RequirementSpec("LATENCY", {"ms": FieldConstraint("interval", minimum=0, maximum=500)}, 2)
        new = RequirementSpec("LATENCY", {"ms": FieldConstraint("interval", minimum=0, maximum=250)}, 2)
        delta = RequirementDeltaRevalidationCompiler.compare([old], [new])[0]
        self.assertEqual(delta.change, "TIGHTENED")
        self.assertEqual(delta.field_changes, (("ms", "TIGHTENED"),))


if __name__ == "__main__":
    unittest.main()
