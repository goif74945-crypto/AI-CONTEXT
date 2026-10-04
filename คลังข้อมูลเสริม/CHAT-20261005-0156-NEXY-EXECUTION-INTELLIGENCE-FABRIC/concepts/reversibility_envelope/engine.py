from __future__ import annotations

import heapq
from typing import Any

from common import ContractError, require_dict, require_list, require_str, sorted_unique_strings, stable_hash


def _topological_order(actions: list[dict[str, Any]]) -> list[str]:
    ids = {a["id"] for a in actions}
    indegree = {action_id: 0 for action_id in ids}
    outgoing: dict[str, list[str]] = {action_id: [] for action_id in ids}
    for action in actions:
        for dep in action["depends_on"]:
            if dep not in ids:
                raise ContractError(f"action {action['id']!r} depends on unknown action {dep!r}")
            if dep == action["id"]:
                raise ContractError(f"action {action['id']!r} cannot depend on itself")
            indegree[action["id"]] += 1
            outgoing[dep].append(action["id"])

    ready = [action_id for action_id, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        current = heapq.heappop(ready)
        order.append(current)
        for child in sorted(outgoing[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(ready, child)
    if len(order) != len(ids):
        raise ContractError("action dependency graph contains a cycle")
    return order


def plan_reversibility(payload: dict[str, Any]) -> dict[str, Any]:
    payload = require_dict(payload, "payload")
    raw_actions = require_list(payload.get("actions", []), "actions")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()

    for index, item in enumerate(raw_actions):
        item = require_dict(item, f"actions[{index}]")
        action_id = require_str(item.get("id"), f"actions[{index}].id")
        if action_id in seen:
            raise ContractError(f"duplicate action id: {action_id}")
        seen.add(action_id)
        depends_on = sorted_unique_strings(item.get("depends_on", []), f"actions[{index}].depends_on")
        reversible = item.get("reversible")
        if not isinstance(reversible, bool):
            raise ContractError(f"actions[{index}].reversible must be boolean")
        compensation = item.get("compensation")
        if compensation is not None:
            compensation = require_str(compensation, f"actions[{index}].compensation")
        approved = item.get("approved_irreversible", False)
        if not isinstance(approved, bool):
            raise ContractError(f"actions[{index}].approved_irreversible must be boolean")
        normalized.append({
            "id": action_id,
            "depends_on": depends_on,
            "reversible": reversible,
            "compensation": compensation,
            "approved_irreversible": approved,
        })

    normalized.sort(key=lambda a: a["id"])
    try:
        order = _topological_order(normalized)
    except ContractError as exc:
        result = {"status": "FREEZE", "reason": "INVALID_ACTION_GRAPH", "detail": str(exc), "execution_order": [], "rollback_order": []}
        result["plan_id"] = stable_hash(result, prefix="reversal-plan")
        return result

    by_id = {a["id"]: a for a in normalized}
    for action_id in order:
        action = by_id[action_id]
        if action["reversible"] and not action["compensation"]:
            result = {
                "status": "FREEZE",
                "reason": "MISSING_COMPENSATION",
                "action": action_id,
                "execution_order": order,
                "rollback_order": [],
            }
            result["plan_id"] = stable_hash(result, prefix="reversal-plan")
            return result
        if not action["reversible"] and not action["approved_irreversible"]:
            result = {
                "status": "FREEZE",
                "reason": "UNAPPROVED_IRREVERSIBLE_ACTION",
                "action": action_id,
                "execution_order": order,
                "rollback_order": [],
            }
            result["plan_id"] = stable_hash(result, prefix="reversal-plan")
            return result

    rollback_order = [
        {"action": action_id, "compensation": by_id[action_id]["compensation"]}
        for action_id in reversed(order)
        if by_id[action_id]["reversible"]
    ]
    point_of_no_return = next((action_id for action_id in order if not by_id[action_id]["reversible"]), None)
    result = {
        "status": "PLAN",
        "execution_order": order,
        "rollback_order": rollback_order,
        "point_of_no_return": point_of_no_return,
    }
    result["plan_id"] = stable_hash(result, prefix="reversal-plan")
    return result
