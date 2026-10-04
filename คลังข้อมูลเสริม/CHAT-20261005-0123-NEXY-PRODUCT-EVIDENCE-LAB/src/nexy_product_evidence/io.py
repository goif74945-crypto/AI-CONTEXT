from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import Direction, ExperimentProposal, GuardrailSpec, MetricKind, MetricSpec


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON must be an object")
    return value


def proposal_from_dict(raw: dict[str, Any]) -> ExperimentProposal:
    metric_raw = raw["primary_metric"]
    metric = MetricSpec(
        name=str(metric_raw["name"]),
        kind=MetricKind(metric_raw["kind"]),
        direction=Direction(metric_raw["direction"]),
        baseline=float(metric_raw["baseline"]),
        mde_abs=float(metric_raw["mde_abs"]),
        alpha=float(metric_raw["alpha"]),
        power=float(metric_raw["power"]),
        planning_stddev=(None if metric_raw.get("planning_stddev") is None else float(metric_raw["planning_stddev"])),
    )
    guardrails = tuple(
        GuardrailSpec(
            name=str(g["name"]),
            direction=Direction(g["direction"]),
            baseline=float(g["baseline"]),
            max_degradation_abs=float(g["max_degradation_abs"]),
        )
        for g in raw["guardrails"]
    )
    return ExperimentProposal(
        experiment_id=str(raw["experiment_id"]),
        title=str(raw["title"]),
        hypothesis=str(raw["hypothesis"]),
        population=str(raw["population"]),
        primary_metric=metric,
        guardrails=guardrails,
        allocation_fraction=float(raw["allocation_fraction"]),
        duration_days=int(raw["duration_days"]),
        risk_flags=frozenset(str(x) for x in raw.get("risk_flags", [])),
    )
