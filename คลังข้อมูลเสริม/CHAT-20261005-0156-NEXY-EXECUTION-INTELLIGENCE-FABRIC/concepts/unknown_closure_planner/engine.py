from __future__ import annotations

from itertools import combinations
from typing import Any

from common import ContractError, require_dict, require_list, require_str, sorted_unique_strings, stable_hash


MAX_PROBES = 20


def plan_unknown_closure(payload: dict[str, Any]) -> dict[str, Any]:
    payload = require_dict(payload, "payload")
    requirements = require_list(payload.get("requirements", []), "requirements")
    probes = require_list(payload.get("probes", []), "probes")
    known = set(sorted_unique_strings(payload.get("known", []), "known"))

    required_unknowns: set[str] = set()
    normalized_requirements: list[dict[str, Any]] = []
    seen_req: set[str] = set()
    for index, item in enumerate(requirements):
        item = require_dict(item, f"requirements[{index}]")
        req_id = require_str(item.get("id"), f"requirements[{index}].id")
        if req_id in seen_req:
            raise ContractError(f"duplicate requirement id: {req_id}")
        seen_req.add(req_id)
        blocked = sorted_unique_strings(item.get("blocked_by", []), f"requirements[{index}].blocked_by")
        required_unknowns.update(blocked)
        normalized_requirements.append({"id": req_id, "blocked_by": blocked})

    needed = sorted(required_unknowns - known)
    if not needed:
        result = {"status": "PROCEED", "needed": [], "selected_probes": [], "total_cost": 0}
        result["plan_id"] = stable_hash(result, prefix="unknown-plan")
        return result

    if len(probes) > MAX_PROBES:
        raise ContractError(f"probe count exceeds exact-planner limit of {MAX_PROBES}")

    normalized_probes: list[dict[str, Any]] = []
    seen_probe: set[str] = set()
    for index, item in enumerate(probes):
        item = require_dict(item, f"probes[{index}]")
        probe_id = require_str(item.get("id"), f"probes[{index}].id")
        if probe_id in seen_probe:
            raise ContractError(f"duplicate probe id: {probe_id}")
        seen_probe.add(probe_id)
        cost = item.get("cost")
        if not isinstance(cost, int) or cost < 0:
            raise ContractError(f"probes[{index}].cost must be a non-negative integer")
        resolves = sorted_unique_strings(item.get("resolves", []), f"probes[{index}].resolves")
        question = require_str(item.get("question"), f"probes[{index}].question")
        normalized_probes.append({"id": probe_id, "cost": cost, "resolves": resolves, "question": question})

    normalized_probes.sort(key=lambda p: p["id"])
    needed_set = set(needed)
    best: tuple[tuple[Any, ...], list[dict[str, Any]]] | None = None

    for size in range(1, len(normalized_probes) + 1):
        for subset in combinations(normalized_probes, size):
            covered: set[str] = set()
            for probe in subset:
                covered.update(probe["resolves"])
            if not needed_set.issubset(covered):
                continue
            ids = tuple(probe["id"] for probe in subset)
            total_cost = sum(probe["cost"] for probe in subset)
            score = (total_cost, len(subset), ids)
            if best is None or score < best[0]:
                best = (score, list(subset))

    if best is None:
        coverable = set().union(*(set(p["resolves"]) for p in normalized_probes)) if normalized_probes else set()
        result = {
            "status": "FREEZE",
            "reason": "UNRESOLVABLE_UNKNOWNS",
            "needed": needed,
            "unresolvable": sorted(needed_set - coverable),
            "selected_probes": [],
            "total_cost": None,
        }
    else:
        selected = best[1]
        result = {
            "status": "ASK",
            "needed": needed,
            "selected_probes": selected,
            "questions": [p["question"] for p in selected],
            "total_cost": sum(p["cost"] for p in selected),
        }
    result["plan_id"] = stable_hash(result, prefix="unknown-plan")
    return result
