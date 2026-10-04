from __future__ import annotations

from dataclasses import dataclass

from .model import InteractionPlan, StepKind
from .scorer import PlanAssessment, assess_plan


@dataclass(frozen=True, slots=True)
class OptimizationResult:
    original: PlanAssessment
    optimized_plan: InteractionPlan
    optimized: PlanAssessment
    removed_step_ids: tuple[str, ...]
    suggestions: tuple[str, ...]


def optimize_plan(plan: InteractionPlan) -> OptimizationResult:
    """Apply only transformations whose safety preconditions are explicit.

    Everything else remains advisory. This intentionally favors false negatives
    (missed optimization) over authority/safety regressions.
    """
    by_id = {s.id: s for s in plan.steps}
    depended_on = {dep for item in plan.steps for dep in item.dependencies}
    removable: set[str] = set()
    for step in plan.steps:
        if step.kind is not StepKind.CONFIRMATION or step.required_by_law or not step.guards_step_id:
            continue
        target = by_id.get(step.guards_step_id)
        if (
            target is not None
            and (target.reversible or target.preauthorized)
            and step.id not in depended_on
        ):
            removable.add(step.id)

    retained = tuple(s for s in plan.steps if s.id not in removable)
    optimized_plan = InteractionPlan(name=f"{plan.name}::safe-optimized", steps=retained, budget=plan.budget)
    original = assess_plan(plan)
    optimized = assess_plan(optimized_plan)

    suggestions: list[str] = []
    clarifications = [s.id for s in retained if s.required and s.blocking and s.kind is StepKind.CLARIFICATION]
    if len(clarifications) > 1:
        suggestions.append("Consider batching independent blocking clarifications into one interruption after semantic-dependency review.")
    if optimized.choice_bits > plan.budget.max_choice_bits:
        suggestions.append("Consider progressive disclosure or hierarchical choice grouping; do not remove required choices.")
    if optimized.wait_ms > plan.budget.max_wait_ms:
        suggestions.append("Consider background execution/progress delivery when cancellation and dependency semantics permit.")
    if optimized.context_switches > plan.budget.max_context_switches:
        suggestions.append("Consider consolidating tool/surface transitions to reduce user context switching.")
    if optimized.human_touches > 0 and optimized.blocking_touches == optimized.human_touches:
        suggestions.append("Review whether all user touches truly need to block execution; preserve authority-required blocks.")

    return OptimizationResult(
        original=original,
        optimized_plan=optimized_plan,
        optimized=optimized,
        removed_step_ids=tuple(sorted(removable)),
        suggestions=tuple(suggestions),
    )
