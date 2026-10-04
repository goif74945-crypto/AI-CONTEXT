from __future__ import annotations

import unittest

from concepts.calibration_observatory.calibrator import PredictionRecord, calibration_report
from concepts.contract_archaeologist.miner import mine_contracts
from concepts.evidence_genealogy.auditor import EvidenceItem, audit_independence
from concepts.failure_atomizer.atomizer import ddmin
from concepts.pausesafe_kernel.kernel import StepState, StepStatus, create_resume_token, validate_resume


class PortfolioIntegrationTests(unittest.TestCase):
    def test_meta_integrity_workflow(self) -> None:
        traces = [
            {"phase": "verify", "decision": "freeze", "severity": 9},
            {"phase": "verify", "decision": "freeze", "severity": 8},
            {"phase": "release", "decision": "pass", "severity": 2},
            {"phase": "release", "decision": "pass", "severity": 1},
        ]
        mined = mine_contracts(traces, min_implication_support=2)
        self.assertEqual(mined.status, "READY")
        self.assertTrue(any(p.kind == "OBSERVED_IMPLICATION" for p in mined.patterns))

        evidence = [
            EvidenceItem("trace-a", "latent-contract", "same-log", "analysis", "h1", "rev1"),
            EvidenceItem("trace-b", "latent-contract", "same-log", "manual", "h2", "rev1"),
            EvidenceItem("test-c", "latent-contract", "independent-test", "runtime", "h3", "rev1"),
        ]
        genealogy = audit_independence(evidence, target_revision="rev1", required_independent_groups=3)
        self.assertEqual(genealogy["status"], "INSUFFICIENT_INDEPENDENCE")

        failing_case = ("noise", "verify", "freeze", "extra")
        atomized = ddmin(failing_case, lambda xs: "verify" in xs and "freeze" in xs)
        self.assertEqual(set(atomized.minimal), {"verify", "freeze"})

        calibration = calibration_report(
            [PredictionRecord(f"p{i}", 0.9, i < 10, "E2") for i in range(20)],
            min_records=20,
        )
        self.assertEqual(calibration["status"], "SYSTEMATIC_OVERCONFIDENCE")

        state = [
            StepState("mine", StepStatus.PASS, True, checkpointed=True),
            StepState("audit", StepStatus.PASS, True, checkpointed=True),
            StepState("reduce", StepStatus.PASS, True, checkpointed=True),
            StepState("calibrate", StepStatus.PASS, True, checkpointed=True),
            StepState("integrate", StepStatus.PENDING, True),
        ]
        token = create_resume_token("meta-integrity", "cp-1", state)
        resumed = validate_resume(token, state)
        self.assertEqual(resumed, {"status": "RESUME_SAFE", "next_steps": ["integrate"]})


if __name__ == "__main__":
    unittest.main()
