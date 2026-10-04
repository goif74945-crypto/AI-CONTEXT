from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import prod
from typing import Iterable


@dataclass(frozen=True)
class ToolSpec:
    name: str
    capabilities: frozenset[str]
    max_evidence_class: int
    reliability: float
    latency_ms: int
    cost_units: float


@dataclass(frozen=True)
class RouteRequest:
    required_capabilities: frozenset[str]
    required_evidence_class: int
    min_tool_reliability: float = 0.0
    max_latency_ms: int = 10_000
    max_cost_units: float = 100.0
    max_tools: int = 3


@dataclass(frozen=True)
class RouteDecision:
    status: str
    tools: tuple[str, ...]
    aggregate_reliability: float
    latency_ms: int
    cost_units: float
    reason: str | None = None


def choose_route(tools: Iterable[ToolSpec], request: RouteRequest) -> RouteDecision:
    specs = tuple(sorted(tools, key=lambda t: t.name))
    if request.required_evidence_class < 0 or request.max_tools <= 0:
        return RouteDecision('FREEZE', (), 0.0, 0, 0.0, 'invalid request')
    candidates = [t for t in specs if t.reliability >= request.min_tool_reliability]
    feasible: list[tuple[float, int, float, tuple[str, ...], float]] = []
    for size in range(1, min(request.max_tools, len(candidates)) + 1):
        for combo in combinations(candidates, size):
            caps = frozenset().union(*(t.capabilities for t in combo))
            if not request.required_capabilities.issubset(caps):
                continue
            if max(t.max_evidence_class for t in combo) < request.required_evidence_class:
                continue
            latency = sum(t.latency_ms for t in combo)
            cost = sum(t.cost_units for t in combo)
            if latency > request.max_latency_ms or cost > request.max_cost_units:
                continue
            reliability = prod(t.reliability for t in combo)
            # penalty prefers lower cost/latency and higher aggregate reliability.
            penalty = cost + (latency / 1000.0) + ((1.0 - reliability) * 100.0)
            names = tuple(t.name for t in combo)
            feasible.append((round(penalty, 9), latency, round(cost, 9), names, reliability))
    if not feasible:
        return RouteDecision('FREEZE', (), 0.0, 0, 0.0, 'no tool route satisfies evidence/capability/budget constraints')
    feasible.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    _, latency, cost, names, reliability = feasible[0]
    return RouteDecision('PASS', names, round(reliability, 6), latency, round(cost, 6))
