from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

from confirmation_coalescer import InteractionBatch
from human_agency_lab import Decision, InteractionDecision, ReasonCode


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical_json(value)).hexdigest()


class SemanticContractError(ValueError):
    pass


class StaleFrameError(SemanticContractError):
    pass


class AuthorityBindingError(SemanticContractError):
    pass


class SurfaceMode(str, Enum):
    SILENT = "SILENT"
    PREVIEW = "PREVIEW"
    CONFIRM = "CONFIRM"
    FREEZE = "FREEZE"


class SurfaceEvent(str, Enum):
    INSPECT = "INSPECT"
    ACKNOWLEDGE = "ACKNOWLEDGE"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    CANCEL = "CANCEL"
    REQUEST_REMEDIATION = "REQUEST_REMEDIATION"


class EventDisposition(str, Enum):
    INSPECTION_REQUESTED = "INSPECTION_REQUESTED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    APPROVAL_REQUESTED = "APPROVAL_REQUESTED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    REMEDIATION_REQUESTED = "REMEDIATION_REQUESTED"


@dataclass(frozen=True)
class ReasonPresentation:
    code: str
    label: str
    summary: str
    severity: str

    def canonical_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "label": self.label,
            "severity": self.severity,
            "summary": self.summary,
        }


_REASON_PRESENTATIONS: dict[ReasonCode, ReasonPresentation] = {
    ReasonCode.LOW_RISK_REVERSIBLE: ReasonPresentation(
        ReasonCode.LOW_RISK_REVERSIBLE.value,
        "Bounded reversible action",
        "The action is low risk and has a reversible path.",
        "info",
    ),
    ReasonCode.USER_AUTHORITY_MISSING: ReasonPresentation(
        ReasonCode.USER_AUTHORITY_MISSING.value,
        "Authority is missing",
        "Explicit authority for this impact is not available.",
        "critical",
    ),
    ReasonCode.IRREVERSIBLE_WITHOUT_ROLLBACK: ReasonPresentation(
        ReasonCode.IRREVERSIBLE_WITHOUT_ROLLBACK.value,
        "Recovery is unavailable",
        "The proposed effect cannot be safely rolled back.",
        "critical",
    ),
    ReasonCode.DESTRUCTIVE_ACTION: ReasonPresentation(
        ReasonCode.DESTRUCTIVE_ACTION.value,
        "Destructive effect",
        "The action can delete or materially replace state.",
        "critical",
    ),
    ReasonCode.SENSITIVE_EXTERNAL_EFFECT: ReasonPresentation(
        ReasonCode.SENSITIVE_EXTERNAL_EFFECT.value,
        "Sensitive external effect",
        "Sensitive data may cross the local control boundary.",
        "critical",
    ),
    ReasonCode.MATERIAL_COST: ReasonPresentation(
        ReasonCode.MATERIAL_COST.value,
        "Material cost",
        "The action may create a material financial effect.",
        "warning",
    ),
    ReasonCode.BROAD_SCOPE: ReasonPresentation(
        ReasonCode.BROAD_SCOPE.value,
        "Broad scope",
        "The proposed action affects a broad surface.",
        "warning",
    ),
    ReasonCode.HIGH_AMBIGUITY: ReasonPresentation(
        ReasonCode.HIGH_AMBIGUITY.value,
        "High ambiguity",
        "Material parts of the requested effect remain unclear.",
        "critical",
    ),
    ReasonCode.MODERATE_AMBIGUITY: ReasonPresentation(
        ReasonCode.MODERATE_AMBIGUITY.value,
        "Review ambiguity",
        "Some details should be reviewed before continuing.",
        "warning",
    ),
    ReasonCode.LOW_CONFIDENCE: ReasonPresentation(
        ReasonCode.LOW_CONFIDENCE.value,
        "Evidence confidence is low",
        "The available evidence does not support high confidence.",
        "warning",
    ),
    ReasonCode.PREVIEW_RECOMMENDED: ReasonPresentation(
        ReasonCode.PREVIEW_RECOMMENDED.value,
        "Preview recommended",
        "Reviewing the proposed effect can reduce avoidable risk.",
        "warning",
    ),
    ReasonCode.REQUIRED_CONFIRMATION: ReasonPresentation(
        ReasonCode.REQUIRED_CONFIRMATION.value,
        "Confirmation required",
        "The action cannot proceed from presentation state alone.",
        "critical",
    ),
    ReasonCode.ATTENTION_BUDGET_CONSTRAINED: ReasonPresentation(
        ReasonCode.ATTENTION_BUDGET_CONSTRAINED.value,
        "Attention budget constrained",
        "A soft preview was suppressed without weakening a hard gate.",
        "info",
    ),
}


def reason_presentation(reason: ReasonCode | str) -> ReasonPresentation:
    try:
        normalized = reason if isinstance(reason, ReasonCode) else ReasonCode(reason)
    except ValueError as error:
        raise SemanticContractError(f"unknown reason code: {reason!r}") from error
    return _REASON_PRESENTATIONS[normalized]


