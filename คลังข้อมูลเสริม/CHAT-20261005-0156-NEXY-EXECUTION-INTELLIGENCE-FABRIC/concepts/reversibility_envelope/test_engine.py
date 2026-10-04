import unittest

from concepts.reversibility_envelope.engine import plan_reversibility


class ReversibilityEnvelopeTests(unittest.TestCase):
    def test_execution_and_rollback_orders(self):
        result = plan_reversibility({"actions": [
            {"id": "write", "depends_on": ["snapshot"], "reversible": True, "compensation": "restore-write"},
            {"id": "snapshot", "depends_on": [], "reversible": True, "compensation": "discard-snapshot"},
            {"id": "verify", "depends_on": ["write"], "reversible": True, "compensation": "clear-verification"},
        ]})
        self.assertEqual(result["status"], "PLAN")
        self.assertEqual(result["execution_order"], ["snapshot", "write", "verify"])
        self.assertEqual([x["action"] for x in result["rollback_order"]], ["verify", "write", "snapshot"])
        self.assertIsNone(result["point_of_no_return"])

    def test_unapproved_irreversible_action_freezes(self):
        result = plan_reversibility({"actions": [
            {"id": "destroy", "depends_on": [], "reversible": False}
        ]})
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "UNAPPROVED_IRREVERSIBLE_ACTION")

    def test_missing_compensation_freezes(self):
        result = plan_reversibility({"actions": [
            {"id": "write", "depends_on": [], "reversible": True}
        ]})
        self.assertEqual(result["reason"], "MISSING_COMPENSATION")

    def test_approved_irreversible_marks_point_of_no_return(self):
        result = plan_reversibility({"actions": [
            {"id": "snapshot", "depends_on": [], "reversible": True, "compensation": "discard"},
            {"id": "publish", "depends_on": ["snapshot"], "reversible": False, "approved_irreversible": True},
        ]})
        self.assertEqual(result["status"], "PLAN")
        self.assertEqual(result["point_of_no_return"], "publish")
        self.assertEqual([x["action"] for x in result["rollback_order"]], ["snapshot"])

    def test_cycle_freezes(self):
        result = plan_reversibility({"actions": [
            {"id": "a", "depends_on": ["b"], "reversible": True, "compensation": "undo-a"},
            {"id": "b", "depends_on": ["a"], "reversible": True, "compensation": "undo-b"},
        ]})
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "INVALID_ACTION_GRAPH")


if __name__ == "__main__":
    unittest.main()
