from __future__ import annotations

from dataclasses import replace

from .canonical import fingerprint
from .model import (
    Action, ActionDecision, Confirmation, DetailLevel, EvidenceStatus,
    RiskLevel, Role, SurfaceInput, SurfacePlan, SystemState, TrustLabel,
)
from .policy import MUTATING_ACTIONS, ROLE_SURFACE_CAPABILITIES

SCHEMA_VERSION = "nexy.prism.surface-plan.v0.1"

_DETAIL_RANK = {
    DetailLevel.COMPACT: 0,
    DetailLevel.STANDARD: 1,
    DetailLevel.FORENSIC: 2,
}


def _max_detail(a: DetailLevel, b: DetailLevel) -> DetailLevel:
    return a if _DETAIL_RANK[a] >= _DETAIL_RANK[b] else b


def _detect_conflicts(inp: SurfaceInput) -> tuple[str, ...]:
    conflicts: list[str] = []
    if inp.release_authorized and inp.system_state is not SystemState.STABLE:
        conflicts.append("RELEASE_AUTHORIZED_OUTSIDE_STABLE")
    if inp.release_authorized and inp.evidence_status is not EvidenceStatus.PASS:
        conflicts.append("RELEASE_AUTHORIZED_WITHOUT_PASS_EVIDENCE")
    if inp.system_state in {SystemState.FREEZE, SystemState.STOP} and inp.release_authorized:
        conflicts.append("RELEASE_AUTHORIZED_WHILE_BLOCKED")
    return tuple(sorted(set(conflicts)))


def _trust_label(inp: SurfaceInput, conflicts: tuple[str, ...]) -> TrustLabel:
    if conflicts:
        return TrustLabel.CONTRACT_CONFLICT
    if inp.system_state is SystemState.STOP:
        return TrustLabel.STOPPED
    if inp.system_state is SystemState.FREEZE:
        return TrustLabel.FROZEN
    if inp.system_state is SystemState.INIT:
        return TrustLabel.INITIALIZING
    if inp.system_state in {SystemState.RUNNING, SystemState.VERIFYING, SystemState.CONSENSUS}:
        return TrustLabel.IN_PROGRESS
    if (
        inp.system_state is SystemState.STABLE
        and inp.evidence_status is EvidenceStatus.PASS
        and inp.release_authorized
    ):
        return TrustLabel.VERIFIED_FINAL
    if inp.evidence_status in {EvidenceStatus.FAIL, EvidenceStatus.BLOCKED, EvidenceStatus.CONFLICT}:
        return TrustLabel.REJECTED
    if inp.evidence_status is not EvidenceStatus.PASS:
        return TrustLabel.UNVERIFIED
    return TrustLabel.READY_UNRELEASED


def _required_detail_floor(inp: SurfaceInput, conflicts: tuple[str, ...]) -> DetailLevel:
    if conflicts:
        return DetailLevel.FORENSIC
    if inp.system_state in {SystemState.FREEZE, SystemState.STOP}:
        return DetailLevel.FORENSIC
    if inp.irreversible or inp.risk is RiskLevel.CRITICAL:
        return DetailLevel.FORENSIC
    if inp.risk is RiskLevel.HIGH:
        return DetailLevel.STANDARD
    if inp.evidence_status is not EvidenceStatus.PASS:
        return DetailLevel.STANDARD
    if inp.requested_action in {Action.CONFIG_CHANGE, Action.HARD_DELETE, Action.RECOVER_FREEZE}:
        return DetailLevel.STANDARD
    return DetailLevel.COMPACT


def _confirmation(inp: SurfaceInput) -> Confirmation:
    if inp.irreversible or inp.requested_action is Action.HARD_DELETE:
        return Confirmation.TYPE_TO_CONFIRM
    if inp.requested_action in {Action.RECOVER_FREEZE, Action.CONFIG_CHANGE}:
        return Confirmation.CONFIRM
    if inp.requested_action is Action.SUBMIT_DIRECTIVE and inp.risk is RiskLevel.CRITICAL:
        return Confirmation.CONFIRM
    return Confirmation.NONE


