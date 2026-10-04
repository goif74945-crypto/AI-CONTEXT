from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .common import Verdict, canonical_hash


@dataclass(frozen=True)
class ObjectiveContract:
    objective_id: str
    acceptance_criteria: tuple[str, ...]
    forbidden_scope_prefixes: tuple[str, ...] = ()


@dataclass(frozen=True)
class WorkItem:
    item_id: str
    contributes_to: tuple[str, ...]
    scope: str
    depends_on: tuple[str, ...] = ()


def _find_cycle(items: dict[str, WorkItem]) -> tuple[str, ...]:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> tuple[str, ...] | None:
        if node in visiting:
            idx = stack.index(node)
            return tuple(stack[idx:] + [node])
        if node in visited:
            return None
        visiting.add(node)
        stack.append(node)
        for dep in sorted(items[node].depends_on):
            if dep in items:
                cycle = visit(dep)
                if cycle:
                    return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in sorted(items):
        cycle = visit(node)
        if cycle:
            return cycle
    return ()


def analyze(contract: ObjectiveContract, work_items: Iterable[WorkItem]) -> dict:
    criteria = tuple(dict.fromkeys(contract.acceptance_criteria))
    if not contract.objective_id.strip() or not criteria or any(not c.strip() for c in criteria):
        return {
            "verdict": Verdict.FREEZE.value,
            "reason_codes": ["INVALID_OBJECTIVE_CONTRACT"],
            "fingerprint": canonical_hash({"contract": contract, "items": []}),
        }

    items_list = list(work_items)
    ids = [item.item_id for item in items_list]
    duplicate_ids = sorted({i for i in ids if ids.count(i) > 1})
    item_map = {item.item_id: item for item in items_list}
    criterion_set = set(criteria)

    invalid_dependencies = sorted(
        (item.item_id, dep)
        for item in items_list
        for dep in item.depends_on
        if dep not in item_map
    )
    invalid_contributions = sorted(
        (item.item_id, criterion)
        for item in items_list
        for criterion in item.contributes_to
        if criterion not in criterion_set
    )
    orphan_items = sorted(item.item_id for item in items_list if not item.contributes_to)
    forbidden_items = sorted(
        item.item_id
        for item in items_list
        if any(item.scope == p or item.scope.startswith(p.rstrip("/") + "/") for p in contract.forbidden_scope_prefixes)
    )
    covered = {criterion for item in items_list for criterion in item.contributes_to if criterion in criterion_set}
    missing_criteria = sorted(criterion_set - covered)
    cycle = _find_cycle(item_map) if not duplicate_ids else ()

    reasons: list[str] = []
    if duplicate_ids:
        reasons.append("DUPLICATE_WORK_ITEM_ID")
    if invalid_dependencies:
        reasons.append("UNKNOWN_DEPENDENCY")
    if invalid_contributions:
        reasons.append("UNKNOWN_ACCEPTANCE_CRITERION")
    if orphan_items:
        reasons.append("ORPHAN_WORK_ITEM")
    if forbidden_items:
        reasons.append("FORBIDDEN_SCOPE")
    if missing_criteria:
        reasons.append("UNCOVERED_ACCEPTANCE_CRITERION")
    if cycle:
        reasons.append("DEPENDENCY_CYCLE")

    result = {
        "verdict": Verdict.FREEZE.value if reasons else Verdict.PASS.value,
        "reason_codes": sorted(reasons),
        "coverage": {
            "criteria_total": len(criteria),
            "criteria_covered": len(covered),
            "ratio_ppm": (len(covered) * 1_000_000) // len(criteria),
        },
        "orphan_items": orphan_items,
        "missing_criteria": missing_criteria,
        "forbidden_items": forbidden_items,
        "invalid_dependencies": [list(v) for v in invalid_dependencies],
        "invalid_contributions": [list(v) for v in invalid_contributions],
        "dependency_cycle": list(cycle),
    }
    result["fingerprint"] = canonical_hash({"contract": contract, "items": sorted(items_list, key=lambda i: i.item_id), "result": result})
    return result
