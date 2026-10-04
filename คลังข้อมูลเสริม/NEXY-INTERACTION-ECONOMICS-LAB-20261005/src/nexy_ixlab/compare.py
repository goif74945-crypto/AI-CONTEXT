from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .model import InteractionPlan
from .scorer import PlanAssessment, assess_plan


class ComparisonVerdict(str, Enum):
    IMPROVEMENT = "IMPROVEMENT"
    REGRESSION = "REGRESSION"
    MIXED = "MIXED"
    EQUIVALENT = "EQUIVALENT"


@dataclass(frozen=True, slots=True)
class PlanComparison:
    baseline: PlanAssessment
    candidate: PlanAssessment
    friction_delta: float
    human_touch_delta: int
    blocking_touch_delta: int
    choice_bits_delta: float
    context_switch_delta: int
    wait_ms_delta: int
    new_error_codes: tuple[str, ...]
    resolved_error_codes: tuple[str, ...]
    verdict: ComparisonVerdict

    def to_mapping(self) -> dict[str, Any]:
        return {
            "baseline": self.baseline.to_mapping(),
            "candidate": self.candidate.to_mapping(),
            "friction_delta": self.friction_delta,
            "human_touch_delta": self.human_touch_delta,
            "blocking_touch_delta": self.blocking_touch_delta,
            "choice_bits_delta": self.choice_bits_delta,
            "context_switch_delta": self.context_switch_delta,
            "wait_ms_delta": self.wait_ms_delta,
            "new_error_codes": list(self.new_error_codes),
            "resolved_error_codes": list(self.resolved_error_codes),
            "verdict": self.verdict.value,
        }


def _error_codes(assessment: PlanAssessment) -> set[str]:
    return {f.code for f in assessment.findings if f.severity == "ERROR"}


def compare_plans(baseline_plan: InteractionPlan, candidate_plan: InteractionPlan) -> PlanComparison:
    baseline = assess_plan(baseline_plan)
    candidate = assess_plan(candidate_plan)
    baseline_errors = _error_codes(baseline)
    candidate_errors = _error_codes(candidate)
    new_errors = tuple(sorted(candidate_errors - baseline_errors))
    resolved_errors = tuple(sorted(baseline_errors - candidate_errors))

    friction_delta = round(candidate.friction_score - baseline.friction_score, 3)
    deltas = (
        candidate.human_touches - baseline.human_touches,
        candidate.blocking_touches - baseline.blocking_touches,
        round(candidate.choice_bits - baseline.choice_bits, 6),
        candidate.context_switches - baseline.context_switches,
        candidate.wait_ms - baseline.wait_ms,
    )

    if new_errors:
        verdict = ComparisonVerdict.REGRESSION
    else:
        metrics = (friction_delta, *deltas)
        any_better = any(x < 0 for x in metrics)
        any_worse = any(x > 0 for x in metrics)
        if any_better and not any_worse:
            verdict = ComparisonVerdict.IMPROVEMENT
        elif any_worse and not any_better:
            verdict = ComparisonVerdict.REGRESSION
        elif any_better and any_worse:
            verdict = ComparisonVerdict.MIXED
        elif resolved_errors:
            verdict = ComparisonVerdict.IMPROVEMENT
        else:
            verdict = ComparisonVerdict.EQUIVALENT

    return PlanComparison(
        baseline=baseline,
        candidate=candidate,
        friction_delta=friction_delta,
        human_touch_delta=deltas[0],
        blocking_touch_delta=deltas[1],
        choice_bits_delta=deltas[2],
        context_switch_delta=deltas[3],
        wait_ms_delta=deltas[4],
        new_error_codes=new_errors,
        resolved_error_codes=resolved_errors,
        verdict=verdict,
    )