@dataclass(frozen=True)
class ActionReasonMap:
    action_id: str
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.action_id.strip():
            raise SemanticContractError("action_id must be non-empty")
        if len(self.reasons) != len(set(self.reasons)):
            raise SemanticContractError("duplicate reason code for action")
        for reason in self.reasons:
            reason_presentation(reason)

    def canonical_dict(self) -> dict[str, Any]:
        return {"action_id": self.action_id, "reasons": list(self.reasons)}


@dataclass(frozen=True)
class SemanticSource:
    source_digest: str
    decision: Decision
    hard_gate: bool
    action_reasons: tuple[ActionReasonMap, ...]
    authority_digest: str
    decision_policy_digest: str

    def __post_init__(self) -> None:
        for name in ("source_digest", "authority_digest", "decision_policy_digest"):
            if not str(getattr(self, name)).strip():
                raise SemanticContractError(f"{name} must be non-empty")
        if not self.action_reasons:
            raise SemanticContractError("at least one action mapping is required")
        action_ids = [item.action_id for item in self.action_reasons]
        if len(action_ids) != len(set(action_ids)):
            raise SemanticContractError("duplicate action mapping")
        if self.decision in (Decision.CONFIRM, Decision.FREEZE) and not self.hard_gate:
            raise SemanticContractError("CONFIRM/FREEZE source must preserve hard_gate")

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "action_reasons": [
                item.canonical_dict()
                for item in sorted(self.action_reasons, key=lambda item: item.action_id)
            ],
            "authority_digest": self.authority_digest,
            "decision": self.decision.value,
            "decision_policy_digest": self.decision_policy_digest,
            "hard_gate": self.hard_gate,
            "source_digest": self.source_digest,
        }


def source_from_decision(
    decision: InteractionDecision,
    *,
    authority_digest: str,
    decision_policy_digest: str,
) -> SemanticSource:
    return SemanticSource(
        source_digest=decision.digest(),
        decision=decision.decision,
        hard_gate=decision.hard_gate,
        action_reasons=(
            ActionReasonMap(
                decision.action_id,
                tuple(reason.value for reason in decision.reasons),
            ),
        ),
        authority_digest=authority_digest,
        decision_policy_digest=decision_policy_digest,
    )


def source_from_batch(batch: InteractionBatch) -> SemanticSource:
    return SemanticSource(
        source_digest=batch.digest(),
        decision=batch.decision,
        hard_gate=batch.decision in (Decision.CONFIRM, Decision.FREEZE),
        action_reasons=tuple(
            ActionReasonMap(item.action_id, item.reason_codes)
            for item in batch.explanations
        ),
        authority_digest=batch.authority_digest,
        decision_policy_digest=batch.decision_policy_digest,
    )


@dataclass(frozen=True)
class ControlSpec:
    event: SurfaceEvent
    label: str
    primary: bool
    requires_backend_authorization: bool

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "event": self.event.value,
            "label": self.label,
            "primary": self.primary,
            "requires_backend_authorization": self.requires_backend_authorization,
        }


@dataclass(frozen=True)
class AccessibilitySemantics:
    surface_role: str
    live_region: str
    initial_focus: str
    escape_behavior: str
    keyboard_order: tuple[str, ...]
    non_color_cues: tuple[str, ...]

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "escape_behavior": self.escape_behavior,
            "initial_focus": self.initial_focus,
            "keyboard_order": list(self.keyboard_order),
            "live_region": self.live_region,
            "non_color_cues": list(self.non_color_cues),
            "surface_role": self.surface_role,
        }


@dataclass(frozen=True)
class SemanticFrame:
    contract_version: str
    mode: SurfaceMode
    source: SemanticSource
    headline: str
    reason_presentations: tuple[ReasonPresentation, ...]
    controls: tuple[ControlSpec, ...]
    accessibility: AccessibilitySemantics

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "accessibility": self.accessibility.canonical_dict(),
            "contract_version": self.contract_version,
            "controls": [control.canonical_dict() for control in self.controls],
            "headline": self.headline,
            "mode": self.mode.value,
            "reason_presentations": [
                reason.canonical_dict() for reason in self.reason_presentations
            ],
            "source": self.source.canonical_dict(),
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


_MODE_BY_DECISION = {
    Decision.PROCEED: SurfaceMode.SILENT,
    Decision.PREVIEW: SurfaceMode.PREVIEW,
    Decision.CONFIRM: SurfaceMode.CONFIRM,
    Decision.FREEZE: SurfaceMode.FREEZE,
}


def _controls(mode: SurfaceMode) -> tuple[ControlSpec, ...]:
    if mode is SurfaceMode.SILENT:
        return tuple()
    if mode is SurfaceMode.PREVIEW:
        return (
            ControlSpec(SurfaceEvent.ACKNOWLEDGE, "Continue", True, False),
            ControlSpec(SurfaceEvent.INSPECT, "Inspect details", False, False),
            ControlSpec(SurfaceEvent.CANCEL, "Cancel", False, False),
        )
    if mode is SurfaceMode.CONFIRM:
        return (
            ControlSpec(SurfaceEvent.APPROVE, "Request approval", True, True),
            ControlSpec(SurfaceEvent.REJECT, "Reject", False, False),
            ControlSpec(SurfaceEvent.INSPECT, "Inspect evidence", False, False),
        )
    return (
        ControlSpec(
            SurfaceEvent.REQUEST_REMEDIATION,
            "Request remediation",
            True,
            True,
        ),
        ControlSpec(SurfaceEvent.INSPECT, "Inspect blocker", False, False),
    )


