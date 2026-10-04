from __future__ import annotations

import itertools
import math
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .canonical import canonical_json
from .errors import ContractValidationError, RecoveryPlanningError
from .model import OutcomeContract
from .verifier import verify_outcome


@dataclass(frozen=True, slots=True)
class RecoveryAction:
    action_id: str
    cost: float
    risk: float
    reversible: bool
    effects: Mapping[str, Any]


def _set_path(root: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    current = root
    for segment in parts[:-1]:
        child = current.get(segment)
        if child is None:
            child = {}
            current[segment] = child
        if not isinstance(child, dict):
            raise RecoveryPlanningError(f"cannot set {path}: non-object at {segment}")
        current = child
    current[parts[-1]] = value


def _parse_actions(actions: Sequence[Mapping[str, Any]]) -> list[RecoveryAction]:
    if len(actions) > 16:
        raise RecoveryPlanningError("at most 16 recovery actions are allowed for exact search")
    parsed: list[RecoveryAction] = []
    seen: set[str] = set()
    for index, raw in enumerate(actions):
        if not isinstance(raw, Mapping):
            raise RecoveryPlanningError(f"actions[{index}] must be an object")
        required = {"action_id", "cost", "risk", "reversible", "effects"}
        if set(raw) != required:
            raise RecoveryPlanningError(f"actions[{index}] fields must be exactly {sorted(required)}")
        action_id = raw["action_id"]
        if not isinstance(action_id, str) or not action_id.strip():
            raise RecoveryPlanningError(f"actions[{index}].action_id must be non-empty")
        if action_id in seen:
            raise RecoveryPlanningError(f"duplicate action_id: {action_id}")
        seen.add(action_id)
        cost = raw["cost"]
        risk = raw["risk"]
        if isinstance(cost, bool) or not isinstance(cost, (int, float)) or not math.isfinite(float(cost)) or float(cost) < 0:
            raise RecoveryPlanningError(f"actions[{index}].cost must be finite and >= 0")
        if isinstance(risk, bool) or not isinstance(risk, (int, float)) or not math.isfinite(float(risk)) or not 0 <= float(risk) <= 1:
            raise RecoveryPlanningError(f"actions[{index}].risk must be finite and between 0 and 1")
        reversible = raw["reversible"]
        if not isinstance(reversible, bool):
            raise RecoveryPlanningError(f"actions[{index}].reversible must be boolean")
        effects = raw["effects"]
        if not isinstance(effects, Mapping) or not effects:
            raise RecoveryPlanningError(f"actions[{index}].effects must be a non-empty object")
        if not all(isinstance(path, str) and path and ".." not in path and all(part for part in path.split(".")) for path in effects):
            raise RecoveryPlanningError(f"actions[{index}].effects contains invalid path")
        try:
            canonical_json(dict(effects))
        except ContractValidationError as exc:
            raise RecoveryPlanningError(f"actions[{index}].effects must be canonical JSON: {exc}") from exc
        parsed.append(RecoveryAction(action_id, float(cost), float(risk), reversible, dict(effects)))
    return sorted(parsed, key=lambda item: item.action_id)


def _compatible(combo: tuple[RecoveryAction, ...]) -> bool:
    assigned: dict[str, Any] = {}
    for action in combo:
        for path, value in action.effects.items():
            if path in assigned and assigned[path] != value:
                return False
            assigned[path] = value
    return True


def _apply(observation: Mapping[str, Any], combo: tuple[RecoveryAction, ...]) -> dict[str, Any]:
    if not isinstance(observation, Mapping):
        raise RecoveryPlanningError("observation must be an object")
    state = deepcopy(dict(observation))
    for action in combo:
        for path, value in sorted(action.effects.items()):
            _set_path(state, path, value)
    return state


def plan_recovery(
    contract: OutcomeContract,
    observation: Mapping[str, Any],
    actions: Sequence[Mapping[str, Any]],
    *,
    max_cost: float,
    max_risk: float,
    require_reversible: bool = True,
) -> dict[str, Any]:
    if isinstance(max_cost, bool) or not isinstance(max_cost, (int, float)) or not math.isfinite(float(max_cost)) or max_cost < 0:
        raise RecoveryPlanningError("max_cost must be finite and >= 0")
    if isinstance(max_risk, bool) or not isinstance(max_risk, (int, float)) or not math.isfinite(float(max_risk)) or not 0 <= max_risk <= 1:
        raise RecoveryPlanningError("max_risk must be finite and between 0 and 1")
    parsed = _parse_actions(actions)

    current_report = verify_outcome(contract, observation)
    if current_report["status"] == "PASS":
        return {"status": "PASS", "plan": [], "cost": 0.0, "risk": 0.0, "reason": "already_satisfied"}

    feasible: list[tuple[tuple[float, float, int, tuple[str, ...]], tuple[RecoveryAction, ...], dict[str, Any]]] = []
    for size in range(1, len(parsed) + 1):
        for combo in itertools.combinations(parsed, size):
            if require_reversible and any(not action.reversible for action in combo):
                continue
            total_cost = sum(action.cost for action in combo)
            combined_risk = 1.0
            for action in combo:
                combined_risk *= 1.0 - action.risk
            combined_risk = 1.0 - combined_risk
            if total_cost > max_cost or combined_risk > max_risk:
                continue
            if not _compatible(combo):
                continue
            state = _apply(observation, combo)
            report = verify_outcome(contract, state)
            if report["status"] != "PASS":
                continue
            ids = tuple(action.action_id for action in combo)
            rank = (round(total_cost, 12), round(combined_risk, 12), len(combo), ids)
            feasible.append((rank, combo, report))

    if not feasible:
        return {
            "status": "FAIL",
            "plan": [],
            "reason": "no_admissible_plan",
            "current_status": current_report["status"],
        }

    rank, combo, report = min(feasible, key=lambda item: item[0])
    return {
        "status": "PASS",
        "plan": [action.action_id for action in combo],
        "cost": rank[0],
        "risk": rank[1],
        "result_status": report["status"],
        "reason": "minimal_lexicographic_cost_risk_size_id",
    }
