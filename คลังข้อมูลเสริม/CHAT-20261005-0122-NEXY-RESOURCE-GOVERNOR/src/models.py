from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class DataClass(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class RiskTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


DATA_CLASS_RANK: dict[DataClass, int] = {
    DataClass.PUBLIC: 0,
    DataClass.INTERNAL: 1,
    DataClass.CONFIDENTIAL: 2,
    DataClass.RESTRICTED: 3,
}

ALLOWED_ROLES = frozenset({"worker", "verifier"})
ALLOWED_OBJECTIVES = frozenset({"cost", "latency", "quality"})


class ContractError(ValueError):
    """Raised when a caller supplies an invalid resource-governor contract."""


@dataclass(frozen=True, slots=True)
class AgentProfile:
    agent_id: str
    provider_domain: str
    roles: frozenset[str]
    capabilities: frozenset[str]
    clearance: DataClass
    max_context_tokens: int
    input_cost_microunits_per_1k: int
    output_cost_microunits_per_1k: int
    estimated_latency_ms: int
    quality_bps: int
    max_evidence_class: int
    active: bool = True
    quarantined: bool = False

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise ContractError("agent_id must be non-empty")
        if not self.provider_domain.strip():
            raise ContractError("provider_domain must be non-empty")
        if not self.roles or not self.roles.issubset(ALLOWED_ROLES):
            raise ContractError(f"roles must be a non-empty subset of {sorted(ALLOWED_ROLES)}")
        if self.max_context_tokens <= 0:
            raise ContractError("max_context_tokens must be > 0")
        for name, value in (
            ("input_cost_microunits_per_1k", self.input_cost_microunits_per_1k),
            ("output_cost_microunits_per_1k", self.output_cost_microunits_per_1k),
            ("estimated_latency_ms", self.estimated_latency_ms),
        ):
            if value < 0:
                raise ContractError(f"{name} must be >= 0")
        if not 0 <= self.quality_bps <= 10_000:
            raise ContractError("quality_bps must be between 0 and 10000")
        if not 0 <= self.max_evidence_class <= 7:
            raise ContractError("max_evidence_class must be between E0 and E7")


@dataclass(frozen=True, slots=True)
class TaskProfile:
    task_id: str
    required_capabilities: frozenset[str]
    data_class: DataClass
    risk_tier: RiskTier
    required_evidence_class: int
    worker_input_tokens: int
    worker_output_tokens: int
    verifier_input_tokens: int = 0
    verifier_output_tokens: int = 0
    require_independent_verifier: bool = False
    min_quality_bps: int = 0
    max_total_tokens: int | None = None
    max_cost_microunits: int | None = None
    max_latency_ms: int | None = None

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ContractError("task_id must be non-empty")
        if not 0 <= self.required_evidence_class <= 7:
            raise ContractError("required_evidence_class must be between E0 and E7")
        for name, value in (
            ("worker_input_tokens", self.worker_input_tokens),
            ("worker_output_tokens", self.worker_output_tokens),
            ("verifier_input_tokens", self.verifier_input_tokens),
            ("verifier_output_tokens", self.verifier_output_tokens),
        ):
            if value < 0:
                raise ContractError(f"{name} must be >= 0")
        if self.worker_input_tokens + self.worker_output_tokens <= 0:
            raise ContractError("worker token estimate must be > 0")
        if not 0 <= self.min_quality_bps <= 10_000:
            raise ContractError("min_quality_bps must be between 0 and 10000")
        for name, value in (
            ("max_total_tokens", self.max_total_tokens),
            ("max_cost_microunits", self.max_cost_microunits),
            ("max_latency_ms", self.max_latency_ms),
        ):
            if value is not None and value < 0:
                raise ContractError(f"{name} must be >= 0 or null")


@dataclass(frozen=True, slots=True)
class GovernorPolicy:
    verifier_required_from_evidence_class: int = 2
    independence_required_risk: frozenset[RiskTier] = field(
        default_factory=lambda: frozenset({RiskTier.HIGH, RiskTier.CRITICAL})
    )
    objective_order: tuple[str, ...] = ("cost", "latency", "quality")
    max_pair_diagnostics: int = 200

    def __post_init__(self) -> None:
        if not 0 <= self.verifier_required_from_evidence_class <= 7:
            raise ContractError("verifier_required_from_evidence_class must be E0..E7")
        if not self.objective_order:
            raise ContractError("objective_order must not be empty")
        if len(set(self.objective_order)) != len(self.objective_order):
            raise ContractError("objective_order must not contain duplicates")
        if not set(self.objective_order).issubset(ALLOWED_OBJECTIVES):
            raise ContractError(f"objective_order contains unsupported metric: {self.objective_order}")
        if self.max_pair_diagnostics <= 0:
            raise ContractError("max_pair_diagnostics must be > 0")


@dataclass(frozen=True, slots=True)
class Elimination:
    stage: str
    subject: str
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AllocationPlan:
    worker_id: str
    verifier_id: str | None
    estimated_total_tokens: int
    estimated_cost_microunits: int
    estimated_latency_ms: int
    optimization_quality_bps: int
    required_evidence_class: int
    verification_status: str = "NOT_VERIFIED"


@dataclass(frozen=True, slots=True)
class GovernorDecision:
    task_id: str
    decision: str
    plan: AllocationPlan | None
    effective_independent_verifier_required: bool
    effective_verifier_required: bool
    freeze_reasons: tuple[str, ...]
    eliminations: tuple[Elimination, ...]
    policy_trace: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "decision": self.decision,
            "plan": asdict(self.plan) if self.plan is not None else None,
            "effective_independent_verifier_required": self.effective_independent_verifier_required,
            "effective_verifier_required": self.effective_verifier_required,
            "freeze_reasons": list(self.freeze_reasons),
            "eliminations": [
                {"stage": item.stage, "subject": item.subject, "reasons": list(item.reasons)}
                for item in self.eliminations
            ],
            "policy_trace": list(self.policy_trace),
        }


@dataclass(frozen=True, slots=True)
class _CandidatePlan:
    worker: AgentProfile
    verifier: AgentProfile | None
    total_tokens: int
    cost_microunits: int
    latency_ms: int
    quality_bps: int
