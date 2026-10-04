from __future__ import annotations

import hashlib
import json

from .model import Disclosure, FreezeEvent, FreezeExplanation, ReasonCode, RecoveryIntent
from .policy import INTENT_PRIORITY, REASON_POLICIES


POLICY_VERSION = "freeze-bridge-policy/1.1"


def _eligible_intents(event: FreezeEvent) -> tuple[RecoveryIntent, ...]:
    policy = REASON_POLICIES[event.reason_code]
    authorized = set(event.authorized_recovery_intents)
    return tuple(
        intent
        for intent in INTENT_PRIORITY
        if intent in policy.allowed_intents and intent in authorized
    )


def _effective_dependency_recheck_safe(event: FreezeEvent) -> bool:
    policy = REASON_POLICIES[event.reason_code]
    if policy.force_dependency_recheck_unsafe:
        return False
    if RecoveryIntent.RECHECK_DEPENDENCY not in _eligible_intents(event):
        return False
    return event.dependency_recheck_safe


def _safe_evidence(event: FreezeEvent) -> tuple[str, ...]:
    policy = REASON_POLICIES[event.reason_code]
    if (
        event.disclosure is Disclosure.RESTRICTED
        and policy.suppress_evidence_when_restricted
    ):
        return ()
    if event.disclosure is Disclosure.RESTRICTED:
        return tuple(
            sorted(ref for ref in event.evidence_refs if ref.startswith("public:"))
        )
    return tuple(sorted(event.evidence_refs))


def _required_inputs(event: FreezeEvent) -> tuple[str, ...]:
    if event.reason_code is not ReasonCode.MISSING_REQUIRED_INPUT:
        return ()
    return tuple(sorted(event.missing_inputs))


def _fingerprint_payload(
    event: FreezeEvent,
    output_without_fingerprint: dict[str, object],
) -> str:
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
            "dependency_recheck_safe": event.dependency_recheck_safe,
            "missing_inputs": sorted(event.missing_inputs),
            "evidence_refs": sorted(event.evidence_refs),
            "authorized_recovery_intents": sorted(
                intent.value for intent in event.authorized_recovery_intents
            ),
            "context_label": event.context_label,
        },
        "explanation": output_without_fingerprint,
    }
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def compile_freeze_explanation(event: FreezeEvent) -> FreezeExplanation:
    policy = REASON_POLICIES[event.reason_code]
    intents = _eligible_intents(event)
    evidence = _safe_evidence(event)
    required_inputs = _required_inputs(event)
    recheck_safe = _effective_dependency_recheck_safe(event)

    output_without_fingerprint: dict[str, object] = {
        "protocol_version": event.protocol_version,
        "event_id": event.event_id,
        "status": event.status.value,
        "reason_code": event.reason_code.value,
        "title": policy.title(event.locale),
        "summary": policy.summary(event.locale),
        "blocking_layer": event.blocking_layer,
        "recovery_owner": event.recovery_owner.value,
        "required_inputs": list(required_inputs),
        "eligible_recovery_intents": [intent.value for intent in intents],
        "evidence_refs": list(evidence),
        "disclosure": event.disclosure.value,
        "dependency_recheck_safe": recheck_safe,
        "downstream_ui_authority_required": True,
    }
    fingerprint = _fingerprint_payload(event, output_without_fingerprint)

    return FreezeExplanation(
        protocol_version=event.protocol_version,
        event_id=event.event_id,
        status=event.status,
        reason_code=event.reason_code,
        title=policy.title(event.locale),
        summary=policy.summary(event.locale),
        blocking_layer=event.blocking_layer,
        recovery_owner=event.recovery_owner,
        required_inputs=required_inputs,
        eligible_recovery_intents=intents,
        evidence_refs=evidence,
        disclosure=event.disclosure,
        dependency_recheck_safe=recheck_safe,
        downstream_ui_authority_required=True,
        fingerprint=fingerprint,
    )


def compile_mapping(raw: dict[str, object]) -> dict[str, object]:
    event = FreezeEvent.from_mapping(raw)
    return compile_freeze_explanation(event).as_dict()
