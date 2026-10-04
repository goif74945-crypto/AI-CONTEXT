from __future__ import annotations

from .model import (
    CompiledExperiment,
    Direction,
    EvidenceSignal,
    EvaluationEvidence,
    EvaluationResult,
    MetricKind,
    MetricObservation,
)
from .serialization import contract_hash
from .stats import observed_interval


def _validate_observation(kind: MetricKind, obs: MetricObservation) -> str | None:
    if obs.control_n <= 0 or obs.treatment_n <= 0:
        return "NON_POSITIVE_SAMPLE_SIZE"
    if kind is MetricKind.PROPORTION:
        if not 0.0 <= obs.control_value <= 1.0 or not 0.0 <= obs.treatment_value <= 1.0:
            return "PROPORTION_OUT_OF_RANGE"
    elif kind is MetricKind.MEAN:
        if obs.control_stddev is None or obs.treatment_stddev is None:
            return "MEAN_STDDEV_REQUIRED"
        if obs.control_stddev < 0.0 or obs.treatment_stddev < 0.0:
            return "MEAN_STDDEV_INVALID"
    return None


def _guardrail_degradation(direction: Direction, obs: MetricObservation) -> float:
    raw = obs.treatment_value - obs.control_value
    return -raw if direction is Direction.HIGHER_IS_BETTER else raw


def evaluate_experiment(contract: CompiledExperiment, evidence: EvaluationEvidence) -> EvaluationResult:
    reasons: list[str] = []

    expected_hash = contract_hash(contract)
    if evidence.contract_hash != expected_hash:
        return EvaluationResult(EvidenceSignal.FREEZE, ("CONTRACT_HASH_MISMATCH",), None)

    if not evidence.data_quality_ok or evidence.invariant_violations:
        reasons.append("DATA_QUALITY_BLOCKED")
        reasons.extend(f"INVARIANT:{x}" for x in evidence.invariant_violations)
        return EvaluationResult(EvidenceSignal.FREEZE, tuple(reasons), None)

    primary_error = _validate_observation(contract.primary_metric.kind, evidence.primary)
    if primary_error:
        return EvaluationResult(EvidenceSignal.FREEZE, (f"PRIMARY_OBSERVATION_INVALID:{primary_error}",), None)
    if evidence.primary.name != contract.primary_metric.name:
        return EvaluationResult(EvidenceSignal.FREEZE, ("PRIMARY_METRIC_NAME_MISMATCH",), None)

    for guardrail in contract.guardrails:
        obs = evidence.guardrails.get(guardrail.name)
        if obs is None:
            return EvaluationResult(EvidenceSignal.FREEZE, (f"GUARDRAIL_MISSING:{guardrail.name}",), None)
        if obs.name != guardrail.name:
            return EvaluationResult(EvidenceSignal.FREEZE, (f"GUARDRAIL_NAME_MISMATCH:{guardrail.name}",), None)
        if obs.control_n <= 0 or obs.treatment_n <= 0:
            return EvaluationResult(EvidenceSignal.FREEZE, (f"GUARDRAIL_SAMPLE_INVALID:{guardrail.name}",), None)
        degradation = _guardrail_degradation(guardrail.direction, obs)
        if degradation > guardrail.max_degradation_abs:
            return EvaluationResult(
                EvidenceSignal.FREEZE,
                (f"GUARDRAIL_BREACH:{guardrail.name}:{degradation:.12g}>{guardrail.max_degradation_abs:.12g}",),
                None,
            )

    if evidence.primary.control_n < contract.planned_sample_per_arm or evidence.primary.treatment_n < contract.planned_sample_per_arm:
        return EvaluationResult(
            EvidenceSignal.INCONCLUSIVE,
            (
                f"UNDERPOWERED:planned_per_arm={contract.planned_sample_per_arm}",
                f"observed_control={evidence.primary.control_n}",
                f"observed_treatment={evidence.primary.treatment_n}",
            ),
            None,
        )

    try:
        interval = observed_interval(contract.primary_metric, evidence.primary)
    except ValueError as exc:
        return EvaluationResult(EvidenceSignal.FREEZE, (f"PRIMARY_INTERVAL_ERROR:{exc}",), None)

    threshold = contract.primary_metric.mde_abs
    if interval.lower >= threshold:
        return EvaluationResult(
            EvidenceSignal.SUPPORTED,
            (f"MDE_CLEARED:lower={interval.lower:.12g}>=threshold={threshold:.12g}",),
            interval,
        )
    if interval.upper < threshold:
        return EvaluationResult(
            EvidenceSignal.REJECTED,
            (f"MDE_NOT_MET:upper={interval.upper:.12g}<threshold={threshold:.12g}",),
            interval,
        )
    return EvaluationResult(
        EvidenceSignal.INCONCLUSIVE,
        (f"MDE_INTERVAL_OVERLAP:lower={interval.lower:.12g},upper={interval.upper:.12g},threshold={threshold:.12g}",),
        interval,
    )
