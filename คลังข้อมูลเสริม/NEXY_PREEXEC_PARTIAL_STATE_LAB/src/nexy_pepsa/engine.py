from __future__ import annotations

import fnmatch
import heapq
from collections import defaultdict

from .canonical import canonical_hash
from .models import (
    AnalysisReport,
    ExecutionPlan,
    Finding,
    PartialState,
    Policy,
    Severity,
    Step,
    StepKind,
    Verdict,
)


class PlanStructureError(ValueError):
    pass


_SEVERITY_ORDER = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.INFO: 2}


def _step_map(plan: ExecutionPlan) -> dict[str, Step]:
    mapping: dict[str, Step] = {}
    for step in plan.steps:
        if step.id in mapping:
            raise PlanStructureError(f"duplicate step id: {step.id}")
        mapping[step.id] = step
    return mapping


def deterministic_topological_order(plan: ExecutionPlan) -> tuple[Step, ...]:
    steps = _step_map(plan)
    indegree = {step_id: 0 for step_id in steps}
    dependents: dict[str, list[str]] = defaultdict(list)

    for step in plan.steps:
        if step.id in step.depends_on:
            raise PlanStructureError(f"step {step.id} depends on itself")
        for dependency in step.depends_on:
            if dependency not in steps:
                raise PlanStructureError(f"step {step.id} depends on missing step {dependency}")
            indegree[step.id] += 1
            dependents[dependency].append(step.id)

    ready = [step_id for step_id, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    order: list[Step] = []

    while ready:
        current_id = heapq.heappop(ready)
        order.append(steps[current_id])
        for child_id in sorted(dependents.get(current_id, [])):
            indegree[child_id] -= 1
            if indegree[child_id] == 0:
                heapq.heappush(ready, child_id)

    if len(order) != len(plan.steps):
        cyclic = sorted(step_id for step_id, degree in indegree.items() if degree > 0)
        raise PlanStructureError(f"dependency cycle detected among: {', '.join(cyclic)}")
    return tuple(order)


def _is_protected(resource: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatchcase(resource, pattern) for pattern in patterns)


def _findings_for_step(step: Step, policy: Policy, *, is_terminal: bool) -> list[Finding]:
    findings: list[Finding] = []

    if step.boundary not in policy.allowed_boundaries:
        findings.append(
            Finding(
                code="BOUNDARY_NOT_ALLOWED",
                severity=Severity.ERROR,
                message=f"boundary {step.boundary!r} is not allowed by policy",
                step_id=step.id,
                resource=step.resource,
            )
        )

    if step.is_mutating and _is_protected(step.resource, policy.protected_resources):
        findings.append(
            Finding(
                code="PROTECTED_RESOURCE_MUTATION",
                severity=Severity.ERROR,
                message="mutating step targets a protected resource",
                step_id=step.id,
                resource=step.resource,
            )
        )

    if step.kind is StepKind.READ:
        if step.reversible or step.rollback_strategy:
            findings.append(
                Finding(
                    code="READ_ROLLBACK_METADATA",
                    severity=Severity.ERROR,
                    message="READ step must not declare rollback metadata",
                    step_id=step.id,
                    resource=step.resource,
                )
            )
        return findings

    if policy.require_postcondition_for_mutation and not step.postcondition:
        findings.append(
            Finding(
                code="MISSING_POSTCONDITION",
                severity=Severity.ERROR,
                message="mutating step must declare a postcondition",
                step_id=step.id,
                resource=step.resource,
            )
        )

    if policy.require_evidence_for_mutation and not step.evidence_required:
        findings.append(
            Finding(
                code="MISSING_EVIDENCE_REQUIREMENT",
                severity=Severity.ERROR,
                message="mutating step must declare at least one evidence requirement",
                step_id=step.id,
                resource=step.resource,
            )
        )

    if step.reversible and not step.rollback_strategy:
        findings.append(
            Finding(
                code="REVERSIBLE_WITHOUT_ROLLBACK",
                severity=Severity.ERROR,
                message="reversible step must declare a rollback strategy",
                step_id=step.id,
                resource=step.resource,
            )
        )
    if not step.reversible and step.rollback_strategy:
        findings.append(
            Finding(
                code="ROLLBACK_ON_IRREVERSIBLE_STEP",
                severity=Severity.ERROR,
                message="irreversible step cannot claim a rollback strategy",
                step_id=step.id,
                resource=step.resource,
            )
        )

    if step.kind is StepKind.EXTERNAL_EFFECT and policy.require_idempotency_for_external and not step.idempotency_key:
        findings.append(
            Finding(
                code="MISSING_IDEMPOTENCY_KEY",
                severity=Severity.ERROR,
                message="external side effect requires an idempotency key",
                step_id=step.id,
                resource=step.resource,
            )
        )

    if not step.reversible:
        if not step.approval_id:
            findings.append(
                Finding(
                    code="IRREVERSIBLE_WITHOUT_APPROVAL",
                    severity=Severity.ERROR,
                    message="irreversible mutation requires explicit approval_id",
                    step_id=step.id,
                    resource=step.resource,
                )
            )
        elif is_terminal and policy.allow_terminal_irreversible_with_approval:
            findings.append(
                Finding(
                    code="APPROVED_TERMINAL_IRREVERSIBLE",
                    severity=Severity.INFO,
                    message="terminal irreversible mutation is explicitly approved",
                    step_id=step.id,
                    resource=step.resource,
                )
            )
        elif not is_terminal:
            findings.append(
                Finding(
                    code="NONTERMINAL_IRREVERSIBLE_MUTATION",
                    severity=Severity.ERROR,
                    message="irreversible mutation occurs before the end of the deterministic execution order",
                    step_id=step.id,
                    resource=step.resource,
                )
            )
        else:
            findings.append(
                Finding(
                    code="IRREVERSIBLE_MUTATION_FORBIDDEN",
                    severity=Severity.ERROR,
                    message="policy forbids terminal irreversible mutations even with approval",
                    step_id=step.id,
                    resource=step.resource,
                )
            )

    return findings


def _partial_states(order: tuple[Step, ...]) -> tuple[PartialState, ...]:
    residual: dict[str, set[str]] = defaultdict(set)
    applied: list[str] = []
    states: list[PartialState] = []

    for index, step in enumerate(order):
        if index > 0:
            dirty_resources = tuple(sorted(resource for resource, owners in residual.items() if owners))
            if dirty_resources:
                states.append(
                    PartialState(
                        failure_before_step=step.id,
                        already_applied_steps=tuple(applied),
                        residual_resources=dirty_resources,
                        reason="a failure at this boundary would leave prior mutations without declared rollback coverage",
                    )
                )

        applied.append(step.id)
        if step.is_mutating and not step.rollback_covered:
            residual[step.resource].add(step.id)

    return tuple(states)


def _plan_hash_payload(plan: ExecutionPlan) -> dict[str, object]:
    return {
        "plan_id": plan.plan_id,
        "steps": [
            {
                "id": step.id,
                "kind": step.kind.value,
                "resource": step.resource,
                "boundary": step.boundary,
                "depends_on": sorted(step.depends_on),
                "reversible": step.reversible,
                "rollback_strategy": step.rollback_strategy,
                "approval_id": step.approval_id,
                "idempotency_key": step.idempotency_key,
                "postcondition": step.postcondition,
                "evidence_required": sorted(step.evidence_required),
            }
            for step in sorted(plan.steps, key=lambda item: item.id)
        ],
    }


def _policy_hash_payload(policy: Policy) -> dict[str, object]:
    return {
        "policy_id": policy.policy_id,
        "allowed_boundaries": sorted(policy.allowed_boundaries),
        "protected_resources": sorted(policy.protected_resources),
        "max_steps": policy.max_steps,
        "require_postcondition_for_mutation": policy.require_postcondition_for_mutation,
        "require_evidence_for_mutation": policy.require_evidence_for_mutation,
        "require_idempotency_for_external": policy.require_idempotency_for_external,
        "allow_terminal_irreversible_with_approval": policy.allow_terminal_irreversible_with_approval,
    }


def analyze(plan: ExecutionPlan, policy: Policy) -> AnalysisReport:
    order = deterministic_topological_order(plan)
    findings: list[Finding] = []

    if len(plan.steps) > policy.max_steps:
        findings.append(
            Finding(
                code="STEP_LIMIT_EXCEEDED",
                severity=Severity.ERROR,
                message=f"plan has {len(plan.steps)} steps; policy max is {policy.max_steps}",
            )
        )

    for index, step in enumerate(order):
        findings.extend(_findings_for_step(step, policy, is_terminal=index == len(order) - 1))

    partial_states = _partial_states(order)
    for state in partial_states:
        findings.append(
            Finding(
                code="UNSAFE_PARTIAL_STATE",
                severity=Severity.ERROR,
                message=(
                    f"failure before {state.failure_before_step} can leave residual resources: "
                    f"{', '.join(state.residual_resources)}"
                ),
                step_id=state.failure_before_step,
            )
        )

    findings.sort(
        key=lambda item: (
            _SEVERITY_ORDER[item.severity],
            item.code,
            item.step_id or "",
            item.resource or "",
            item.message,
        )
    )

    verdict = Verdict.FREEZE if any(item.severity is Severity.ERROR for item in findings) else Verdict.READY
    plan_hash = canonical_hash(_plan_hash_payload(plan))
    policy_hash = canonical_hash(_policy_hash_payload(policy))
    combined_hash = canonical_hash({"plan_hash": plan_hash, "policy_hash": policy_hash, "report_version": "1.0"})

    mutating = sum(1 for step in order if step.is_mutating)
    irreversible = sum(1 for step in order if step.is_mutating and not step.reversible)
    rollback_covered = sum(1 for step in order if step.rollback_covered)
    stats = {
        "steps": len(order),
        "mutating_steps": mutating,
        "irreversible_steps": irreversible,
        "rollback_covered_steps": rollback_covered,
        "error_findings": sum(1 for item in findings if item.severity is Severity.ERROR),
        "warning_findings": sum(1 for item in findings if item.severity is Severity.WARNING),
        "info_findings": sum(1 for item in findings if item.severity is Severity.INFO),
        "unsafe_partial_states": len(partial_states),
    }

    return AnalysisReport(
        report_version="1.0",
        plan_id=plan.plan_id,
        policy_id=policy.policy_id,
        verdict=verdict,
        plan_hash=plan_hash,
        policy_hash=policy_hash,
        combined_hash=combined_hash,
        ordered_steps=tuple(step.id for step in order),
        findings=tuple(findings),
        partial_states=partial_states,
        stats=stats,
    )
