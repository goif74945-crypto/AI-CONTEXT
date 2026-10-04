from __future__ import annotations

from dataclasses import asdict, dataclass
from math import log2
from typing import Any

from .model import InteractionPlan, StepKind, USER_TOUCH_KINDS


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    severity: str
    message: str
    step_id: str | None = None


@dataclass(frozen=True, slots=True)
class PlanAssessment:
    plan_name: str
    friction_score: float
    human_touches: int
    blocking_touches: int
    choice_bits: float
    context_switches: int
    wait_ms: int
    user_effort: float
    freeze_steps: int
    unguarded_irreversible_actions: tuple[str, ...]
    redundant_confirmations: tuple[str, ...]
    findings: tuple[Finding, ...]

    @property
    def passed_budget(self) -> bool:
        return not any(f.severity == "ERROR" for f in self.findings)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "plan_name": self.plan_name,
            "friction_score": self.friction_score,
            "human_touches": self.human_touches,
            "blocking_touches": self.blocking_touches,
            "choice_bits": self.choice_bits,
            "context_switches": self.context_switches,
            "wait_ms": self.wait_ms,
            "user_effort": self.user_effort,
            "freeze_steps": self.freeze_steps,
            "unguarded_irreversible_actions": list(self.unguarded_irreversible_actions),
            "redundant_confirmations": list(self.redundant_confirmations),
            "passed_budget": self.passed_budget,
            "findings": [asdict(f) for f in self.findings],
        }


def _choice_bits(choice_count: int) -> float:
    return log2(choice_count) if choice_count >= 2 else 0.0


def assess_plan(plan: InteractionPlan) -> PlanAssessment:
    by_id = {s.id: s for s in plan.steps}
    touches = sum(1 for s in plan.steps if s.required and s.kind in USER_TOUCH_KINDS)
    blocking = sum(1 for s in plan.steps if s.required and s.blocking and s.kind in USER_TOUCH_KINDS)
    choice_bits = sum(_choice_bits(s.choice_count) for s in plan.steps if s.required)
    switches = sum(s.context_switches for s in plan.steps if s.required)
    wait_ms = sum(s.estimated_wait_ms for s in plan.steps if s.required)
    effort = sum(s.user_effort for s in plan.steps if s.required and s.kind in USER_TOUCH_KINDS)
    freeze_steps = sum(1 for s in plan.steps if s.required and s.kind is StepKind.FREEZE)

    guarded_targets = {
        s.guards_step_id
        for s in plan.steps
        if s.required and s.kind is StepKind.CONFIRMATION and s.guards_step_id
    }
    unguarded = tuple(
        s.id
        for s in plan.steps
        if s.required
        and s.kind is StepKind.IRREVERSIBLE_ACTION
        and not s.reversible
        and not s.preauthorized
        and s.id not in guarded_targets
    )

    redundant: list[str] = []
    findings: list[Finding] = []
    for step in plan.steps:
        if step.kind is not StepKind.CONFIRMATION or not step.required:
            continue
        target = by_id.get(step.guards_step_id) if step.guards_step_id else None
        if target is None:
            findings.append(Finding("IXF-STRUCT-GUARD-TARGET", "ERROR", "Confirmation does not reference a valid guarded step", step.id))
            continue
        if not step.required_by_law and (target.reversible or target.preauthorized):
            redundant.append(step.id)
            findings.append(Finding("IXF-REDUNDANT-CONFIRM", "WARN", "Confirmation guards an explicitly reversible or preauthorized action", step.id))

    for step_id in unguarded:
        findings.append(Finding("IXF-UNGUARDED-IRREVERSIBLE", "ERROR", "Irreversible non-preauthorized action has no confirmation guard", step_id))

    wait_penalty = min(15.0, (wait_ms / 1000.0) * 1.5)
    raw_score = (
        touches * 12.0
        + blocking * 10.0
        + choice_bits * 5.0
        + switches * 7.0
        + wait_penalty
        + effort * 2.0
        + freeze_steps * 8.0
    )
    score = round(min(100.0, raw_score), 3)

    budget = plan.budget
    if score > budget.max_friction_score:
        findings.append(Finding("IXF-BUDGET-SCORE", "ERROR", f"friction_score {score} exceeds budget {budget.max_friction_score}"))
    if blocking > budget.max_blocking_touches:
        findings.append(Finding("IXF-BUDGET-BLOCKING", "ERROR", f"blocking_touches {blocking} exceeds budget {budget.max_blocking_touches}"))
    if choice_bits > budget.max_choice_bits:
        findings.append(Finding("IXF-BUDGET-CHOICE", "ERROR", f"choice_bits {choice_bits:.3f} exceeds budget {budget.max_choice_bits}"))
    if switches > budget.max_context_switches:
        findings.append(Finding("IXF-BUDGET-SWITCH", "ERROR", f"context_switches {switches} exceeds budget {budget.max_context_switches}"))
    if wait_ms > budget.max_wait_ms:
        findings.append(Finding("IXF-BUDGET-WAIT", "ERROR", f"wait_ms {wait_ms} exceeds budget {budget.max_wait_ms}"))

    for step in plan.steps:
        if step.required and step.kind in USER_TOUCH_KINDS and not step.justification:
            findings.append(Finding("IXF-TOUCH-NO-JUSTIFICATION", "WARN", "User touch has no explicit justification", step.id))

    return PlanAssessment(
        plan_name=plan.name,
        friction_score=score,
        human_touches=touches,
        blocking_touches=blocking,
        choice_bits=round(choice_bits, 6),
        context_switches=switches,
        wait_ms=wait_ms,
        user_effort=round(effort, 3),
        freeze_steps=freeze_steps,
        unguarded_irreversible_actions=unguarded,
        redundant_confirmations=tuple(redundant),
        findings=tuple(findings),
    )
