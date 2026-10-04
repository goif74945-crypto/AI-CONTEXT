from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Iterable


@dataclass(frozen=True)
class TestSpec:
    name: str
    covers: frozenset[str]
    cost: float


@dataclass(frozen=True)
class VerificationPlan:
    status: str
    impacted_nodes: tuple[str, ...]
    selected_tests: tuple[str, ...]
    uncovered_nodes: tuple[str, ...]
    reason: str


def impacted_nodes(dependencies: dict[str, set[str]], changed: Iterable[str]) -> set[str]:
    reverse: dict[str, set[str]] = defaultdict(set)
    nodes = set(dependencies)
    for node, deps in dependencies.items():
        nodes.update(deps)
        for dep in deps:
            reverse[dep].add(node)
    start = set(changed)
    seen = set(start)
    q = deque(sorted(start))
    while q:
        cur = q.popleft()
        for nxt in sorted(reverse.get(cur, ())):
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return seen


def schedule(dependencies: dict[str, set[str]], changed: Iterable[str], tests: Iterable[TestSpec]) -> VerificationPlan:
    impacted = impacted_nodes(dependencies, changed)
    if not impacted:
        return VerificationPlan("PLAN", (), (), (), "NO_IMPACT")
    specs = list(tests)
    if any(not t.name or t.cost <= 0 for t in specs):
        return VerificationPlan("FREEZE", tuple(sorted(impacted)), (), tuple(sorted(impacted)), "INVALID_TEST_METADATA")

    selectable = [t for t in specs if t.covers & impacted]
    coverable = set().union(*(t.covers for t in selectable)) & impacted if selectable else set()
    uncovered = impacted - coverable
    if uncovered:
        return VerificationPlan("FREEZE", tuple(sorted(impacted)), (), tuple(sorted(uncovered)), "UNCOVERED_IMPACT")

    remaining = set(impacted)
    selected: list[str] = []
    while remaining:
        ranked = []
        for t in selectable:
            gain = len(t.covers & remaining)
            if gain:
                ranked.append((-(gain / t.cost), t.cost, t.name, t))
        if not ranked:
            break
        ranked.sort(key=lambda x: (x[0], x[1], x[2]))
        chosen = ranked[0][3]
        selected.append(chosen.name)
        remaining -= chosen.covers
        selectable = [t for t in selectable if t.name != chosen.name]

    if remaining:
        return VerificationPlan("FREEZE", tuple(sorted(impacted)), tuple(selected), tuple(sorted(remaining)), "PLANNER_STALLED")
    return VerificationPlan("PLAN", tuple(sorted(impacted)), tuple(selected), (), "COVERED_IMPACT")
