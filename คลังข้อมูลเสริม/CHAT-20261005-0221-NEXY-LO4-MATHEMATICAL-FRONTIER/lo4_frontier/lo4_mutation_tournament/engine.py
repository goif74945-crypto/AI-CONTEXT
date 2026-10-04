"""Fail-closed, recommendation-only tournament for experimental Lo4 proposals."""
from __future__ import annotations

from decimal import Decimal
from numbers import Real
from collections.abc import Iterable, Mapping

_METRICS = ("safety", "utility", "proof", "reversibility", "novelty")
_DEFAULT_THRESHOLDS = {"safety": 0.90, "proof": 0.80, "reversibility": 0.60}
_WEIGHTS = {
    "safety": Decimal("0.30"),
    "utility": Decimal("0.20"),
    "proof": Decimal("0.20"),
    "reversibility": Decimal("0.15"),
    "novelty": Decimal("0.15"),
}


def _normalize_metrics(raw: Mapping[str, object]) -> dict[str, Decimal]:
    if not isinstance(raw, Mapping):
        raise ValueError("metrics must be a mapping")
    if set(raw) != set(_METRICS):
        raise ValueError(f"metrics must contain exactly {_METRICS!r}")
    normalized: dict[str, Decimal] = {}
    for metric in _METRICS:
        value = raw[metric]
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"metric {metric} must be numeric")
        decimal_value = Decimal(str(value))
        if not Decimal("0") <= decimal_value <= Decimal("1"):
            raise ValueError(f"metric {metric} must be within [0,1]")
        normalized[metric] = decimal_value
    return normalized


def _dominates(a: dict[str, Decimal], b: dict[str, Decimal]) -> bool:
    return all(a[m] >= b[m] for m in _METRICS) and any(a[m] > b[m] for m in _METRICS)


def run_tournament(
    candidates: Iterable[dict], *, thresholds: Mapping[str, float] | None = None
) -> dict:
    """Rank experimental candidates without granting promotion authority.

    Candidate eligibility is fail-closed: any invariant failure or threshold
    violation rejects it.  Eligible candidates are Pareto-filtered and then a
    deterministic weighted score selects a recommendation.  The output can
    never authorize Canon mutation or promotion.
    """
    materialized = list(candidates)
    if not materialized:
        raise ValueError("at least one candidate is required")
    threshold_map = dict(_DEFAULT_THRESHOLDS)
    if thresholds is not None:
        for metric, value in thresholds.items():
            if metric not in _METRICS:
                raise ValueError(f"unknown threshold metric: {metric}")
            if isinstance(value, bool) or not isinstance(value, Real) or not 0 <= value <= 1:
                raise ValueError(f"threshold {metric} must be within [0,1]")
            threshold_map[metric] = float(value)

    normalized: dict[str, dict] = {}
    rejected: dict[str, str] = {}
    for candidate in materialized:
        if not isinstance(candidate, dict):
            raise ValueError("each candidate must be a mapping")
        candidate_id = candidate.get("id")
        if not isinstance(candidate_id, str) or not candidate_id:
            raise ValueError("candidate id must be a non-empty string")
        if candidate_id in normalized:
            raise ValueError(f"duplicate candidate id: {candidate_id}")
        invariant_failures = candidate.get("invariant_failures")
        if not isinstance(invariant_failures, list) or any(
            not isinstance(item, str) or not item for item in invariant_failures
        ):
            raise ValueError("invariant_failures must be a list of non-empty strings")
        metrics = _normalize_metrics(candidate.get("metrics", {}))
        normalized[candidate_id] = {"metrics": metrics, "invariant_failures": tuple(sorted(set(invariant_failures)))}
        if invariant_failures:
            rejected[candidate_id] = "INVARIANT_FAILURE"
            continue
        if any(metrics[m] < Decimal(str(limit)) for m, limit in threshold_map.items()):
            rejected[candidate_id] = "THRESHOLD_FAILURE"

    eligible = {candidate_id: data for candidate_id, data in normalized.items() if candidate_id not in rejected}
    pareto: list[str] = []
    for candidate_id in sorted(eligible):
        metrics = eligible[candidate_id]["metrics"]
        if not any(
            other_id != candidate_id and _dominates(other["metrics"], metrics)
            for other_id, other in eligible.items()
        ):
            pareto.append(candidate_id)

    def score(candidate_id: str) -> Decimal:
        metrics = eligible[candidate_id]["metrics"]
        return sum((_WEIGHTS[m] * metrics[m] for m in _METRICS), start=Decimal("0"))

    winner_id = min(pareto, key=lambda candidate_id: (-score(candidate_id), candidate_id)) if pareto else None
    scores = {candidate_id: str(score(candidate_id).normalize()) for candidate_id in sorted(eligible)}
    return {
        "status": "RECOMMENDATION_ONLY" if winner_id is not None else "NO_ELIGIBLE_CANDIDATE",
        "winner_id": winner_id,
        "eligible_ids": tuple(sorted(eligible)),
        "pareto_ids": tuple(pareto),
        "rejected": {candidate_id: rejected[candidate_id] for candidate_id in sorted(rejected)},
        "scores": scores,
        "promotion_permitted": False,
        "authority": "EXPERIMENTAL_ONLY",
    }