def _decide_action(inp: SurfaceInput, conflicts: tuple[str, ...]) -> ActionDecision:
    confirmation = _confirmation(inp)
    action = inp.requested_action

    if conflicts:
        return ActionDecision(action, False, "INPUT_CONTRACT_CONFLICT", confirmation)

    if action not in ROLE_SURFACE_CAPABILITIES[inp.role]:
        return ActionDecision(action, False, "ROLE_SURFACE_DENY", confirmation)

    if not inp.backend_authorized:
        return ActionDecision(
            action, False, inp.backend_reason_code or "BACKEND_DENY", confirmation
        )

    if inp.system_state is SystemState.STOP:
        if action in {Action.OPEN_TRACE, Action.EXPORT_AUDIT}:
            return ActionDecision(action, True, "READ_ONLY_STOP_DIAGNOSTIC", confirmation)
        return ActionDecision(action, False, "SYSTEM_STOP", confirmation)

    if inp.system_state is SystemState.FREEZE:
        if action in {Action.OPEN_TRACE, Action.EXPORT_AUDIT}:
            return ActionDecision(action, True, "READ_ONLY_FREEZE_DIAGNOSTIC", confirmation)
        if action is Action.RECOVER_FREEZE:
            if inp.role is Role.OWNER and inp.recoverable:
                return ActionDecision(action, True, "OWNER_RECOVERY_ALLOWED", confirmation)
            return ActionDecision(action, False, "FREEZE_RECOVERY_DENIED", confirmation)
        return ActionDecision(action, False, "SYSTEM_FREEZE", confirmation)

    if action is Action.RECOVER_FREEZE:
        return ActionDecision(action, False, "NOT_IN_FREEZE", confirmation)

    if action is Action.VIEW_RESULT:
        if (
            inp.system_state is SystemState.STABLE
            and inp.evidence_status is EvidenceStatus.PASS
            and inp.release_authorized
        ):
            return ActionDecision(action, True, "RELEASED_RESULT", confirmation)
        return ActionDecision(action, False, "RESULT_NOT_RELEASED", confirmation)

    if action is Action.EXPORT_ARTIFACT:
        if (
            inp.system_state is SystemState.STABLE
            and inp.evidence_status is EvidenceStatus.PASS
            and inp.release_authorized
        ):
            return ActionDecision(action, True, "RELEASED_ARTIFACT", confirmation)
        return ActionDecision(action, False, "EXPORT_BLOCKED_UNRELEASED", confirmation)

    if action in {Action.CONFIG_CHANGE, Action.HARD_DELETE} and inp.system_state not in {
        SystemState.READY, SystemState.STABLE,
    }:
        return ActionDecision(action, False, "MUTATION_DEFERRED_DURING_ACTIVE_STATE", confirmation)

    if action in MUTATING_ACTIONS and inp.role in {Role.AUDITOR, Role.SYSTEM, Role.PUBLIC_USER}:
        return ActionDecision(action, False, "NON_MUTATING_ROLE", confirmation)

    return ActionDecision(action, True, "SURFACE_ALLOWED_BACKEND_AUTHORIZED", confirmation)


