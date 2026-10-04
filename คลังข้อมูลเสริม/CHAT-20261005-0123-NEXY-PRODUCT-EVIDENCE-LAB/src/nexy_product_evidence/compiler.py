from __future__ import annotations

import math
import re

from .errors import ExperimentValidationError, ValidationIssue
from .model import CompiledExperiment, Direction, ExperimentProposal, MetricKind, MetricSpec
from .stats import sample_size_per_arm


_PROHIBITED_RISK_FLAGS = frozenset({
    "dark_pattern",
    "coercion",
    "deception_without_consent",
    "privacy_violation",
    "safety_bypass",
    "security_bypass",
})
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")


def _finite(value: float) -> bool:
    return math.isfinite(value)


def _validate_metric(spec: MetricSpec, field: str, issues: list[ValidationIssue]) -> None:
    if not spec.name.strip():
        issues.append(ValidationIssue("METRIC_NAME_REQUIRED", f"{field}.name", "metric name is required"))
    if not _finite(spec.baseline):
        issues.append(ValidationIssue("BASELINE_NOT_FINITE", f"{field}.baseline", "baseline must be finite"))
    if not _finite(spec.mde_abs) or spec.mde_abs <= 0.0:
        issues.append(ValidationIssue("MDE_INVALID", f"{field}.mde_abs", "MDE must be finite and > 0"))
    if not 0.0 < spec.alpha < 1.0:
        issues.append(ValidationIssue("ALPHA_INVALID", f"{field}.alpha", "alpha must be between 0 and 1"))
    if not 0.5 < spec.power < 1.0:
        issues.append(ValidationIssue("POWER_INVALID", f"{field}.power", "power must be > 0.5 and < 1"))

    if spec.kind is MetricKind.PROPORTION:
        if not 0.0 < spec.baseline < 1.0:
            issues.append(ValidationIssue("PROPORTION_BASELINE_INVALID", f"{field}.baseline", "proportion baseline must be between 0 and 1"))
        target = spec.baseline + spec.mde_abs if spec.direction is Direction.HIGHER_IS_BETTER else spec.baseline - spec.mde_abs
        if not 0.0 < target < 1.0:
            issues.append(ValidationIssue("PROPORTION_TARGET_INVALID", field, "baseline +/- MDE must remain between 0 and 1"))
        if spec.planning_stddev is not None:
            issues.append(ValidationIssue("STDDEV_NOT_ALLOWED", f"{field}.planning_stddev", "proportion metrics do not use planning_stddev"))
    elif spec.kind is MetricKind.MEAN:
        if spec.planning_stddev is None or not _finite(spec.planning_stddev) or spec.planning_stddev <= 0.0:
            issues.append(ValidationIssue("STDDEV_REQUIRED", f"{field}.planning_stddev", "mean metrics require finite planning_stddev > 0"))


def compile_experiment(proposal: ExperimentProposal) -> CompiledExperiment:
    issues: list[ValidationIssue] = []

    if not _ID_RE.fullmatch(proposal.experiment_id):
        issues.append(ValidationIssue("EXPERIMENT_ID_INVALID", "experiment_id", "use 3-128 characters from A-Z a-z 0-9 . _ : - and start alphanumeric"))
    if not proposal.title.strip():
        issues.append(ValidationIssue("TITLE_REQUIRED", "title", "title is required"))
    if not proposal.hypothesis.strip():
        issues.append(ValidationIssue("HYPOTHESIS_REQUIRED", "hypothesis", "hypothesis is required"))
    if not proposal.population.strip():
        issues.append(ValidationIssue("POPULATION_REQUIRED", "population", "population is required"))
    if proposal.allocation_fraction != 0.5:
        issues.append(ValidationIssue("ALLOCATION_UNSUPPORTED", "allocation_fraction", "reference v1 supports only deterministic 50/50 allocation planning"))
    if proposal.duration_days <= 0:
        issues.append(ValidationIssue("DURATION_INVALID", "duration_days", "duration_days must be positive"))
    if not proposal.guardrails:
        issues.append(ValidationIssue("GUARDRAIL_REQUIRED", "guardrails", "at least one explicit guardrail is required"))

    prohibited = sorted(flag for flag in proposal.risk_flags if flag in _PROHIBITED_RISK_FLAGS)
    if prohibited:
        issues.append(ValidationIssue("PROHIBITED_RISK", "risk_flags", "prohibited risk flags: " + ", ".join(prohibited)))

    _validate_metric(proposal.primary_metric, "primary_metric", issues)

    seen: set[str] = set()
    for idx, g in enumerate(proposal.guardrails):
        path = f"guardrails[{idx}]"
        if not g.name.strip():
            issues.append(ValidationIssue("GUARDRAIL_NAME_REQUIRED", f"{path}.name", "guardrail name is required"))
        if g.name in seen:
            issues.append(ValidationIssue("GUARDRAIL_DUPLICATE", f"{path}.name", "guardrail names must be unique"))
        seen.add(g.name)
        if not _finite(g.baseline):
            issues.append(ValidationIssue("GUARDRAIL_BASELINE_NOT_FINITE", f"{path}.baseline", "baseline must be finite"))
        if not _finite(g.max_degradation_abs) or g.max_degradation_abs < 0.0:
            issues.append(ValidationIssue("GUARDRAIL_THRESHOLD_INVALID", f"{path}.max_degradation_abs", "threshold must be finite and >= 0"))

    if issues:
        raise ExperimentValidationError(issues)

    planned = sample_size_per_arm(proposal.primary_metric)
    return CompiledExperiment(
        schema_version="npel.contract.v1",
        experiment_id=proposal.experiment_id,
        title=proposal.title.strip(),
        hypothesis=proposal.hypothesis.strip(),
        population=proposal.population.strip(),
        primary_metric=proposal.primary_metric,
        guardrails=tuple(proposal.guardrails),
        allocation_fraction=proposal.allocation_fraction,
        duration_days=proposal.duration_days,
        planned_sample_per_arm=planned,
        risk_flags=tuple(sorted(proposal.risk_flags)),
    )
