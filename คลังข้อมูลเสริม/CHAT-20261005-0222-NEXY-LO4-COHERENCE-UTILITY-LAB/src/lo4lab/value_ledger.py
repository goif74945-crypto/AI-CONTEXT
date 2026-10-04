from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite

from .canonical import fingerprint


class ValueLedgerError(ValueError):
    pass


class Direction(str, Enum):
    HIGHER_IS_BETTER = "HIGHER_IS_BETTER"
    LOWER_IS_BETTER = "LOWER_IS_BETTER"


_EVIDENCE_RANK = {"E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4, "E5": 5, "E6": 6, "E7": 7}


@dataclass(frozen=True, slots=True)
class ValueContract:
    proposal_id: str
    mechanism: str
    user_outcome: str
    primary_metric: str
    direction: Direction
    minimum_effect: float
    guard_metric: str
    maximum_guard_regression: float
    falsifier: str
    guard_direction: Direction = Direction.LOWER_IS_BETTER

    def __post_init__(self) -> None:
        for field_name in ("proposal_id", "mechanism", "user_outcome", "primary_metric", "guard_metric", "falsifier"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueLedgerError(f"{field_name} must be non-empty")
        if self.primary_metric == self.guard_metric:
            raise ValueLedgerError("primary_metric and guard_metric must differ")
        if not isinstance(self.direction, Direction):
            raise ValueLedgerError("direction must be a Direction")
        if not isinstance(self.guard_direction, Direction):
            raise ValueLedgerError("guard_direction must be a Direction")
        for field_name in ("minimum_effect", "maximum_guard_regression"):
            value = getattr(self, field_name)
            if not isfinite(value) or value < 0:
                raise ValueLedgerError(f"{field_name} must be finite and non-negative")


@dataclass(frozen=True, slots=True)
class ExperimentObservation:
    baseline_primary: float
    candidate_primary: float
    baseline_guard: float
    candidate_guard: float
    sample_count: int
    evidence_class: str
    falsifier_triggered: bool = False

    def __post_init__(self) -> None:
        for field_name in ("baseline_primary", "candidate_primary", "baseline_guard", "candidate_guard"):
            if not isfinite(getattr(self, field_name)):
                raise ValueLedgerError(f"{field_name} must be finite")
        if not isinstance(self.sample_count, int) or self.sample_count < 0:
            raise ValueLedgerError("sample_count must be non-negative int")
        if self.evidence_class not in _EVIDENCE_RANK:
            raise ValueLedgerError("unknown evidence_class")


@dataclass(frozen=True, slots=True)
class ValueAssessment:
    status: str
    primary_effect: float
    guard_regression: float
    reason_codes: tuple[str, ...]
    advisory_only: bool
    assessment_fingerprint: str


def assess_value(
    contract: ValueContract,
    observation: ExperimentObservation,
    *,
    minimum_samples: int = 20,
    minimum_evidence_class: str = "E2",
) -> ValueAssessment:
    if minimum_samples < 1:
        raise ValueLedgerError("minimum_samples must be >= 1")
    if minimum_evidence_class not in _EVIDENCE_RANK:
        raise ValueLedgerError("unknown minimum_evidence_class")

    raw_effect = observation.candidate_primary - observation.baseline_primary
    primary_effect = raw_effect if contract.direction == Direction.HIGHER_IS_BETTER else -raw_effect
    raw_guard_change = observation.candidate_guard - observation.baseline_guard
    guard_regression = (
        raw_guard_change
        if contract.guard_direction == Direction.LOWER_IS_BETTER
        else -raw_guard_change
    )

    reasons: list[str] = []
    if observation.sample_count < minimum_samples:
        reasons.append("INSUFFICIENT_SAMPLE")
    if _EVIDENCE_RANK[observation.evidence_class] < _EVIDENCE_RANK[minimum_evidence_class]:
        reasons.append("INSUFFICIENT_EVIDENCE_CLASS")
    if observation.falsifier_triggered:
        reasons.append("FALSIFIER_TRIGGERED")
    if primary_effect < contract.minimum_effect:
        reasons.append("PRIMARY_EFFECT_BELOW_THRESHOLD")
    if guard_regression > contract.maximum_guard_regression:
        reasons.append("GUARD_REGRESSION_EXCEEDED")

    if "FALSIFIER_TRIGGERED" in reasons or "GUARD_REGRESSION_EXCEEDED" in reasons:
        status = "FALSIFIED"
    elif "INSUFFICIENT_SAMPLE" in reasons or "INSUFFICIENT_EVIDENCE_CLASS" in reasons:
        status = "NOT_VERIFIED"
    elif "PRIMARY_EFFECT_BELOW_THRESHOLD" in reasons:
        status = "NO_SUPPORTED_BENEFIT"
    else:
        status = "BENEFIT_SUPPORTED"
        reasons.append("CAUSAL_CONTRACT_THRESHOLDS_MET")

    payload = {
        "proposal_id": contract.proposal_id,
        "status": status,
        "primary_effect": primary_effect,
        "guard_regression": guard_regression,
        "reason_codes": sorted(reasons),
        "advisory_only": True,
    }
    return ValueAssessment(
        status=status,
        primary_effect=primary_effect,
        guard_regression=guard_regression,
        reason_codes=tuple(sorted(reasons)),
        advisory_only=True,
        assessment_fingerprint=fingerprint(payload),
    )