def _mandatory_disclosures(
    inp: SurfaceInput,
    action: ActionDecision,
    conflicts: tuple[str, ...],
) -> tuple[str, ...]:
    items: list[str] = [
        f"SYSTEM_STATE:{inp.system_state.value}",
        f"EVIDENCE_STATUS:{inp.evidence_status.value}",
        f"ROLE:{inp.role.value}",
    ]

    if conflicts:
        items.extend(f"CONTRACT_CONFLICT:{code}" for code in conflicts)

    if inp.system_state is SystemState.FREEZE:
        items.extend([
            "FREEZE:AUTHORITATIVE",
            f"INCIDENT_CODE:{inp.incident_code or 'UNKNOWN'}",
            f"BLOCKING_LAYER:{inp.blocking_layer or 'UNKNOWN'}",
            f"RECOVERABLE:{str(inp.recoverable).lower()}",
        ])

    if inp.system_state is SystemState.STOP:
        items.append("STOP:AUTHORITATIVE")

    if inp.evidence_status is not EvidenceStatus.PASS or not inp.release_authorized:
        items.append("OUTPUT_RELEASE:NOT_FINAL")
    elif inp.system_state is SystemState.STABLE:
        items.append("OUTPUT_RELEASE:AUTHORIZED")

    if inp.irreversible:
        items.append("IRREVERSIBLE_ACTION:true")

    if inp.risk in {RiskLevel.HIGH, RiskLevel.CRITICAL}:
        items.append(f"RISK:{inp.risk.value}")

    if not action.enabled:
        items.append(f"ACTION_BLOCKED:{action.reason_code}")

    if action.confirmation is not Confirmation.NONE:
        items.append(f"CONFIRMATION:{action.confirmation.value}")

    return tuple(dict.fromkeys(items))


def _optional_sections(inp: SurfaceInput, detail: DetailLevel) -> tuple[str, ...]:
    if detail is DetailLevel.COMPACT:
        return tuple()

    sections: list[str] = ["reason_summary", "next_legal_action"]
    if inp.role in {Role.OWNER, Role.OPERATOR, Role.AUDITOR}:
        sections.append("evidence_summary")
    if inp.role in {Role.OWNER, Role.AUDITOR}:
        sections.extend(["trace_link", "permission_boundary"])
    if detail is DetailLevel.FORENSIC:
        sections.extend(["state_transition_context", "recovery_or_rollback_context"])
    return tuple(dict.fromkeys(sections))


def _banner(inp: SurfaceInput, conflicts: tuple[str, ...]) -> str | None:
    # Blocked states must remain visually dominant even when upstream
    # facts are contradictory. Conflict is disclosed, never used to mask them.
    if inp.system_state is SystemState.FREEZE:
        return "FREEZE"
    if inp.system_state is SystemState.STOP:
        return "STOP"
    if conflicts:
        return "CONTRACT_CONFLICT"
    if inp.system_state in {SystemState.RUNNING, SystemState.VERIFYING, SystemState.CONSENSUS}:
        return inp.system_state.value
    return None


def compile_surface(inp: SurfaceInput) -> SurfacePlan:
    """Compile authoritative backend state into a truth-preserving UI plan.

    This does not grant permission, release output, recover state, or mutate
    NEXY. It can only make the presentation surface more restrictive.
    """
    conflicts = _detect_conflicts(inp)
    action = _decide_action(inp, conflicts)
    floor = _required_detail_floor(inp, conflicts)
    detail = _max_detail(inp.preferred_detail, floor)
    trust = _trust_label(inp, conflicts)
    disclosures = _mandatory_disclosures(inp, action, conflicts)
    optional_sections = _optional_sections(inp, detail)

    reasons = [action.reason_code]
    if detail is not inp.preferred_detail:
        reasons.append("DETAIL_RAISED_TO_TRUTH_FLOOR")
    if conflicts:
        reasons.append("FAIL_CLOSED_ON_INPUT_CONFLICT")

    draft = SurfacePlan(
        schema_version=SCHEMA_VERSION,
        trust_label=trust,
        detail_level=detail,
        banner=_banner(inp, conflicts),
        action=action,
        mandatory_disclosures=disclosures,
        optional_sections=optional_sections,
        conflict_codes=conflicts,
        reasons=tuple(reasons),
        fingerprint="",
    )
    digest = fingerprint({
        "input": inp.to_primitive(),
        "plan": draft.to_primitive(include_fingerprint=False),
    })
    return replace(draft, fingerprint=digest)
