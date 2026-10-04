import unittest

from nexy_product_evidence.analytics import EventContract, validate_event_contract, validate_event_payload


class AnalyticsTests(unittest.TestCase):
    def test_valid_contract(self):
        c = EventContract("task_completed", frozenset({"task_id"}), frozenset({"surface"}))
        self.assertEqual(validate_event_contract(c), ())

    def test_invalid_event_name(self):
        c = EventContract("Task Completed", frozenset())
        self.assertIn("EVENT_NAME_INVALID", validate_event_contract(c))

    def test_overlap(self):
        c = EventContract("task_completed", frozenset({"id"}), frozenset({"id"}))
        self.assertTrue(any(x.startswith("PROPERTY_CLASS_OVERLAP") for x in validate_event_contract(c)))

    def test_forbidden_contract_property(self):
        c = EventContract("task_completed", frozenset({"api" + "_" + "key"}))
        self.assertTrue(any(x.startswith("FORBIDDEN_PROPERTY") for x in validate_event_contract(c)))

    def test_missing_payload_property(self):
        c = EventContract("task_completed", frozenset({"task_id"}))
        self.assertTrue(any(x.startswith("MISSING_PROPERTY") for x in validate_event_payload(c, {})))

    def test_forbidden_payload_property(self):
        c = EventContract("task_completed", frozenset({"task_id"}), frozenset())
        errors = validate_event_payload(c, {"task_id": "1", "to" + "ken": "x"})
        self.assertTrue(any(x.startswith("FORBIDDEN_PROPERTY") for x in errors))

    def test_unexpected_payload_property(self):
        c = EventContract("task_completed", frozenset({"task_id"}))
        errors = validate_event_payload(c, {"task_id": "1", "extra": 1})
        self.assertTrue(any(x.startswith("UNEXPECTED_PROPERTY") for x in errors))

    def test_valid_payload(self):
        c = EventContract("task_completed", frozenset({"task_id"}), frozenset({"surface"}))
        self.assertEqual(validate_event_payload(c, {"task_id": "1", "surface": "dialog"}), ())


if __name__ == "__main__":
    unittest.main()
