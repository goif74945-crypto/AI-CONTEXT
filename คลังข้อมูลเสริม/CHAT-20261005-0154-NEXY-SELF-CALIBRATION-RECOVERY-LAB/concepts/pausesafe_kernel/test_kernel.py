from __future__ import annotations

import unittest

from concepts.pausesafe_kernel.kernel import (
    StepState,
    StepStatus,
    create_resume_token,
    preemption_assessment,
    validate_resume,
)


class PauseSafeKernelTests(unittest.TestCase):
    def test_blocks_non_idempotent_unprotected_inflight(self) -> None:
        steps = [StepState("write", StepStatus.RUNNING, idempotent=False)]
        r = preemption_assessment(steps)
        self.assertEqual(r["status"], "BLOCKED_UNSAFE_INFLIGHT")
        self.assertEqual(r["unsafe_steps"], ["write"])

    def test_requires_drain_for_idempotent_running_step(self) -> None:
        steps = [StepState("read", StepStatus.RUNNING, idempotent=True)]
        self.assertEqual(preemption_assessment(steps)["status"], "DRAIN_REQUIRED")

    def test_compensation_allows_drain_not_instant_checkpoint(self) -> None:
        steps = [StepState("write", StepStatus.RUNNING, idempotent=False, compensation_registered=True)]
        self.assertEqual(preemption_assessment(steps)["status"], "DRAIN_REQUIRED")

    def test_token_and_resume_are_state_bound(self) -> None:
        steps = [
            StepState("inspect", StepStatus.PASS, idempotent=True, checkpointed=True),
            StepState("build", StepStatus.PENDING, idempotent=True),
        ]
        token = create_resume_token("M1", "C1", steps)
        result = validate_resume(token, steps)
        self.assertEqual(result["status"], "RESUME_SAFE")
        self.assertEqual(result["next_steps"], ["build"])

        drifted = [
            StepState("inspect", StepStatus.PASS, idempotent=True, checkpointed=True),
            StepState("build", StepStatus.RUNNING, idempotent=True, checkpointed=True),
        ]
        self.assertEqual(validate_resume(token, drifted)["status"], "STATE_DRIFT")

    def test_duplicate_step_ids_rejected(self) -> None:
        steps = [
            StepState("same", StepStatus.PASS, True, checkpointed=True),
            StepState("same", StepStatus.PENDING, True),
        ]
        with self.assertRaises(ValueError):
            create_resume_token("M", "C", steps)

    def test_token_deterministic_for_equivalent_state(self) -> None:
        a = [StepState("b", StepStatus.PENDING, True), StepState("a", StepStatus.PASS, True, True)]
        b = list(reversed(a))
        self.assertEqual(create_resume_token("M", "C", a), create_resume_token("M", "C", b))


if __name__ == "__main__":
    unittest.main()
