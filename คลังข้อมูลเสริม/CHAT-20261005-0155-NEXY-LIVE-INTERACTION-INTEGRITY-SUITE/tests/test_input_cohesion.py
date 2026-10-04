import unittest

from nexy_live_integrity import GateStatus, InputCohesionGate, InputRequirement, InputResource

H1 = "1" * 64
H2 = "2" * 64
H3 = "3" * 64


class InputCohesionTests(unittest.TestCase):
    def test_complete_binding_passes_and_extra_is_quarantined(self):
        reqs = [InputRequirement("spec", "file", expected_sha256=H1)]
        resources = [
            InputResource("spec", "file", H1, "user"),
            InputResource("unreferenced", "file", H2, "external"),
        ]
        result = InputCohesionGate.evaluate(reqs, resources)
        self.assertTrue(result.allowed)
        self.assertEqual([r.resource_id for r in result.bound_resources], ["spec"])
        self.assertEqual([r.resource_id for r in result.quarantined_resources], ["unreferenced"])

    def test_missing_required_freezes(self):
        result = InputCohesionGate.evaluate([InputRequirement("spec", "file")], [])
        self.assertEqual(result.status, GateStatus.FREEZE)
        self.assertIn("missing:spec", result.problems)

    def test_digest_mismatch_freezes(self):
        result = InputCohesionGate.evaluate(
            [InputRequirement("spec", "file", expected_sha256=H1)],
            [InputResource("spec", "file", H2, "user")],
        )
        self.assertIn("digest_mismatch:spec", result.problems)

    def test_duplicate_resource_id_is_ambiguous(self):
        result = InputCohesionGate.evaluate(
            [InputRequirement("spec", "file")],
            [InputResource("spec", "file", H1, "user"), InputResource("spec", "file", H3, "user")],
        )
        self.assertIn("ambiguous:spec", result.problems)


if __name__ == "__main__":
    unittest.main()
