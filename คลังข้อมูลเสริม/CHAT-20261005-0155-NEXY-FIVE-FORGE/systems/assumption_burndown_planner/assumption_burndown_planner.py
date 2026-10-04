from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable


@dataclass(frozen=True)
class Assumption:
    assumption_id: str
    impact: int
    uncertainty: float
    blocks_mutation: bool = False


@dataclass(frozen=True)
class Probe:
    probe_id: str
    resolves: frozenset[str]
    cost: float
    risk: float


@dataclass(frozen=True)
class BurnDownPlan:
    status: str
    probes: tuple[str, ...]
    covered_assumptions: tuple[str, ...]
    residual_assumptions: tuple[str, ...]
    burned_risk: float
    total_cost: float
    total_risk: float
    reason: str | None = None


def plan_burndown(assumptions: Iterable[Assumption], probes: Iterable[Probe], *, max_cost: float, max_risk: float) -> BurnDownPlan:
    assumps = tuple(sorted(assumptions, key=lambda a: a.assumption_id))
    probe_list = tuple(sorted(probes, key=lambda p: p.probe_id))
    if len(probe_list) > 20:
        return BurnDownPlan('FREEZE', (), (), tuple(a.assumption_id for a in assumps), 0.0, 0.0, 0.0, 'prototype exact search supports at most 20 probes')
    ids = {a.assumption_id for a in assumps}
    if len(ids) != len(assumps):
        return BurnDownPlan('FREEZE', (), (), (), 0.0, 0.0, 0.0, 'duplicate assumption ids')
    for a in assumps:
        if not 1 <= a.impact <= 5 or not 0.0 <= a.uncertainty <= 1.0:
            return BurnDownPlan('FREEZE', (), (), (), 0.0, 0.0, 0.0, 'invalid assumption score')
    for p in probe_list:
        if p.cost < 0 or p.risk < 0:
            return BurnDownPlan('FREEZE', (), (), (), 0.0, 0.0, 0.0, 'invalid probe budget values')
        if not p.resolves.issubset(ids):
            return BurnDownPlan('FREEZE', (), (), (), 0.0, 0.0, 0.0, f'probe {p.probe_id} references unknown assumption')

    blockers = {a.assumption_id for a in assumps if a.blocks_mutation}
    weight = {a.assumption_id: a.impact * a.uncertainty for a in assumps}
    candidates = []
    for size in range(0, len(probe_list) + 1):
        for combo in combinations(probe_list, size):
            cost = sum(p.cost for p in combo)
            risk = sum(p.risk for p in combo)
            if cost > max_cost or risk > max_risk:
                continue
            covered = frozenset().union(*(p.resolves for p in combo)) if combo else frozenset()
            if not blockers.issubset(covered):
                continue
            burned = sum(weight[i] for i in covered)
            names = tuple(p.probe_id for p in combo)
            candidates.append((-burned, cost, risk, size, names, covered))
    if not candidates:
        return BurnDownPlan('FREEZE', (), (), tuple(a.assumption_id for a in assumps), 0.0, 0.0, 0.0, 'no bounded probe set covers all mutation-blocking assumptions')
    candidates.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4]))
    neg_burned, cost, risk, _, names, covered = candidates[0]
    residual = tuple(a.assumption_id for a in assumps if a.assumption_id not in covered)
    return BurnDownPlan('PASS', names, tuple(sorted(covered)), residual, round(-neg_burned, 6), round(cost, 6), round(risk, 6))
