from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Any

from .models import ExecutionPlan, Policy, Step, StepKind


class InputValidationError(ValueError):
    pass


def _reject_float(raw: str) -> None:
    raise InputValidationError(f"floating-point JSON values are forbidden: {raw}")


def load_json(path: str | Path) -> dict[str, Any]:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise InputValidationError(f"cannot read {path}: {exc}") from exc
    try:
        value = json.loads(text, parse_float=_reject_float)
    except (json.JSONDecodeError, InputValidationError) as exc:
        raise InputValidationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InputValidationError(f"top-level JSON in {path} must be an object")
    return value


def _expect_keys(data: dict[str, Any], *, allowed: set[str], required: set[str], where: str) -> None:
    unknown = sorted(set(data) - allowed)
    missing = sorted(required - set(data))
    if unknown:
        raise InputValidationError(f"{where}: unknown fields: {', '.join(unknown)}")
    if missing:
        raise InputValidationError(f"{where}: missing required fields: {', '.join(missing)}")


def _nonempty_str(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputValidationError(f"{where} must be a non-empty string")
    if unicodedata.normalize("NFC", value) != value:
        raise InputValidationError(f"{where} must already be Unicode NFC normalized")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise InputValidationError(f"{where} must not contain ASCII control characters")
    return value


def _optional_str(value: Any, where: str) -> str | None:
    if value is None:
        return None
    return _nonempty_str(value, where)


def _string_tuple(value: Any, where: str, *, allow_empty: bool = True) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise InputValidationError(f"{where} must be an array of strings")
    items: list[str] = []
    for index, item in enumerate(value):
        items.append(_nonempty_str(item, f"{where}[{index}]"))
    if not allow_empty and not items:
        raise InputValidationError(f"{where} must not be empty")
    if len(items) != len(set(items)):
        raise InputValidationError(f"{where} must not contain duplicates")
    return tuple(items)


def _bool(value: Any, where: str) -> bool:
    if type(value) is not bool:
        raise InputValidationError(f"{where} must be boolean")
    return value


def _positive_int(value: Any, where: str) -> int:
    if type(value) is not int or value <= 0:
        raise InputValidationError(f"{where} must be a positive integer")
    return value


def parse_plan(data: dict[str, Any]) -> ExecutionPlan:
    _expect_keys(
        data,
        allowed={"plan_id", "steps"},
        required={"plan_id", "steps"},
        where="plan",
    )
    plan_id = _nonempty_str(data["plan_id"], "plan.plan_id")
    raw_steps = data["steps"]
    if not isinstance(raw_steps, list) or not raw_steps:
        raise InputValidationError("plan.steps must be a non-empty array")

    steps: list[Step] = []
    for index, raw in enumerate(raw_steps):
        where = f"plan.steps[{index}]"
        if not isinstance(raw, dict):
            raise InputValidationError(f"{where} must be an object")
        _expect_keys(
            raw,
            allowed={
                "id",
                "kind",
                "resource",
                "boundary",
                "depends_on",
                "reversible",
                "rollback_strategy",
                "approval_id",
                "idempotency_key",
                "postcondition",
                "evidence_required",
            },
            required={"id", "kind", "resource", "boundary"},
            where=where,
        )
        raw_kind = _nonempty_str(raw["kind"], f"{where}.kind")
        try:
            kind = StepKind(raw_kind)
        except ValueError as exc:
            legal = ", ".join(item.value for item in StepKind)
            raise InputValidationError(f"{where}.kind must be one of: {legal}") from exc

        step = Step(
            id=_nonempty_str(raw["id"], f"{where}.id"),
            kind=kind,
            resource=_nonempty_str(raw["resource"], f"{where}.resource"),
            boundary=_nonempty_str(raw["boundary"], f"{where}.boundary"),
            depends_on=_string_tuple(raw.get("depends_on", []), f"{where}.depends_on"),
            reversible=_bool(raw.get("reversible", False), f"{where}.reversible"),
            rollback_strategy=_optional_str(raw.get("rollback_strategy"), f"{where}.rollback_strategy"),
            approval_id=_optional_str(raw.get("approval_id"), f"{where}.approval_id"),
            idempotency_key=_optional_str(raw.get("idempotency_key"), f"{where}.idempotency_key"),
            postcondition=_optional_str(raw.get("postcondition"), f"{where}.postcondition"),
            evidence_required=_string_tuple(raw.get("evidence_required", []), f"{where}.evidence_required"),
        )
        steps.append(step)

    return ExecutionPlan(plan_id=plan_id, steps=tuple(steps))


def parse_policy(data: dict[str, Any]) -> Policy:
    _expect_keys(
        data,
        allowed={
            "policy_id",
            "allowed_boundaries",
            "protected_resources",
            "max_steps",
            "require_postcondition_for_mutation",
            "require_evidence_for_mutation",
            "require_idempotency_for_external",
            "allow_terminal_irreversible_with_approval",
        },
        required={"policy_id", "allowed_boundaries", "protected_resources"},
        where="policy",
    )
    return Policy(
        policy_id=_nonempty_str(data["policy_id"], "policy.policy_id"),
        allowed_boundaries=_string_tuple(data["allowed_boundaries"], "policy.allowed_boundaries", allow_empty=False),
        protected_resources=_string_tuple(data["protected_resources"], "policy.protected_resources"),
        max_steps=_positive_int(data.get("max_steps", 128), "policy.max_steps"),
        require_postcondition_for_mutation=_bool(
            data.get("require_postcondition_for_mutation", True),
            "policy.require_postcondition_for_mutation",
        ),
        require_evidence_for_mutation=_bool(
            data.get("require_evidence_for_mutation", True),
            "policy.require_evidence_for_mutation",
        ),
        require_idempotency_for_external=_bool(
            data.get("require_idempotency_for_external", True),
            "policy.require_idempotency_for_external",
        ),
        allow_terminal_irreversible_with_approval=_bool(
            data.get("allow_terminal_irreversible_with_approval", True),
            "policy.allow_terminal_irreversible_with_approval",
        ),
    )


def load_plan(path: str | Path) -> ExecutionPlan:
    return parse_plan(load_json(path))


def load_policy(path: str | Path) -> Policy:
    return parse_policy(load_json(path))
