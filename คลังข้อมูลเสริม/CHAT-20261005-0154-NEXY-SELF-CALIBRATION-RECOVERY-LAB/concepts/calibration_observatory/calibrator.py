from __future__ import annotations

from dataclasses import dataclass, asdict
from math import isfinite
from typing import Iterable

from core.canonical import fingerprint


@dataclass(frozen=True)
class PredictionRecord:
    record_id: str
    probability: float
    outcome: bool
    evidence_class: str

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ValueError("record_id must be non-empty")
        if not isfinite(self.probability) or not 0.0 <= self.probability <= 1.0:
            raise ValueError("probability must be finite and in [0, 1]")
        if not self.evidence_class.strip():
            raise ValueError("evidence_class must be non-empty")

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _bucket_index(p: float, bucket_count: int) -> int:
    return min(int(p * bucket_count), bucket_count - 1)


def calibration_report(
    records: Iterable[PredictionRecord],
    *,
    bucket_count: int = 10,
    min_records: int = 20,
    gap_threshold: float = 0.10,
) -> dict[str, object]:
    rows = sorted(list(records), key=lambda r: r.record_id)
    if bucket_count < 2:
        raise ValueError("bucket_count must be >= 2")
    if min_records < 1:
        raise ValueError("min_records must be >= 1")
    if not 0 <= gap_threshold <= 1:
        raise ValueError("gap_threshold must be in [0, 1]")
    ids = [r.record_id for r in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate record_id")

    if not rows:
        payload = {
            "status": "NO_DATA",
            "count": 0,
            "brier_score": None,
            "ece": None,
            "buckets": [],
            "interpretation": "ADVISORY_ONLY_NOT_EVIDENCE_OF_CORRECTNESS",
        }
        payload["report_fingerprint"] = fingerprint(payload)
        return payload

    brier_sum = 0.0
    stats = [{"count": 0, "confidence_sum": 0.0, "successes": 0} for _ in range(bucket_count)]
    evidence_classes: set[str] = set()
    for r in rows:
        truth = 1.0 if r.outcome else 0.0
        brier_sum += (r.probability - truth) ** 2
        idx = _bucket_index(r.probability, bucket_count)
        bucket = stats[idx]
        bucket["count"] += 1
        bucket["confidence_sum"] += r.probability
        bucket["successes"] += 1 if r.outcome else 0
        evidence_classes.add(r.evidence_class)

    buckets: list[dict[str, object]] = []
    weighted_gap = 0.0
    signed_weighted_gap = 0.0
    for i, bucket in enumerate(stats):
        count = int(bucket["count"])
        if not count:
            continue
        avg_conf = float(bucket["confidence_sum"]) / count
        success_rate = int(bucket["successes"]) / count
        gap = avg_conf - success_rate
        weighted_gap += abs(gap) * count / len(rows)
        signed_weighted_gap += gap * count / len(rows)
        buckets.append({
            "bucket": i,
            "lower": i / bucket_count,
            "upper": (i + 1) / bucket_count,
            "count": count,
            "avg_confidence": round(avg_conf, 12),
            "success_rate": round(success_rate, 12),
            "signed_gap": round(gap, 12),
        })

    if len(rows) < min_records:
        status = "NOT_ENOUGH_DATA"
    elif abs(signed_weighted_gap) <= gap_threshold and weighted_gap <= gap_threshold:
        status = "CALIBRATION_WITHIN_THRESHOLD"
    elif signed_weighted_gap > gap_threshold:
        status = "SYSTEMATIC_OVERCONFIDENCE"
    elif signed_weighted_gap < -gap_threshold:
        status = "SYSTEMATIC_UNDERCONFIDENCE"
    else:
        status = "LOCAL_MISALIGNMENT"

    payload = {
        "status": status,
        "count": len(rows),
        "brier_score": round(brier_sum / len(rows), 12),
        "ece": round(weighted_gap, 12),
        "signed_calibration_bias": round(signed_weighted_gap, 12),
        "buckets": buckets,
        "evidence_classes": sorted(evidence_classes),
        "interpretation": "ADVISORY_ONLY_NOT_EVIDENCE_OF_CORRECTNESS",
    }
    payload["report_fingerprint"] = fingerprint(payload)
    return payload
