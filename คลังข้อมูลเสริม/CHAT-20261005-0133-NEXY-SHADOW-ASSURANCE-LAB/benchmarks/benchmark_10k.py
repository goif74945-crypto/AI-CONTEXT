from __future__ import annotations

import json
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shadowguard.gate import evaluate_datasets
from shadowguard.models import DecisionRecord


def build(case_id: str, revision: str) -> DecisionRecord:
    return DecisionRecord.from_mapping({
        "case_id": case_id,
        "input_fingerprint": "sha256:" + case_id,
        "revision": revision,
        "policy_fingerprint": "sha256:policy-stable",
        "authority_chain": ["USER_LAW", "NEXY_LAW", "JUDGE"],
        "outcome": "RELEASE",
        "action": "return:verified",
        "required_evidence_classes": ["E2"],
        "evidence": [{"class": "E2", "ref": "unit:" + case_id, "revision": revision}],
        "safety_labels": ["safe-output"],
    })


def main() -> None:
    stable = [build(f"case-{i:05d}", "stable-r1") for i in range(10_000)]
    candidate = [build(f"case-{i:05d}", "candidate-r2") for i in range(10_000)]
    start = time.perf_counter()
    report = evaluate_datasets(stable, candidate)
    elapsed = time.perf_counter() - start
    print(json.dumps({
        "status": report.status,
        "cases": report.compared_cases,
        "seconds": round(elapsed, 6),
        "cases_per_second": round(report.compared_cases / elapsed, 2),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
