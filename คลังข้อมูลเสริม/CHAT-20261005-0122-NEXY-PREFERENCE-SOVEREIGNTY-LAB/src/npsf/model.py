from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, TypeAlias

JsonScalar: TypeAlias = str | bool | int


class ScopeKind(str, Enum):
    USER = "USER"
    PROJECT = "PROJECT"
    SESSION = "SESSION"
    TASK = "TASK"


SCOPE_SPECIFICITY: Mapping[ScopeKind, int] = {
    ScopeKind.USER: 10,
    ScopeKind.PROJECT: 20,
    ScopeKind.SESSION: 30,
    ScopeKind.TASK: 40,
}


class PreferenceState(str, Enum):
    CANDIDATE = "CANDIDATE"
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    SUPERSEDED = "SUPERSEDED"


class Provenance(str, Enum):
    EXPLICIT_USER = "EXPLICIT_USER"
    CONFIRMED_INFERENCE = "CONFIRMED_INFERENCE"
    INFERRED_CANDIDATE = "INFERRED_CANDIDATE"
    MIGRATED_CONFIRMED = "MIGRATED_CONFIRMED"


class ImpactClass(str, Enum):
    PRESENTATION = "PRESENTATION"
    WORKFLOW_CONVENIENCE = "WORKFLOW_CONVENIENCE"
    EXECUTION_SENSITIVE = "EXECUTION_SENSITIVE"


class ResolutionStatus(str, Enum):
    RESOLVED = "RESOLVED"
    DEFAULT = "DEFAULT"
    FROZEN = "FROZEN"


class PreferenceError(ValueError):
    """Base error for deterministic preference-contract violations."""


class RegistryError(PreferenceError):
    pass


class ValidationError(PreferenceError):
    pass


class TransitionError(PreferenceError):
    pass


@dataclass(frozen=True, slots=True)
class PreferenceScope:
    kind: ScopeKind
    scope_id: str

    def __post_init__(self) -> None:
        if not self.scope_id or not self.scope_id.strip():
            raise ValidationError("scope_id must be non-empty")
        if self.scope_id != self.scope_id.strip():
            raise ValidationError("scope_id must not contain surrounding whitespace")

    @property
    def specificity(self) -> int:
        return SCOPE_SPECIFICITY[self.kind]


@dataclass(frozen=True, slots=True)
class ResolutionContext:
    user_scope_id: str
    project_id: str | None = None
    session_id: str | None = None
    task_id: str | None = None

    def __post_init__(self) -> None:
        if not self.user_scope_id or not self.user_scope_id.strip():
            raise ValidationError("user_scope_id must be non-empty")

    def matches(self, scope: PreferenceScope) -> bool:
        expected = {
            ScopeKind.USER: self.user_scope_id,
            ScopeKind.PROJECT: self.project_id,
            ScopeKind.SESSION: self.session_id,
            ScopeKind.TASK: self.task_id,
        }[scope.kind]
        return expected is not None and expected == scope.scope_id

    def to_payload(self) -> dict[str, str | None]:
        return {
            "user_scope_id": self.user_scope_id,
            "project_id": self.project_id,
            "session_id": self.session_id,
            "task_id": self.task_id,
        }


def require_aware(value: datetime, field_name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValidationError(f"{field_name} must be timezone-aware")
    return value


def canonical_timestamp(value: datetime) -> str:
    require_aware(value, "datetime")
    normalized = value.astimezone(timezone.utc)
    return normalized.isoformat(timespec="microseconds").replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class PreferenceDefinition:
    key: str
    allowed_values: tuple[JsonScalar, ...]
    default: JsonScalar
    impact: ImpactClass
    allowed_scopes: frozenset[ScopeKind]
    requires_expiry: bool = False
    max_ttl_seconds: int | None = None
    requires_consent_receipt: bool = False
    description: str = ""

    def __post_init__(self) -> None:
        if not self.key:
            raise RegistryError("preference key must be non-empty")
        if not self.allowed_values:
            raise RegistryError(f"{self.key}: allowed_values must be non-empty")
        if not self.allowed_scopes:
            raise RegistryError(f"{self.key}: allowed_scopes must be non-empty")
        if not _typed_contains(self.allowed_values, self.default):
            raise RegistryError(f"{self.key}: default must be one of allowed_values")
        if self.max_ttl_seconds is not None and self.max_ttl_seconds <= 0:
            raise RegistryError(f"{self.key}: max_ttl_seconds must be positive")
        if self.requires_expiry and self.max_ttl_seconds is None:
            raise RegistryError(f"{self.key}: requires_expiry requires max_ttl_seconds")

    def accepts(self, value: JsonScalar) -> bool:
        return _typed_contains(self.allowed_values, value)


def _typed_contains(options: tuple[JsonScalar, ...], value: JsonScalar) -> bool:
    return any(type(option) is type(value) and option == value for option in options)


@dataclass(frozen=True, slots=True)
class PreferenceRecord:
    record_id: str
    preference_id: str
    revision: int
    key: str
    value: JsonScalar
    provenance: Provenance
    state: PreferenceState
    scope: PreferenceScope
    created_at: datetime
    expires_at: datetime | None
    source_event_id: str
    consent_receipt_id: str | None = None
    supersedes_record_id: str | None = None

    def __post_init__(self) -> None:
        if not self.record_id or not self.preference_id:
            raise ValidationError("record_id and preference_id are required")
        if self.revision < 1:
            raise ValidationError("revision must be >= 1")
        if not self.source_event_id or not self.source_event_id.strip():
            raise ValidationError("source_event_id must be non-empty")
        require_aware(self.created_at, "created_at")
        if self.expires_at is not None:
            require_aware(self.expires_at, "expires_at")
            if (
                self.state in {PreferenceState.CANDIDATE, PreferenceState.ACTIVE}
                and self.expires_at <= self.created_at
            ):
                raise ValidationError(
                    "expires_at must be later than created_at for candidate/active records"
                )

    def is_expired(self, now: datetime) -> bool:
        require_aware(now, "now")
        return self.expires_at is not None and now >= self.expires_at

    def to_payload(self, *, include_record_id: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "preference_id": self.preference_id,
            "revision": self.revision,
            "key": self.key,
            "value": self.value,
            "provenance": self.provenance.value,
            "state": self.state.value,
            "scope": {"kind": self.scope.kind.value, "scope_id": self.scope.scope_id},
            "created_at": canonical_timestamp(self.created_at),
            "expires_at": canonical_timestamp(self.expires_at) if self.expires_at else None,
            "source_event_id": self.source_event_id,
            "consent_receipt_id": self.consent_receipt_id,
            "supersedes_record_id": self.supersedes_record_id,
        }
        if include_record_id:
            payload["record_id"] = self.record_id
        return payload


@dataclass(frozen=True, slots=True)
class Resolution:
    key: str
    status: ResolutionStatus
    value: JsonScalar | None
    reason: str
    source_record_ids: tuple[str, ...]
    specificity: int | None = None

    def to_payload(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "status": self.status.value,
            "value": self.value,
            "reason": self.reason,
            "source_record_ids": list(self.source_record_ids),
            "specificity": self.specificity,
        }
