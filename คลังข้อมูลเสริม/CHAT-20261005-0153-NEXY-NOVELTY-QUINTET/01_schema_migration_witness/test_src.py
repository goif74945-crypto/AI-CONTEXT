import unittest
from src import apply_plan, evaluate_round_trip


class SchemaMigrationWitnessTests(unittest.TestCase):
    def test_rename_round_trip_is_lossless(self):
        records = [{"user_id": 7, "name": "Ada"}, {"user_id": 8, "name": "Lin"}]
        forward = [{"op": "rename", "from": "user_id", "to": "id"}]
        reverse = [{"op": "rename", "from": "id", "to": "user_id"}]
        report = evaluate_round_trip(records, forward, reverse)
        self.assertTrue(report["lossless"])
        self.assertEqual(report["mismatches"], [])

    def test_drop_without_inverse_is_detected(self):
        records = [{"id": 1, "legacy": "x"}]
        forward = [{"op": "drop", "field": "legacy"}]
        reverse = []
        report = evaluate_round_trip(records, forward, reverse)
        self.assertFalse(report["lossless"])
        self.assertEqual(report["mismatches"][0]["index"], 0)

    def test_default_operation_does_not_overwrite_existing_value(self):
        record = {"mode": "strict"}
        out = apply_plan(record, [{"op": "add_default", "field": "mode", "value": "safe"}])
        self.assertEqual(out["mode"], "strict")

    def test_invalid_operation_fails_closed(self):
        with self.assertRaises(ValueError):
            apply_plan({"x": 1}, [{"op": "invent_magic"}])

    def test_empty_witness_corpus_is_not_verified(self):
        report = evaluate_round_trip([], [], [])
        self.assertEqual(report["status"], "NOT_VERIFIED")
        self.assertFalse(report["lossless"])


if __name__ == "__main__":
    unittest.main()