def _accessibility(mode: SurfaceMode, controls: tuple[ControlSpec, ...]) -> AccessibilitySemantics:
    order = tuple(control.event.value for control in controls)
    if mode is SurfaceMode.SILENT:
        return AccessibilitySemantics(
            "status", "off", "none", "none", order, ("text", "state-code")
        )
    if mode is SurfaceMode.PREVIEW:
        return AccessibilitySemantics(
            "dialog", "polite", "headline", "CANCEL", order, ("text", "icon")
        )
    if mode is SurfaceMode.CONFIRM:
        return AccessibilitySemantics(
            "alertdialog", "assertive", "headline", "REJECT", order, ("text", "icon")
        )
    return AccessibilitySemantics(
        "alertdialog",
        "assertive",
        "blocker-headline",
        "NO_DISMISS",
        order,
        ("text", "icon", "state-code"),
    )


def compile_semantic_frame(source: SemanticSource) -> SemanticFrame:
    mode = _MODE_BY_DECISION[source.decision]
    controls = _controls(mode)
    unique_reasons = sorted(
        {reason for item in source.action_reasons for reason in item.reasons}
    )
    presentations = tuple(reason_presentation(reason) for reason in unique_reasons)
    headline = {
        SurfaceMode.SILENT: "No interruption required",
        SurfaceMode.PREVIEW: "Review before continuing",
        SurfaceMode.CONFIRM: "Explicit approval is required",
        SurfaceMode.FREEZE: "Execution is frozen",
    }[mode]
    return SemanticFrame(
        contract_version="agency-semantic/v1",
        mode=mode,
        source=source,
        headline=headline,
        reason_presentations=presentations,
        controls=controls,
        accessibility=_accessibility(mode, controls),
    )


@dataclass(frozen=True)
class SurfaceResponse:
    frame_digest: str
    event: SurfaceEvent
    actor_authority_digest: str = ""


@dataclass(frozen=True)
class TransitionRecord:
    frame_digest: str
    source_digest: str
    event: SurfaceEvent
    disposition: EventDisposition
    backend_authorization_required: bool
    execution_authorized: bool

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "backend_authorization_required": self.backend_authorization_required,
            "disposition": self.disposition.value,
            "event": self.event.value,
            "execution_authorized": self.execution_authorized,
            "frame_digest": self.frame_digest,
            "source_digest": self.source_digest,
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


_DISPOSITION = {
    SurfaceEvent.INSPECT: EventDisposition.INSPECTION_REQUESTED,
    SurfaceEvent.ACKNOWLEDGE: EventDisposition.ACKNOWLEDGED,
    SurfaceEvent.APPROVE: EventDisposition.APPROVAL_REQUESTED,
    SurfaceEvent.REJECT: EventDisposition.REJECTED,
    SurfaceEvent.CANCEL: EventDisposition.CANCELLED,
    SurfaceEvent.REQUEST_REMEDIATION: EventDisposition.REMEDIATION_REQUESTED,
}


def apply_surface_event(
    frame: SemanticFrame,
    response: SurfaceResponse,
) -> TransitionRecord:
    frame_digest = frame.digest()
    if response.frame_digest != frame_digest:
        raise StaleFrameError("response is bound to a stale or different frame")
    controls = {control.event: control for control in frame.controls}
    if response.event not in controls:
        raise SemanticContractError(
            f"event {response.event.value} is not legal for {frame.mode.value}"
        )
    control = controls[response.event]
    if control.requires_backend_authorization:
        if response.actor_authority_digest != frame.source.authority_digest:
            raise AuthorityBindingError("actor authority does not match frame authority")
    return TransitionRecord(
        frame_digest=frame_digest,
        source_digest=frame.source.source_digest,
        event=response.event,
        disposition=_DISPOSITION[response.event],
        backend_authorization_required=control.requires_backend_authorization,
        execution_authorized=False,
    )


@dataclass(frozen=True)
class SemanticAudit:
    frames: int
    action_mappings: int
    modes: Mapping[str, int]
    legal_events: int
    digest: str


def audit_frames(frames: Iterable[SemanticFrame]) -> SemanticAudit:
    materialized = tuple(frames)
    mode_counts = {mode.value: 0 for mode in SurfaceMode}
    for frame in materialized:
        mode_counts[frame.mode.value] += 1
    payload = [frame.canonical_dict() for frame in materialized]
    return SemanticAudit(
        frames=len(materialized),
        action_mappings=sum(len(frame.source.action_reasons) for frame in materialized),
        modes=mode_counts,
        legal_events=sum(len(frame.controls) for frame in materialized),
        digest=_digest(payload),
    )
