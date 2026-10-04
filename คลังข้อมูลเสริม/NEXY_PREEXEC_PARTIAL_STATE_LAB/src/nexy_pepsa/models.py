from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class StepKind(str, Enum):
    READ = "READ"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    EXTERNAL_EFFECT = "EXTERNAL_EFFECT"

    @property
    def is_mutating(self) -> bool:
        return self is not StepKind.READ


class Verdict(str, Enum):
    READY = "READY"
    FREEZE = "FREEZE"


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass(frozen=True, slots=True)
class Step:
    id: str
    kind: StepKind
    resource: str
    boundary: str
    depends_on: tuple[str, ...] = ()
    reversible: bool = False
    rollback_strategy: str | None = None
    approval_id: str | None = None
    idempotency_key: str | None = None
    postcondition: str | None = None
    evidence_required: tuple[str, ...] = ()

    @property
    def is_mutating(self) -> bool:
        return self.kind.is_mutating

    @property
    def rollback_covered(self) -> bool:
        return bool(self.reversible and self.rollback_strategy)


@dataclass(frozen=True, slots=True)
class ExecutionPlan:
    plan_id: str
    steps: tuple[Step, ...]


@dataclass(frozen=True, slots=True)
class Policy:
    policy_id: str
    allowed_boundaries: tuple[str, ...]
    protected_resources: tuple[str, ...]
    max_steps: int = 128
    require_postcondition_for_mutation: bool = True
    require_evidence_for_mutation: bool = True
    require_idempotency_for_external: bool = True
    allow_terminal_irreversible_with_approval: bool = True


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    severity: Severity
    message: str
    step_id: str | None = None
    resource: str | None = None


@dataclass(frozen=True, slots=True)
class PartialState:
    failure_before_step: str
    already_applied_steps: tuple[str, ...]
    residual_resources: tuple[str, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class AnalysisReport:
    report_version: str
    plan_id: str
    policy_id: str
    verdict: Verdict
    plan_hash: str
    policy_hash: str
    combined_hash: str
    ordered_steps: tuple[str, ...]
    findings: tuple[Finding, ...]
    partial_states: tuple[PartialState, ...]
    stats: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_version": self.report_version,
            "plan_id": self.plan_id,
            "policy_id": self.policy_id,
            "verdict": self.verdict.value,
            "plan_hash": self.plan_hash,
            "policy_hash": self.policy_hash,
            "combined_hash": self.combined_hash,
            "ordered_steps": list(self.ordered_steps),
            "findings": [
                {
                    "code": item.code,
                    "severity": item.severity.value,
                    "message": item.message,
                    "step_id": item.step_id,
                    "resource": item.resource,
                }
                for item in self.findings
            ],
            "partial_states": [
                {
                    "failure_before_step": state.failure_before_step,
                    "already_applied_steps": list(state.already_applied_steps),
                    "residual_resources": list(state.residual_resources),
                    "reason": state.reason,
                }
                for state in self.partial_states
            ],
            "stats": dict(sorted(self.stats.items())),
        }
