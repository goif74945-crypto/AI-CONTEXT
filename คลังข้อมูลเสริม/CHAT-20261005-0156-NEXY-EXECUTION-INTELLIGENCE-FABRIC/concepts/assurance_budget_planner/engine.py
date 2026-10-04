from __future__ import annotations

from itertools import combinations
from typing import Any

from common import ContractError, require_dict, require_list, require_str, sorted_unique_strings, stable_hash


MAX_VALIDATORS = 20


def _satisfies(subset: tuple[dict[str, Any], ...], requirements: dict[str, int]) -> bool:
    for dimension, min_independent in requirements.items():
        domains = {v["domain"] for v in subset if dimension in v["covers"]}
        if len(domains) < min_independent:
            return False
    return True


def plan_assurance(payload: dict[str, Any]) -> dict[str, Any]:
    payload = require_dict(payload, "payload")
    raw_requirements = require_dict(payload.get("requirements", {}), "requirements")
    validators = require_list(payload.get("validators", []), "validators")
    budget = payload.get("max_cost")
    if budget is not None and (not isinstance(budget, int) or budget < 0):
        raise ContractError("max_cost must be a non-negative integer or null")

    requirements: dict[str, int] = {}
    for dimension in sorted(raw_requirements):
        require_str(dimension, "requirement dimension")
        count = raw_requirements[dimension]
        if not isinstance(count, int) or count < 1:
            raise ContractError(f"requirements[{dimension!r}] must be a positive integer")
        requirements[dimension] = count

    if not requirements:
        result = {"status": "PLAN", "selected_validators": [], "total_cost": 0, "max_latency_ms": 0, "coverage": {}}
        result["plan_id"] = stable_hash(result, prefix="assurance-plan")
        return result
    if len(validators) > MAX_VALIDATORS:
        raise ContractError(f"validator count exceeds exact-planner limit of {MAX_VALIDATORS}")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(validators):
        item = require_dict(item, f"validators[{index}]")
        validator_id = require_str(item.get("id"), f"validators[{index}].id")
        if validator_id in seen:
            raise ContractError(f"duplicate validator id: {validator_id}")
        seen.add(validator_id)
        domain = require_str(item.get("domain"), f"validators[{index}].domain")
        covers = sorted_unique_strings(item.get("covers", []), f"validators[{index}].covers")
        cost = item.get("cost")
        latency = item.get("latency_ms")
        if not isinstance(cost, int) or cost < 0:
            raise ContractError(f"validators[{index}].cost must be a non-negative integer")
        if not isinstance(latency, int) or latency < 0:
            raise ContractError(f"validators[{index}].latency_ms must be a non-negative integer")
        normalized.append({"id": validator_id, "domain": domain, "covers": covers, "cost": cost, "latency_ms": latency})
    normalized.sort(key=lambda v: v["id"])

    best: tuple[tuple[Any, ...], tuple[dict[str, Any], ...]] | None = None
    for size in range(1, len(normalized) + 1):
        for subset in combinations(normalized, size):
            if not _satisfies(subset, requirements):
                continue
            total_cost = sum(v["cost"] for v in subset)
            max_latency = max((v["latency_ms"] for v in subset), default=0)
            ids = tuple(v["id"] for v in subset)
            score = (total_cost, max_latency, len(subset), ids)
            if best is None or score < best[0]:
                best = (score, subset)

    if best is None:
        result = {"status": "FREEZE", "reason": "INSUFFICIENT_INDEPENDENT_ASSURANCE", "selected_validators": [], "total_cost": None}
        result["plan_id"] = stable_hash(result, prefix="assurance-plan")
        return result

    selected = list(best[1])
    total_cost = sum(v["cost"] for v in selected)
    if budget is not None and total_cost > budget:
        result = {
            "status": "FREEZE",
            "reason": "ASSURANCE_BUDGET_EXCEEDED",
            "required_cost": total_cost,
            "max_cost": budget,
            "selected_validators": selected,
            "total_cost": total_cost,
        }
        result["plan_id"] = stable_hash(result, prefix="assurance-plan")
        return result

    coverage = {
        dimension: sorted({v["domain"] for v in selected if dimension in v["covers"]})
        for dimension in requirements
    }
    result = {
        "status": "PLAN",
        "selected_validators": selected,
        "total_cost": total_cost,
        "max_latency_ms": max((v["latency_ms"] for v in selected), default=0),
        "coverage": coverage,
    }
    result["plan_id"] = stable_hash(result, prefix="assurance-plan")
    return result
