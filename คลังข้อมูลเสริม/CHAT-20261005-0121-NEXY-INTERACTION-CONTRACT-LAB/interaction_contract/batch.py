from __future__ import annotations

from collections import Counter
from typing import Any

from .analyzer import analyze_contract
from .canonical import canonical_sha256
from .model import ValidationError


def analyze_batch(raw_contracts: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(raw_contracts, list) or not raw_contracts:
        raise ValidationError("batch must be a non-empty list of contracts")

    reports = [analyze_contract(item) for item in raw_contracts]
    reports.sort(key=lambda report: (report["contract_id"], report["input_fingerprint_sha256"]))

    codes: Counter[str] = Counter()
    for report in reports:
        for finding in report["findings"]:
            codes[finding["code"]] += 1

    pass_count = sum(report["completion_gate"] == "PASS" for report in reports)
    retention_total = sum(report["metrics"]["retention_score"] for report in reports)

    return {
        "schema_version": "interaction-contract-batch-report/v0.1",
        "batch_fingerprint_sha256": canonical_sha256(raw_contracts),
        "contracts": len(reports),
        "pass_count": pass_count,
        "block_count": len(reports) - pass_count,
        "mean_retention_score": retention_total / len(reports),
        "finding_counts": dict(sorted(codes.items())),
        "reports": reports,
    }
