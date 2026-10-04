from __future__ import annotations

import json

from concepts.calibration_observatory.calibrator import PredictionRecord, calibration_report
from concepts.contract_archaeologist.miner import mine_contracts
from concepts.evidence_genealogy.auditor import EvidenceItem, audit_independence
from concepts.failure_atomizer.atomizer import ddmin
from concepts.pausesafe_kernel.kernel import StepState, StepStatus, create_resume_token, validate_resume


def main() -> None:
    traces = [
        {"phase": "verify", "decision": "freeze", "risk": 9, "actor": "judge"},
        {"phase": "verify", "decision": "freeze", "risk": 8, "actor": "judge"},
        {"phase": "release", "decision": "pass", "risk": 2, "actor": "judge"},
        {"phase": "release", "decision": "pass", "risk": 1, "actor": "judge"},
    ]
    mined = mine_contracts(traces, min_implication_support=2)

    genealogy = audit_independence(
        [
            EvidenceItem("e1", "latent-contract", "trace-log", "analysis", "h1", "rev1"),
            EvidenceItem("e2", "latent-contract", "trace-log", "manual", "h2", "rev1"),
            EvidenceItem("e3", "latent-contract", "independent-test", "runtime", "h3", "rev1"),
        ],
        target_revision="rev1",
        required_independent_groups=3,
    )

    atomized = ddmin(
        ("noise-A", "phase=verify", "noise-B", "decision=freeze", "noise-C"),
        lambda xs: "phase=verify" in xs and "decision=freeze" in xs,
    )

    calibration = calibration_report(
        [PredictionRecord(f"p{i:02d}", 0.9, i < 10, "E2") for i in range(20)],
        min_records=20,
        gap_threshold=0.1,
    )

    steps = [
        StepState("mine", StepStatus.PASS, True, checkpointed=True),
        StepState("audit", StepStatus.PASS, True, checkpointed=True),
        StepState("minimize", StepStatus.PASS, True, checkpointed=True),
        StepState("calibrate", StepStatus.PASS, True, checkpointed=True),
        StepState("adoption-review", StepStatus.PENDING, True),
    ]
    token = create_resume_token("NMIL-DEMO", "checkpoint-1", steps)
    resume = validate_resume(token, steps)

    output = {
        "authority": "AI_PROPOSAL_DEMO_NOT_NEXY_CANON",
        "contract_archaeologist": mined.as_dict(),
        "evidence_genealogy": genealogy,
        "failure_atomizer": atomized.as_dict(),
        "calibration_observatory": calibration,
        "pausesafe": {"token": token.as_dict(), "resume": resume},
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
