from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


class FreezeBridgeError(ValueError):
    """Raised when an input cannot be normalized into the protocol contract."""


class Locale(str, Enum):
    EN = "en"
    TH = "th"


class FreezeStatus(str, Enum):
    FROZEN = "FROZEN"
    BLOCKED = "BLOCKED"
    NOT_VERIFIED = "NOT_VERIFIED"
    UNKNOWN = "UNKNOWN"
    CONFLICT = "CONFLICT"


class Disclosure(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"


class RecoveryOwner(str, Enum):
    USER = "USER"
    OPERATOR = "OPERATOR"
    SYSTEM = "SYSTEM"
    EXTERNAL_DEPENDENCY = "EXTERNAL_DEPENDENCY"
    NONE = "NONE"


class ReasonCode(str, Enum):
    MISSING_REQUIRED_INPUT = "MISSING_REQUIRED_INPUT"
    AUTHORITY_CONFLICT = "AUTHORITY_CONFLICT"
    POLICY_CONFLICT = "POLICY_CONFLICT"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    DEPENDENCY_UNAVAILABLE = "DEPENDENCY_UNAVAILABLE"
    SECURITY_INTEGRITY = "SECURITY_INTEGRITY"
    INVALID_STATE_TRANSITION = "INVALID_STATE_TRANSITION"
    STALE_EVIDENCE = "STALE_EVIDENCE"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    INTERNAL_INVARIANT = "INTERNAL_INVARIANT"
    UNKNOWN_REASON = "UNKNOWN_REASON"


class ActionCode(str, Enum):
    PROVIDE_MISSING_INPUT = "PROVIDE_MISSING_INPUT"
    REVIEW_CONFLICT = "REVIEW_CONFLICT"
    RETRY_AFTER_DEPENDENCY = "RETRY_AFTER_DEPENDENCY"
    OPEN_EVIDENCE = "OPEN_EVIDENCE"
    REQUEST_AUTHORITY_REVIEW = "REQUEST_AUTHORITY_REVIEW"
    CONTACT_OPERATOR = "CONTACT_OPERATOR"
    ACKNOWLEDGE = "ACKNOWLEDGE"
    CHANGE_SCOPE = "CHANGE_SCOPE"
    WAIT_FOR_SYSTEM = "WAIT_FOR_SYSTEM"


CONTROL_CHARACTERS = {chr(i) for i in range(0x20)} - {"\t"}


def _clean_text(value: Any, *, field_name: str, max_length: int) -> str:
    if not isinstance(value, str):
        raise FreezeBridgeError(f"{field_name} must be a string")
    value = value.strip()
    if not value:
        raise FreezeBridgeError(f"{field_name} must not be empty")
    if any(ch in CONTROL_CHARACTERS for ch in value):
        raise FreezeBridgeError(f"{field_name} contains forbidden control characters")
    if len(value) > max_length:
        raise FreezeBridgeError(f"{field_name} exceeds max length {max_length}")
    return value


def _clean_optional_text(value: Any, *, field_name: str, max_length: int) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise FreezeBridgeError(f"{field_name} must be a string or null")
    value = value.strip()
    if not value:
        return None
    if any(ch in CONTROL_CHARACTERS for ch in value):
        raise FreezeBridgeError(f"{field_name} contains forbidden control characters")
    if len(value) > max_length:
        raise FreezeBridgeError(f"{field_name} exceeds max length {max_length}")
    return value


def _clean_string_list(
    value: Any,
    *,
    field_name: str,
    max_items: int,
    item_max_length: int,
) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise FreezeBridgeError(f"{field_name} must be a list of strings")
    if len(value) > max_items:
        raise FreezeBridgeError(f"{field_name} exceeds max items {max_items}")
    cleaned: list[str] = []
    seen: set[str] = set()
    for index, raw in enumerate(value):
        item = _clean_text(raw, field_name=f"{field_name}[{index}]", max_length=item_max_length)
        if item not in seen:
            cleaned.append(item)
            seen.add(item)
    return tuple(cleaned)


def _parse_enum(enum_type: type[Enum], value: Any, *, field_name: str, fallback: Enum | None = None) -> Enum:
    if not isinstance(value, str):
        if fallback is not None:
            return fallback
        raise FreezeBridgeError(f"{field_name} must be a string")
    try:
        return enum_type(value)
    except ValueError:
        if fallback is not None:
            return fallback
        allowed = ", ".join(member.value for member in enum_type)
        raise FreezeBridgeError(f"{field_name} must be one of: {allowed}") from None


@dataclass(frozen=True, slots=True)
class FreezeEvent:
    event_id: str
    reason_code: ReasonCode
    status: FreezeStatus
    blocking_layer: str
    recovery_owner: RecoveryOwner
    disclosure: Disclosure = Disclosure.PUBLIC
    locale: Locale = Locale.EN
    retryable: bool = False
    missing_inputs: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    authorized_actions: tuple[ActionCode, ...] = field(default_factory=tuple)
    context_label: str | None = None
    protocol_version: str = "1.0"

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "FreezeEvent":
        if not isinstance(raw, Mapping):
            raise FreezeBridgeError("event must be an object")

        protocol_version = _clean_text(raw.get("protocol_version", "1.0"), field_name="protocol_version", max_length=16)
        if protocol_version != "1.0":
            raise FreezeBridgeError("unsupported protocol_version")

        event_id = _clean_text(raw.get("event_id"), field_name="event_id", max_length=128)
        blocking_layer = _clean_text(raw.get("blocking_layer"), field_name="blocking_layer", max_length=96)
        context_label = _clean_optional_text(raw.get("context_label"), field_name="context_label", max_length=160)

        reason_code = _parse_enum(
            ReasonCode,
            raw.get("reason_code", ReasonCode.UNKNOWN_REASON.value),
            field_name="reason_code",
            fallback=ReasonCode.UNKNOWN_REASON,
        )
        status = _parse_enum(FreezeStatus, raw.get("status"), field_name="status")
        recovery_owner = _parse_enum(RecoveryOwner, raw.get("recovery_owner"), field_name="recovery_owner")
        disclosure = _parse_enum(Disclosure, raw.get("disclosure", Disclosure.PUBLIC.value), field_name="disclosure")
        locale = _parse_enum(Locale, raw.get("locale", Locale.EN.value), field_name="locale")

        retryable = raw.get("retryable", False)
        if not isinstance(retryable, bool):
            raise FreezeBridgeError("retryable must be a boolean")

        missing_inputs = _clean_string_list(
            raw.get("missing_inputs"), field_name="missing_inputs", max_items=24, item_max_length=96
        )
        evidence_refs = _clean_string_list(
            raw.get("evidence_refs"), field_name="evidence_refs", max_items=24, item_max_length=160
        )

        raw_actions = raw.get("authorized_actions", ())
        if isinstance(raw_actions, (str, bytes)) or not isinstance(raw_actions, Sequence):
            raise FreezeBridgeError("authorized_actions must be a list")
        if len(raw_actions) > len(ActionCode):
            raise FreezeBridgeError("authorized_actions exceeds supported action count")
        actions: list[ActionCode] = []
        seen_actions: set[ActionCode] = set()
        for index, value in enumerate(raw_actions):
            action = _parse_enum(ActionCode, value, field_name=f"authorized_actions[{index}]")
            assert isinstance(action, ActionCode)
            if action not in seen_actions:
                actions.append(action)
                seen_actions.add(action)

        return cls(
            event_id=event_id,
            reason_code=reason_code,  # type: ignore[arg-type]
            status=status,  # type: ignore[arg-type]
            blocking_layer=blocking_layer,
            recovery_owner=recovery_owner,  # type: ignore[arg-type]
            disclosure=disclosure,  # type: ignore[arg-type]
            locale=locale,  # type: ignore[arg-type]
            retryable=retryable,
            missing_inputs=missing_inputs,
            evidence_refs=evidence_refs,
            authorized_actions=tuple(actions),
            context_label=context_label,
            protocol_version=protocol_version,
        )


@dataclass(frozen=True, slots=True)
class RecoveryAction:
    code: ActionCode
    label: str
    description: str

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code.value,
            "label": self.label,
            "description": self.description,
        }


@dataclass(frozen=True, slots=True)
class RecoveryCard:
    protocol_version: str
    event_id: str
    status: FreezeStatus
    reason_code: ReasonCode
    title: str
    summary: str
    blocking_layer: str
    recovery_owner: RecoveryOwner
    needed: tuple[str, ...]
    actions: tuple[RecoveryAction, ...]
    evidence_refs: tuple[str, ...]
    disclosure: Disclosure
    retryable: bool
    fingerprint: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "protocol_version": self.protocol_version,
            "event_id": self.event_id,
            "status": self.status.value,
            "reason_code": self.reason_code.value,
            "title": self.title,
            "summary": self.summary,
            "blocking_layer": self.blocking_layer,
            "recovery_owner": self.recovery_owner.value,
            "needed": list(self.needed),
            "actions": [action.as_dict() for action in self.actions],
            "evidence_refs": list(self.evidence_refs),
            "disclosure": self.disclosure.value,
            "retryable": self.retryable,
            "fingerprint": self.fingerprint,
        }
