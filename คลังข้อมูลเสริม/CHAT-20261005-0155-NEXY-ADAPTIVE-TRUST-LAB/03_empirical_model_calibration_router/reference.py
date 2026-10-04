from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from typing import Iterable


@dataclass(frozen=True)
class Observation:
    model_id: str
    capability: str
    success: bool
    reported_confidence: float
    latency_ms: int
    cost_microunits: int


@dataclass(frozen=True)
class RoutePolicy:
    min_samples: int = 3
    max_latency_ms: int = 5000
    max_cost_microunits: int = 1000
    min_reliability: float = 0.5
    latency_penalty: float = 0.10
    cost_penalty: float = 0.10


@dataclass(frozen=True)
class RouteDecision:
    status: str
    model_id: str | None
    reason: str
    scores: dict[str, float]


def route(observations: Iterable[Observation], capability: str, policy: RoutePolicy = RoutePolicy()) -> RouteDecision:
    if not capability or policy.min_samples <= 0 or policy.max_latency_ms <= 0 or policy.max_cost_microunits < 0:
        return RouteDecision("FREEZE", None, "INVALID_POLICY_OR_CAPABILITY", {})
    groups: dict[str, list[Observation]] = defaultdict(list)
    for o in observations:
        if not o.model_id or not o.capability or not (0 <= o.reported_confidence <= 1) or o.latency_ms < 0 or o.cost_microunits < 0:
            return RouteDecision("FREEZE", None, "MALFORMED_OBSERVATION", {})
        if o.capability == capability:
            groups[o.model_id].append(o)
    if not groups:
        return RouteDecision("PROBE", None, "NO_CAPABILITY_EVIDENCE", {})

    if all(len(rows) < policy.min_samples for rows in groups.values()):
        return RouteDecision("PROBE", None, "INSUFFICIENT_SAMPLES", {})

    scores: dict[str, float] = {}
    for model_id, rows in groups.items():
        if len(rows) < policy.min_samples:
            continue
        successes = sum(1 for r in rows if r.success)
        reliability = (successes + 1.0) / (len(rows) + 2.0)
        mean_cal_error = sum(abs(r.reported_confidence - (1.0 if r.success else 0.0)) for r in rows) / len(rows)
        mean_latency = sum(r.latency_ms for r in rows) / len(rows)
        mean_cost = sum(r.cost_microunits for r in rows) / len(rows)
        if reliability < policy.min_reliability or mean_latency > policy.max_latency_ms or mean_cost > policy.max_cost_microunits:
            continue
        latency_ratio = min(mean_latency / policy.max_latency_ms, 1.0)
        cost_ratio = 0.0 if policy.max_cost_microunits == 0 else min(mean_cost / policy.max_cost_microunits, 1.0)
        scores[model_id] = reliability - mean_cal_error - policy.latency_penalty * latency_ratio - policy.cost_penalty * cost_ratio

    if not scores:
        return RouteDecision("FREEZE", None, "NO_ELIGIBLE_MODEL", {})
    winner = sorted(scores, key=lambda m: (-scores[m], m))[0]
    return RouteDecision("ROUTE", winner, "EMPIRICAL_BEST_ELIGIBLE", scores)
