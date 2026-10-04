from __future__ import annotations

from dataclasses import dataclass

from .common import ContractError, fingerprint, require_text, require_unit
from .q64 import Q64

_ALLOWED_EFFECTS = {"VIEW_ONLY", "REVERSIBLE_STATE"}


@dataclass(frozen=True, slots=True)
class ExperimentProposal:
    proposal_id: str
    effect_class: str
    information_gain: Q64
    risk: Q64
    blast_radius: Q64
    rollback_confidence: Q64
    pilot_cost: Q64
    sample_budget: int
    rollback_procedure_id: str
    stop_rule_id: str

    def __post_init__(self) -> None:
        require_text(self.proposal_id, "proposal_id")
        if self.effect_class not in _ALLOWED_EFFECTS:
            raise ContractError("effect_class must be reversible")
        for field in ("information_gain", "risk", "blast_radius", "rollback_confidence", "pilot_cost"):
            require_unit(getattr(self, field), field)
        if not isinstance(self.sample_budget, int) or isinstance(self.sample_budget, bool) or self.sample_budget <= 0:
            raise ContractError("sample_budget must be positive int")
        require_text(self.rollback_procedure_id, "rollback_procedure_id")
        require_text(self.stop_rule_id, "stop_rule_id")


@dataclass(frozen=True, slots=True)
class ExperimentPolicy:
    min_information_gain: Q64
    max_risk: Q64
    max_blast_radius: Q64
    min_rollback_confidence: Q64
    max_sample_budget: int
    max_treatment_fraction: Q64
    min_option_value: Q64
    risk_weight: Q64
    blast_weight: Q64
    cost_weight: Q64

    def __post_init__(self) -> None:
        for field in (
            "min_information_gain", "max_risk", "max_blast_radius", "min_rollback_confidence",
            "max_treatment_fraction", "risk_weight", "blast_weight", "cost_weight"
        ):
            require_unit(getattr(self, field), field)
        if not isinstance(self.min_option_value, Q64):
            raise ContractError("min_option_value must be Q64.64")
        if not isinstance(self.max_sample_budget, int) or isinstance(self.max_sample_budget, bool) or self.max_sample_budget <= 0:
            raise ContractError("max_sample_budget must be positive int")


@dataclass(frozen=True, slots=True)
class ExperimentPlan:
    status: str
    reason: str
    proposal_id: str
    option_value: Q64
    treatment_fraction: Q64
    treatment_budget: int
    control_budget: int
    rollback_procedure_id: str | None
    stop_rule_id: str | None
    fingerprint: str


def plan_experiment(proposal: ExperimentProposal, policy: ExperimentPolicy) -> ExperimentPlan:
    option_value = (
        proposal.information_gain * proposal.rollback_confidence
        - policy.risk_weight * proposal.risk
        - policy.blast_weight * proposal.blast_radius
        - policy.cost_weight * proposal.pilot_cost
    )
    if proposal.information_gain.raw < policy.min_information_gain.raw:
        return _result("REJECT", "INSUFFICIENT_INFORMATION_GAIN", proposal, option_value, Q64.zero(), 0, 0)
    if proposal.risk.raw > policy.max_risk.raw:
        return _result("REJECT", "RISK_TOO_HIGH", proposal, option_value, Q64.zero(), 0, 0)
    if proposal.blast_radius.raw > policy.max_blast_radius.raw:
        return _result("REJECT", "BLAST_RADIUS_TOO_HIGH", proposal, option_value, Q64.zero(), 0, 0)
    if proposal.rollback_confidence.raw < policy.min_rollback_confidence.raw:
        return _result("REJECT", "ROLLBACK_CONFIDENCE_TOO_LOW", proposal, option_value, Q64.zero(), 0, 0)
    if proposal.sample_budget > policy.max_sample_budget:
        return _result("REJECT", "SAMPLE_BUDGET_TOO_HIGH", proposal, option_value, Q64.zero(), 0, 0)
    if option_value.raw < policy.min_option_value.raw:
        return _result("HOLD", "OPTION_VALUE_BELOW_THRESHOLD", proposal, option_value, Q64.zero(), 0, proposal.sample_budget)

    denominator = Q64.one() + proposal.risk + proposal.blast_radius + proposal.pilot_cost
    raw_fraction = proposal.information_gain / denominator
    treatment_fraction = raw_fraction.min(policy.max_treatment_fraction)
    if treatment_fraction.raw <= 0:
        return _result("REJECT", "ZERO_SAFE_TREATMENT_FRACTION", proposal, option_value, Q64.zero(), 0, proposal.sample_budget)
    treatment_budget = (proposal.sample_budget * treatment_fraction.raw) // (1 << 64)
    if treatment_budget <= 0:
        treatment_budget = 1
    if treatment_budget >= proposal.sample_budget:
        treatment_budget = proposal.sample_budget - 1 if proposal.sample_budget > 1 else 1
    control_budget = proposal.sample_budget - treatment_budget
    if control_budget <= 0:
        return _result("REJECT", "NO_CONTROL_HOLDOUT", proposal, option_value, Q64.zero(), 0, proposal.sample_budget)
    return _result("PLAN", "POSITIVE_REVERSIBLE_INFORMATION_OPTION", proposal, option_value, treatment_fraction, treatment_budget, control_budget)


def _result(status: str, reason: str, proposal: ExperimentProposal, option_value: Q64, fraction: Q64, treatment: int, control: int) -> ExperimentPlan:
    rollback = proposal.rollback_procedure_id if status == "PLAN" else None
    stop = proposal.stop_rule_id if status == "PLAN" else None
    core = {
        "status": status,
        "reason": reason,
        "proposal_id": proposal.proposal_id,
        "option_value": option_value,
        "treatment_fraction": fraction,
        "treatment_budget": treatment,
        "control_budget": control,
        "rollback_procedure_id": rollback,
        "stop_rule_id": stop,
    }
    return ExperimentPlan(status, reason, proposal.proposal_id, option_value, fraction, treatment, control, rollback, stop, fingerprint(core))
