from __future__ import annotations

from typing import Any

from .canonical import content_hash
from .errors import ContractValidationError
from .model import Criterion, ForbiddenEffect, OutcomeContract

_ALLOWED_TOP = {"objective_id", "objective", "criteria", "forbidden_effects"}
_ALLOWED_CRITERION = {
    "id",
    "path",
    "op",
    "value",
    "hard",
    "weight",
    "regression_guard",
    "max_regression",
}
_ALLOWED_FORBIDDEN = {"id", "path", "op", "value"}
_ALLOWED_OPS = {"min", "max", "eq", "range", "in"}


def _require_exact_keys(payload: dict[str, Any], allowed: set[str], where: str, required: set[str]) -> None:
    unknown = sorted(set(payload) - allowed)
    missing = sorted(required - set(payload))
    if unknown:
        raise ContractValidationError(f"unknown field(s) in {where}: {', '.join(unknown)}")
    if missing:
        raise ContractValidationError(f"missing field(s) in {where}: {', '.join(missing)}")


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractValidationError(f"{label} must be a non-empty string")
    return value.strip()


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContractValidationError(f"{label} must be numeric")
    result = float(value)
    if result != result or result in (float("inf"), float("-inf")):
        raise ContractValidationError(f"{label} must be finite")
    return result


def _validate_operator_value(op: str, value: Any, label: str) -> Any:
    if op not in _ALLOWED_OPS:
        raise ContractValidationError(f"{label}.op unsupported: {op!r}")
    if op in {"min", "max"}:
        _number(value, f"{label}.value")
    elif op == "range":
        if not isinstance(value, list) or len(value) != 2:
            raise ContractValidationError(f"{label}.value must be [low, high] for range")
        low = _number(value[0], f"{label}.value[0]")
        high = _number(value[1], f"{label}.value[1]")
        if low > high:
            raise ContractValidationError(f"{label}.value range low must be <= high")
    elif op == "in":
        if not isinstance(value, list) or not value:
            raise ContractValidationError(f"{label}.value must be a non-empty list for in")
    return value


def compile_contract(spec: dict[str, Any]) -> tuple[OutcomeContract, str]:
    if not isinstance(spec, dict):
        raise ContractValidationError("contract spec must be an object")
    _require_exact_keys(spec, _ALLOWED_TOP, "contract", {"objective_id", "objective", "criteria"})
    objective_id = _nonempty_string(spec["objective_id"], "objective_id")
    objective = _nonempty_string(spec["objective"], "objective")

    criteria_raw = spec["criteria"]
    if not isinstance(criteria_raw, list) or not criteria_raw:
        raise ContractValidationError("criteria must be a non-empty list")

    criteria: list[Criterion] = []
    seen_ids: set[str] = set()
    for index, raw in enumerate(criteria_raw):
        where = f"criteria[{index}]"
        if not isinstance(raw, dict):
            raise ContractValidationError(f"{where} must be an object")
        _require_exact_keys(raw, _ALLOWED_CRITERION, where, {"id", "path", "op", "value", "hard"})
        criterion_id = _nonempty_string(raw["id"], f"{where}.id")
        if criterion_id in seen_ids:
            raise ContractValidationError(f"duplicate criterion id: {criterion_id}")
        seen_ids.add(criterion_id)
        path = _nonempty_string(raw["path"], f"{where}.path")
        if any(part == "" for part in path.split(".")):
            raise ContractValidationError(f"{where}.path contains an empty segment")
        op = raw["op"]
        if not isinstance(op, str):
            raise ContractValidationError(f"{where}.op must be a string")
        value = _validate_operator_value(op, raw["value"], where)
        hard = raw["hard"]
        if not isinstance(hard, bool):
            raise ContractValidationError(f"{where}.hard must be boolean")
        weight = _number(raw.get("weight", 0.0 if hard else 1.0), f"{where}.weight")
        if hard and weight != 0.0:
            raise ContractValidationError(f"{where}.weight must be 0 for hard criteria")
        if not hard and weight <= 0.0:
            raise ContractValidationError(f"{where}.weight must be > 0 for soft criteria")
        regression_guard = raw.get("regression_guard", hard)
        if not isinstance(regression_guard, bool):
            raise ContractValidationError(f"{where}.regression_guard must be boolean")
        max_regression = _number(raw.get("max_regression", 0.0), f"{where}.max_regression")
        if max_regression < 0:
            raise ContractValidationError(f"{where}.max_regression must be >= 0")
        criteria.append(
            Criterion(
                criterion_id=criterion_id,
                path=path,
                op=op,  # type: ignore[arg-type]
                value=value,
                hard=hard,
                weight=weight,
                regression_guard=regression_guard,
                max_regression=max_regression,
            )
        )

    forbidden_raw = spec.get("forbidden_effects", [])
    if not isinstance(forbidden_raw, list):
        raise ContractValidationError("forbidden_effects must be a list")
    forbidden: list[ForbiddenEffect] = []
    seen_forbidden: set[str] = set()
    for index, raw in enumerate(forbidden_raw):
        where = f"forbidden_effects[{index}]"
        if not isinstance(raw, dict):
            raise ContractValidationError(f"{where} must be an object")
        _require_exact_keys(raw, _ALLOWED_FORBIDDEN, where, {"id", "path", "op", "value"})
        effect_id = _nonempty_string(raw["id"], f"{where}.id")
        if effect_id in seen_forbidden:
            raise ContractValidationError(f"duplicate forbidden effect id: {effect_id}")
        seen_forbidden.add(effect_id)
        path = _nonempty_string(raw["path"], f"{where}.path")
        op = raw["op"]
        if not isinstance(op, str):
            raise ContractValidationError(f"{where}.op must be a string")
        value = _validate_operator_value(op, raw["value"], where)
        forbidden.append(ForbiddenEffect(effect_id=effect_id, path=path, op=op, value=value))  # type: ignore[arg-type]

    contract = OutcomeContract(
        contract_version="nexy-oaf/1",
        objective_id=objective_id,
        objective=objective,
        criteria=tuple(sorted(criteria, key=lambda item: item.criterion_id)),
        forbidden_effects=tuple(sorted(forbidden, key=lambda item: item.effect_id)),
    )
    return contract, content_hash(contract.to_dict())


def contract_from_dict(payload: dict[str, Any]) -> OutcomeContract:
    if not isinstance(payload, dict):
        raise ContractValidationError("contract must be an object")
    allowed = {"contract_version", "objective_id", "objective", "criteria", "forbidden_effects"}
    unknown = sorted(set(payload) - allowed)
    missing = sorted(allowed - set(payload))
    if unknown:
        raise ContractValidationError(f"unknown field(s) in compiled contract: {', '.join(unknown)}")
    if missing:
        raise ContractValidationError(f"missing field(s) in compiled contract: {', '.join(missing)}")
    if payload.get("contract_version") != "nexy-oaf/1":
        raise ContractValidationError("unsupported contract_version")
    spec = {
        "objective_id": payload["objective_id"],
        "objective": payload["objective"],
        "criteria": payload["criteria"],
        "forbidden_effects": payload["forbidden_effects"],
    }
    contract, _ = compile_contract(spec)
    return contract
