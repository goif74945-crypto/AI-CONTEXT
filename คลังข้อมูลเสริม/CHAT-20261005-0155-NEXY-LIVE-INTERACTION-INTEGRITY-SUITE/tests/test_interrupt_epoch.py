import unittest

from nexy_live_integrity import GateStatus, InterruptEpochGate


class InterruptEpochTests(unittest.TestCase):
    def test_superseded_directive_invalidates_old_action(self):
        gate = InterruptEpochGate("s1")
        old = gate.begin_directive("d1", {"text": "send report"})
        lease = gate.prepare_action(old, {"tool": "mail", "id": 1})
        gate.begin_directive("d2", {"text": "do not send; save draft"})
        result = gate.commit_action(lease, {"tool": "mail", "id": 1})
        self.assertEqual(result.status, GateStatus.FREEZE)
        self.assertEqual(result.code, "INTERRUPT_STALE_ACTION")

    def test_action_change_is_detected(self):
        gate = InterruptEpochGate("s1")
        token = gate.begin_directive("d1", {"text": "x"})
        lease = gate.prepare_action(token, {"amount": 10})
        result = gate.commit_action(lease, {"amount": 11})
        self.assertEqual(result.code, "INTERRUPT_ACTION_CHANGED")

    def test_commit_is_single_use(self):
        gate = InterruptEpochGate("s1")
        token = gate.begin_directive("d1", {"text": "x"})
        action = {"op": "save"}
        lease = gate.prepare_action(token, action)
        self.assertTrue(gate.commit_action(lease, action).allowed)
        replay = gate.commit_action(lease, action)
        self.assertEqual(replay.status, GateStatus.REJECT)
        self.assertEqual(replay.code, "INTERRUPT_LEASE_REPLAY")

    def test_cancel_invalidates_token(self):
        gate = InterruptEpochGate("s1")
        token = gate.begin_directive("d1", {"text": "x"})
        gate.cancel_active("user interrupted")
        self.assertEqual(gate.validate_token(token).code, "INTERRUPT_NO_ACTIVE_DIRECTIVE")


if __name__ == "__main__":
    unittest.main()
