from __future__ import annotations

from .compiler import compile_surface
from .model import (
    Action, Confirmation, DetailLevel, EvidenceStatus, Role,
    SurfaceInput, SurfacePlan, SystemState, TrustLabel,
)


def validate_plan(inp: SurfaceInput, plan: SurfacePlan) -> tuple[str, ...]:
    violations: list[str] = []

    if plan.action.enabled and not inp.backend_authorized:
        violations.append("ACTION_ENABLED_WITH_BACKEND_DENY")

    if plan.trust_label is TrustLabel.VERIFIED_FINAL:
        if inp.system_state is not SystemState.STABLE:
            violations.append("VERIFIED_FINAL_OUTSIDE_STABLE")
        if inp.evidence_status is not EvidenceStatus.PASS:
            violations.append("VERIFIED_FINAL_WITHOUT_PASS_EVIDENCE")
        if not inp.release_authorized:
            violations.append("VERIFIED_FINAL_WITHOUT_RELEASE_AUTH")

    if inp.system_state is SystemState.FREEZE:
        if plan.banner != "FREEZE":
            violations.append("FREEZE_BANNER_MISSING")
        if "FREEZE:AUTHORITATIVE" not in plan.mandatory_disclosures:
            violations.append("FREEZE_DISCLOSURE_MISSING")
        if plan.action.enabled and plan.action.action not in {
            Action.OPEN_TRACE, Action.EXPORT_AUDIT, Action.RECOVER_FREEZE,
        }:
            violations.append("FREEZE_ENABLED_ILLEGAL_ACTION")
        if plan.action.action is Action.RECOVER_FREEZE and plan.action.enabled:
            if inp.role is not Role.OWNER or not inp.recoverable:
                violations.append("RECOVERY_ENABLED_WITHOUT_OWNER_RECOVERABLE")

    if inp.system_state is SystemState.STOP:
        if plan.banner != "STOP":
            violations.append("STOP_BANNER_MISSING")
        if plan.action.enabled and plan.action.action not in {Action.OPEN_TRACE, Action.EXPORT_AUDIT}:
            violations.append("STOP_ENABLED_NON_DIAGNOSTIC_ACTION")

    if inp.irreversible and plan.action.confirmation is not Confirmation.TYPE_TO_CONFIRM:
        violations.append("IRREVERSIBLE_WITHOUT_TYPED_CONFIRMATION")

    if inp.system_state in {SystemState.FREEZE, SystemState.STOP} and plan.detail_level is not DetailLevel.FORENSIC:
        violations.append("BLOCKED_STATE_BELOW_FORENSIC_DETAIL")

    if plan.action.action in {Action.VIEW_RESULT, Action.EXPORT_ARTIFACT} and plan.action.enabled:
        if inp.system_state is not SystemState.STABLE:
            violations.append("RELEASE_ACTION_ENABLED_OUTSIDE_STABLE")
        if inp.evidence_status is not EvidenceStatus.PASS:
            violations.append("RELEASE_ACTION_ENABLED_WITHOUT_PASS")
        if not inp.release_authorized:
            violations.append("RELEASE_ACTION_ENABLED_WITHOUT_RELEASE_AUTH")

    if compile_surface(inp).fingerprint != plan.fingerprint:
        violations.append("NON_DETERMINISTIC_FINGERPRINT")

    return tuple(violations)


def assert_plan_valid(inp: SurfaceInput, plan: SurfacePlan) -> None:
    violations = validate_plan(inp, plan)
    if violations:
        raise AssertionError("; ".join(violations))
