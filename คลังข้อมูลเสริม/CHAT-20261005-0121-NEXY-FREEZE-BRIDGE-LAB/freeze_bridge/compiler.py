from __future__ import annotations

import hashlib
import json

from .model import (
    ActionCode,
    Disclosure,
    FreezeEvent,
    RecoveryAction,
    RecoveryCard,
    ReasonCode,
)
from .policy import ACTION_PRIORITY, ACTION_TEXT, REASON_POLICIES


POLICY_VERSION = "freeze-bridge-policy/1.0"


def _effective_actions(event: FreezeEvent) -> tuple[ActionCode, ...]:
    policy = REASON_POLICIES[event.reason_code]
    allowed = policy.allowed_actions
    requested = set(event.authorized_actions)
    return tuple(action for action in ACTION_PRIORITY if action in allowed and action in requested)


def _effective_retryable(event: FreezeEvent) -> bool:
    policy = REASON_POLICIES[event.reason_code]
    if policy.force_non_retryable:
        return False
    if ActionCode.RETRY_AFTER_DEPENDENCY not in _effective_actions(event):
        return False
    return event.retryable


def _safe_evidence(event: FreezeEvent) -> tuple[str, ...]:
    policy = REASON_POLICIES[event.reason_code]
    if event.disclosure is Disclosure.RESTRICTED and policy.suppress_evidence_when_restricted:
        return ()
    if event.disclosure is Disclosure.RESTRICTED:
        return tuple(ref for ref in event.evidence_refs if ref.startswith("public:"))
    return tuple(sorted(event.evidence_refs))


def _needed(event: FreezeEvent) -> tuple[str, ...]:
    if event.reason_code is not ReasonCode.MISSING_REQUIRED_INPUT:
        return ()
    return tuple(sorted(event.missing_inputs))


def _make_actions(event: FreezeEvent) -> tuple[RecoveryAction, ...]:
    text_map = ACTION_TEXT[event.locale]
    return tuple(
        RecoveryAction(code=code, label=text_map[code][0], description=text_map[code][1])
        for code in _effective_actions(event)
    )


def _fingerprint_payload(event: FreezeEvent, card_without_fingerprint: dict[str, object]) -> str:
    canonical = {
        "policy_version": POLICY_VERSION,
        "event": {
            "protocol_version": event.protocol_version,
            "event_id": event.event_id,
            "reason_code": event.reason_code.value,
            "status": event.status.value,
            "blocking_layer": event.blocking_layer,
            "recovery_owner": event.recovery_owner.value,
            "disclosure": event.disclosure.value,
            "locale": event.locale.value,
            "retryable": event.retryable,
            "missing_inputs": sorted(event.missing_inputs),
            "evidence_refs": sorted(event.evidence_refs),
            "authorized_actions": sorted(action.value for action in event.authorized_actions),
            "context_label": event.context_label,
        },
        "card": card_without_fingerprint,
    }
    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def compile_recovery_card(event: FreezeEvent) -> RecoveryCard:
    policy = REASON_POLICIES[event.reason_code]
    actions = _make_actions(event)
    evidence = _safe_evidence(event)
    needed = _needed(event)
    retryable = _effective_retryable(event)

    card_without_fingerprint: dict[str, object] = {
        "protocol_version": event.protocol_version,
        "event_id": event.event_id,
        "status": event.status.value,
        "reason_code": event.reason_code.value,
        "title": policy.title(event.locale),
        "summary": policy.summary(event.locale),
        "blocking_layer": event.blocking_layer,
        "recovery_owner": event.recovery_owner.value,
        "needed": list(needed),
        "actions": [action.as_dict() for action in actions],
        "evidence_refs": list(evidence),
        "disclosure": event.disclosure.value,
        "retryable": retryable,
    }
    fingerprint = _fingerprint_payload(event, card_without_fingerprint)

    return RecoveryCard(
        protocol_version=event.protocol_version,
        event_id=event.event_id,
        status=event.status,
        reason_code=event.reason_code,
        title=policy.title(event.locale),
        summary=policy.summary(event.locale),
        blocking_layer=event.blocking_layer,
        recovery_owner=event.recovery_owner,
        needed=needed,
        actions=actions,
        evidence_refs=evidence,
        disclosure=event.disclosure,
        retryable=retryable,
        fingerprint=fingerprint,
    )


def compile_mapping(raw: dict[str, object]) -> dict[str, object]:
    event = FreezeEvent.from_mapping(raw)
    return compile_recovery_card(event).as_dict()
