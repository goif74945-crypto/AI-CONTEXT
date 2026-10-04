"""Assumption Liquidation Planner (ALP).

Ranks experiments by expected retired epistemic risk per unit of execution cost,
without promoting assumptions to facts. The planner is deterministic and budget
bounded; execution of an experiment is outside this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Assumption:
    assumption_id: str
    impact: float
    uncertainty: float
    blocks: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.assumption_id.strip():
            raise ValueError("assumption_id must be non-empty")
        for name, value in (("impact", self.impact), ("uncertainty", self.uncertainty)):
            if not isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be finite and in [0, 1]")

    @property
    def epistemic_risk(self) -> float:
        return self.impact * self.uncertainty


@dataclass(frozen=True, slots=True)
class Experiment:
    experiment_id: str
    resolves: frozenset[str]
    cost: float
    execution_risk: float = 0.0
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not self.experiment_id.strip():
            raise ValueError("experiment_id must be non-empty")
        if not self.resolves:
            raise ValueError("resolves must be non-empty")
        if not isfinite(self.cost) or self.cost <= 0:
            raise ValueError("cost must be finite and > 0")
        if not isfinite(self.execution_risk) or not 0.0 <= self.execution_risk <= 1.0:
            raise ValueError("execution_risk must be finite and in [0, 1]")
        if not isfinite(self.confidence) or not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be finite and in [0, 1]")


@dataclass(frozen=True, slots=True)
class PlannedExperiment:
    experiment_id: str
    marginal_risk_reduction: float
    utility: float
    cumulative_cost: float
    resolves: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ExperimentPlan:
    selected: tuple[PlannedExperiment, ...]
    remaining_assumptions: tuple[str, ...]
    total_cost: float
    expected_risk_reduction: float


def plan_experiments(
    assumptions: Iterable[Assumption],
    experiments: Iterable[Experiment],
    *,
    budget: float,
) -> ExperimentPlan:
    if not isfinite(budget) or budget < 0:
        raise ValueError("budget must be finite and >= 0")

    assumption_list = tuple(assumptions)
    if len({item.assumption_id for item in assumption_list}) != len(assumption_list):
        raise ValueError("assumption_id values must be unique")
    assumption_map = {item.assumption_id: item for item in assumption_list}

    experiment_list = tuple(experiments)
    if len({item.experiment_id for item in experiment_list}) != len(experiment_list):
        raise ValueError("experiment_id values must be unique")
    unknown_targets = sorted(
        {aid for item in experiment_list for aid in item.resolves if aid not in assumption_map}
    )
    if unknown_targets:
        raise ValueError(f"experiments reference unknown assumptions: {unknown_targets}")

    unresolved = set(assumption_map)
    selected: list[PlannedExperiment] = []
    spent = 0.0
    retired = 0.0
    remaining_experiments = {item.experiment_id: item for item in experiment_list}

    while remaining_experiments:
        candidates: list[tuple[float, float, str, Experiment, tuple[str, ...]]] = []
        for experiment in remaining_experiments.values():
            if spent + experiment.cost > budget + 1e-12:
                continue
            newly_resolved = tuple(sorted(unresolved.intersection(experiment.resolves)))
            raw_reduction = sum(assumption_map[aid].epistemic_risk for aid in newly_resolved)
            marginal = raw_reduction * experiment.confidence
            risk_adjusted_cost = experiment.cost * (1.0 + experiment.execution_risk)
            utility = marginal / risk_adjusted_cost if risk_adjusted_cost else 0.0
            # Sort descending utility, then marginal, then stable ID ascending.
            candidates.append((utility, marginal, experiment.experiment_id, experiment, newly_resolved))

        if not candidates:
            break
        candidates.sort(key=lambda row: (-row[0], -row[1], row[2]))
        utility, marginal, _, chosen, newly_resolved = candidates[0]
        if marginal <= 0.0:
            break

        spent += chosen.cost
        retired += marginal
        unresolved.difference_update(newly_resolved)
        selected.append(
            PlannedExperiment(
                experiment_id=chosen.experiment_id,
                marginal_risk_reduction=marginal,
                utility=utility,
                cumulative_cost=spent,
                resolves=newly_resolved,
            )
        )
        del remaining_experiments[chosen.experiment_id]

    return ExperimentPlan(
        selected=tuple(selected),
        remaining_assumptions=tuple(sorted(unresolved)),
        total_cost=spent,
        expected_risk_reduction=retired,
    )
