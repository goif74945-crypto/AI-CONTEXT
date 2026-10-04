from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .model import ValidationError


def _strict_bool(raw: Mapping[str, Any], key: str, default: bool) -> bool:
    value = raw.get(key, default)
    if not isinstance(value, bool):
        raise ValidationError(f"{key} must be a boolean")
    return value


class Action(str, Enum):
    EXECUTE = "EXECUTE"
    ASK_CLARIFICATION = "ASK_CLARIFICATION"
    CONFIRM = "CONFIRM"
    FREEZE = "FREEZE"


class Risk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True, slots=True)
class DecisionContext:
    authority_conflict: bool = False
    missing_required_information: bool = False
    evidence_required: bool = False
    evidence_sufficient: bool = True
    action_reversible: bool = True
    action_preauthorized: bool = False
    confirmation_required_by_law: bool = False
    risk: Risk = Risk.LOW

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "DecisionContext":
        try:
            risk = Risk(str(raw.get("risk", "LOW")).upper())
        except ValueError as exc:
            raise ValidationError(f"unknown risk: {raw.get('risk')!r}") from exc
        return cls(
            authority_conflict=_strict_bool(raw, "authority_conflict", False),
            missing_required_information=_strict_bool(raw, "missing_required_information", False),
            evidence_required=_strict_bool(raw, "evidence_required", False),
            evidence_sufficient=_strict_bool(raw, "evidence_sufficient", True),
            action_reversible=_strict_bool(raw, "action_reversible", True),
            action_preauthorized=_strict_bool(raw, "action_preauthorized", False),
            confirmation_required_by_law=_strict_bool(raw, "confirmation_required_by_law", False),
            risk=risk,
        )


@dataclass(frozen=True, slots=True)
class DecisionResult:
    action: Action
    reason_code: str
    explanation: str

    def to_mapping(self) -> dict[str, str]:
        return {"action": self.action.value, "reason_code": self.reason_code, "explanation": self.explanation}


def decide_action(ctx: DecisionContext) -> DecisionResult:
    """Apply deterministic precedence; no probabilistic inference or hidden defaults."""
    if ctx.authority_conflict:
        return DecisionResult(Action.FREEZE, "IXD-AUTHORITY-CONFLICT", "Material authority conflict must be resolved before action.")
    if ctx.missing_required_information:
        return DecisionResult(Action.ASK_CLARIFICATION, "IXD-MISSING-REQUIRED-INFO", "Required material information is missing.")
    if ctx.evidence_required and not ctx.evidence_sufficient:
        return DecisionResult(Action.FREEZE, "IXD-EVIDENCE-INSUFFICIENT", "Required evidence is insufficient for the requested action.")
    if ctx.confirmation_required_by_law:
        return DecisionResult(Action.CONFIRM, "IXD-LAW-CONFIRM", "Governing law explicitly requires confirmation.")
    irreversible = not ctx.action_reversible
    if irreversible and not ctx.action_preauthorized:
        return DecisionResult(Action.CONFIRM, "IXD-IRREVERSIBLE-NOT-PREAUTHORIZED", "Irreversible action lacks explicit preauthorization.")
    return DecisionResult(Action.EXECUTE, "IXD-AUTHORIZED-EXECUTE", "No blocking authority, information, evidence, or confirmation condition remains.")
