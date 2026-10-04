from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class MetricKind(str, Enum):
    PROPORTION = "proportion"
    MEAN = "mean"


class Direction(str, Enum):
    HIGHER_IS_BETTER = "higher_is_better"
    LOWER_IS_BETTER = "lower_is_better"


class EvidenceSignal(str, Enum):
    SUPPORTED = "SUPPORTED"
    REJECTED = "REJECTED"
    INCONCLUSIVE = "INCONCLUSIVE"
    FREEZE = "FREEZE"


@dataclass(frozen=True, slots=True)
class MetricSpec:
    name: str
    kind: MetricKind
    direction: Direction
    baseline: float
    mde_abs: float
    alpha: float
    power: float
    planning_stddev: float | None = None


@dataclass(frozen=True, slots=True)
class GuardrailSpec:
    name: str
    direction: Direction
    baseline: float
    max_degradation_abs: float


@dataclass(frozen=True, slots=True)
class ExperimentProposal:
    experiment_id: str
    title: str
    hypothesis: str
    population: str
    primary_metric: MetricSpec
    guardrails: tuple[GuardrailSpec, ...]
    allocation_fraction: float
    duration_days: int
    risk_flags: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True, slots=True)
class CompiledExperiment:
    schema_version: str
    experiment_id: str
    title: str
    hypothesis: str
    population: str
    primary_metric: MetricSpec
    guardrails: tuple[GuardrailSpec, ...]
    allocation_fraction: float
    duration_days: int
    planned_sample_per_arm: int
    risk_flags: tuple[str, ...]
    authority: str = "human_product_decision"


@dataclass(frozen=True, slots=True)
class MetricObservation:
    name: str
    control_value: float
    treatment_value: float
    control_n: int
    treatment_n: int
    control_stddev: float | None = None
    treatment_stddev: float | None = None


@dataclass(frozen=True, slots=True)
class EvaluationEvidence:
    contract_hash: str
    primary: MetricObservation
    guardrails: Mapping[str, MetricObservation]
    data_quality_ok: bool = True
    invariant_violations: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class IntervalResult:
    effect_in_desired_direction: float
    lower: float
    upper: float
    p_value_vs_zero: float


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    signal: EvidenceSignal
    reasons: tuple[str, ...]
    primary_interval: IntervalResult | None
    human_decision_required: bool = True
