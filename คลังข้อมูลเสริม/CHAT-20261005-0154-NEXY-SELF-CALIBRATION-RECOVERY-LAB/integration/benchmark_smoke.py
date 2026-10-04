from __future__ import annotations

import json
import platform
import statistics
import time

from concepts.calibration_observatory.calibrator import PredictionRecord, calibration_report
from concepts.contract_archaeologist.miner import mine_contracts
from concepts.evidence_genealogy.auditor import EvidenceItem, audit_independence
from concepts.failure_atomizer.atomizer import ddmin
from concepts.pausesafe_kernel.kernel import StepState, StepStatus, preemption_assessment


def timed(fn, repeats: int = 5):
    values = []
    result = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        result = fn()
        values.append(time.perf_counter() - t0)
    return result, {
        "repeats": repeats,
        "median_seconds": statistics.median(values),
        "min_seconds": min(values),
        "max_seconds": max(values),
    }


def main() -> None:
    traces = [
        {
            "phase": "verify" if i % 2 == 0 else "release",
            "decision": "freeze" if i % 2 == 0 else "pass",
            "actor": "judge",
            "risk": i % 10,
            "lane": f"L{i % 4}",
        }
        for i in range(2_000)
    ]
    mined, t_miner = timed(lambda: mine_contracts(traces, min_implication_support=100), 3)

    evidence = [
        EvidenceItem(
            f"e{i:05d}",
            "claim",
            f"root-{i % 500}",
            f"method-{i % 7}",
            f"content-{i}",
            "rev",
        )
        for i in range(20_000)
    ]
    audited, t_evidence = timed(lambda: audit_independence(evidence, target_revision="rev", required_independent_groups=400), 3)

    predictions = [PredictionRecord(f"p{i:06d}", (i % 100) / 100, (i % 100) < 50, "E2") for i in range(100_000)]
    calibrated, t_calibration = timed(lambda: calibration_report(predictions, min_records=20), 3)

    steps = [StepState(f"s{i:05d}", StepStatus.PASS if i < 49_999 else StepStatus.PENDING, True, checkpointed=i < 49_999) for i in range(50_000)]
    paused, t_pause = timed(lambda: preemption_assessment(steps), 5)

    atoms = tuple(f"x{i}" for i in range(2_048))
    reduced, t_atomizer = timed(lambda: ddmin(atoms, lambda xs: "x777" in xs and "x1777" in xs), 3)

    report = {
        "status": "LOCAL_SMOKE_ONLY_NOT_PRODUCTION_SLA",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "processor": platform.processor(),
        },
        "benchmarks": {
            "contract_archaeologist_2000_events": {**t_miner, "patterns": len(mined.patterns)},
            "evidence_genealogy_20000_items": {**t_evidence, "groups": audited["independent_group_count"]},
            "calibration_100000_records": {**t_calibration, "status": calibrated["status"]},
            "pausesafe_50000_steps": {**t_pause, "status": paused["status"]},
            "failure_atomizer_2048_items": {**t_atomizer, "minimal_size": len(reduced.minimal), "evaluations": reduced.evaluations},
        },
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
