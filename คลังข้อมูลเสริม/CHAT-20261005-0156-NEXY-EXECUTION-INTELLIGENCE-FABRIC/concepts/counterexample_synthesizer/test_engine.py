import unittest

from common import ContractError
from concepts.counterexample_synthesizer.engine import synthesize_counterexamples, validate_case


class CounterexampleSynthesizerTests(unittest.TestCase):
    def setUp(self):
        self.schema = {"fields": {
            "age": {"type": "int", "required": True, "min": 1, "max": 120},
            "mode": {"type": "enum", "required": True, "values": ["safe", "strict"]},
            "name": {"type": "string", "required": True, "min_length": 2, "max_length": 8},
            "enabled": {"type": "bool", "required": True},
        }}
        self.valid = {"age": 13, "mode": "strict", "name": "NEXY", "enabled": True}

    def test_generated_vectors_are_all_invalid(self):
        suite = synthesize_counterexamples(self.schema, self.valid)
        self.assertEqual(suite["status"], "PASS")
        self.assertGreaterEqual(suite["count"], 10)
        for vector in suite["vectors"]:
            self.assertTrue(validate_case(self.schema, vector["input"]), vector["id"])

    def test_invalid_base_case_freezes(self):
        suite = synthesize_counterexamples(self.schema, {**self.valid, "age": 0})
        self.assertEqual(suite["status"], "FREEZE")
        self.assertEqual(suite["reason"], "BASE_CASE_INVALID")

    def test_malformed_bounds_fail_closed(self):
        bad_schema = {"fields": {"age": {"type": "int", "required": True, "min": "zero"}}}
        with self.assertRaises(ContractError):
            synthesize_counterexamples(bad_schema, {"age": 1})

    def test_field_order_does_not_change_suite(self):
        reversed_fields = dict(reversed(list(self.schema["fields"].items())))
        one = synthesize_counterexamples(self.schema, self.valid)
        two = synthesize_counterexamples({"fields": reversed_fields}, self.valid)
        self.assertEqual(one["suite_id"], two["suite_id"])


if __name__ == "__main__":
    unittest.main()
