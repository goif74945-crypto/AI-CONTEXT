import unittest

from failure_witness_distiller.engine import distill


class FailureWitnessDistillerTests(unittest.TestCase):
    @staticmethod
    def oracle(payload):
        if payload.get("action") == "release" and payload.get("authority") != "approved":
            return "FREEZE:AUTHORITY_MISSING"
        return None

    def test_distills_irrelevant_structure_while_preserving_signature(self):
        source = {
            "action": "release",
            "authority": "missing",
            "trace": {"id": "abc", "noise": [1, 2, 3]},
            "notes": "long irrelevant explanation",
            "flags": [True, False],
        }
        result = distill(source, self.oracle)
        self.assertEqual(result.signature, "FREEZE:AUTHORITY_MISSING")
        self.assertLess(result.final_nodes, result.original_nodes)
        self.assertEqual(self.oracle(result.witness), result.signature)
        self.assertEqual(result.witness.get("action"), "release")
        self.assertNotEqual(result.witness.get("authority"), "approved")

    def test_is_deterministic(self):
        source = {"z": 9, "action": "release", "authority": "denied", "a": [1, 2, 3]}
        a = distill(source, self.oracle)
        b = distill(source, self.oracle)
        self.assertEqual(a.witness, b.witness)
        self.assertEqual(a.steps, b.steps)

    def test_refuses_non_failing_source(self):
        with self.assertRaisesRegex(ValueError, "does not produce"):
            distill({"action": "release", "authority": "approved"}, self.oracle)

    def test_unstable_oracle_is_detected(self):
        calls = {"n": 0}

        def unstable(_payload):
            calls["n"] += 1
            return "X" if calls["n"] < 2 else None

        with self.assertRaises(RuntimeError):
            distill({"a": 1}, unstable)


if __name__ == "__main__":
    unittest.main()
