from __future__ import annotations

import copy
import unittest

from c4_resume_equivalence.implementation import ResumeState, compile_capsule, verify_resume_equivalence


def next_action(critical):
    pending = critical["resume_critical"]["pending"]
    return {"action": pending[0] if pending else "complete", "target": critical["target_identity"]}


class ResumeEquivalenceTests(unittest.TestCase):
    def make_state(self, *, ephemeral=None, pending=None):
        return ResumeState(
            task_id="task-1",
            authority_epoch="law-9",
            target_identity="repo@abc123",
            resume_critical={"pending": pending or ["verify", "commit"], "invariants": ["no-nexy-write"]},
            ephemeral=ephemeral or {},
        )

    def test_ephemeral_change_preserves_equivalence(self) -> None:
        capsule = compile_capsule(self.make_state(ephemeral={"ui_tab": "a"}), next_action)
        result = verify_resume_equivalence(
            capsule, self.make_state(ephemeral={"ui_tab": "b", "note": "new"}), next_action
        )
        self.assertEqual(result.status, "VERIFIED")

    def test_critical_change_freezes(self) -> None:
        capsule = compile_capsule(self.make_state(), next_action)
        result = verify_resume_equivalence(capsule, self.make_state(pending=["deploy"]), next_action)
        self.assertEqual(result.reason, "RESUME_CRITICAL_STATE_DRIFT")

    def test_tamper_is_detected(self) -> None:
        capsule = compile_capsule(self.make_state(), next_action)
        tampered = copy.deepcopy(capsule)
        tampered["next_action"] = {"action": "delete"}
        result = verify_resume_equivalence(tampered, self.make_state(), next_action)
        self.assertEqual(result.reason, "CAPSULE_INTEGRITY_MISMATCH")

    def test_different_next_action_logic_freezes(self) -> None:
        capsule = compile_capsule(self.make_state(), next_action)
        result = verify_resume_equivalence(
            capsule,
            self.make_state(),
            lambda critical: {"action": "different", "target": critical["target_identity"]},
        )
        self.assertEqual(result.reason, "NEXT_ACTION_DRIFT")

    def test_input_mapping_order_is_canonical(self) -> None:
        left = ResumeState("t", "a", "x", {"z": 1, "a": 2})
        right = ResumeState("t", "a", "x", {"a": 2, "z": 1})
        self.assertEqual(compile_capsule(left, lambda _: "n"), compile_capsule(right, lambda _: "n"))


if __name__ == "__main__":
    unittest.main()
