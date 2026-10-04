from __future__ import annotations

from typing import Any

from .canonical import to_canonical_data
from .model import VerificationReport


def report_to_dict(report: VerificationReport) -> dict[str, Any]:
    return {
        "run_id": report.run_id,
        "passed": report.passed,
        "counts": dict(report.counts),
        "metadata": to_canonical_data(report.metadata),
        "results": [
            {
                "relation_id": item.relation_id,
                "status": item.status.value,
                "reason": item.reason,
                "seed_case_hash": item.seed_case_hash,
                "derived_case_hash": item.derived_case_hash,
                "baseline_observation_hash": item.baseline_observation_hash,
                "derived_observation_hash": item.derived_observation_hash,
                "details": to_canonical_data(item.details),
            }
            for item in report.results
        ],
    }
