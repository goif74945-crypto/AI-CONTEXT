from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from types import MappingProxyType
from typing import Any, Iterable, Mapping
import unicodedata

from .canonical import sha256_canonical


def _validate_identity(name: str, value: str, *, max_length: int = 256) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be non-empty and have no surrounding whitespace")
    if len(value) > max_length:
        raise ValueError(f"{name} exceeds {max_length} characters")
    if unicodedata.normalize("NFKC", value) != value:
        raise ValueError(f"{name} must already be NFKC-normalized")
    if any(unicodedata.category(ch).startswith("C") for ch in value):
        raise ValueError(f"{name} contains a control/format character")


def _validate_identity_set(name: str, values: Iterable[str]) -> None:
    for value in values:
        _validate_identity(name, value)


class Sensitivity(IntEnum):
    PUBLIC = 0
    INTERNAL = 1
    CONFIDENTIAL = 2
    PRIVATE = 3
    SECRET = 4
    RESTRICTED = 5


class ReleaseStatus(str, Enum):
    RELEASED = "RELEASED"
    FROZEN = "FROZEN"


@dataclass(frozen=True, slots=True)
class ContextField:
    key: str
    value: Any
    sensitivity: Sensitivity
    provenance: str
    compartments: frozenset[str] = field(default_factory=frozenset)
    allowed_purposes: frozenset[str] = field(default_factory=frozenset)
    derived_from: tuple[str, ...] = ()
    expires_at: str | None = None

    def __post_init__(self) -> None:
        _validate_identity("context field key", self.key)
        _validate_identity("context provenance", self.provenance, max_length=1024)
        if not isinstance(self.sensitivity, Sensitivity):
            raise ValueError("context sensitivity must be a Sensitivity")
        _validate_identity_set("context compartment", self.compartments)
        _validate_identity_set("context allowed purpose", self.allowed_purposes)
        _validate_identity_set("derived_from key", self.derived_from)

    def metadata(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "sensitivity": self.sensitivity.name,
            "provenance": self.provenance,
            "compartments": sorted(self.compartments),
            "allowed_purposes": sorted(self.allowed_purposes),
            "derived_from": list(self.derived_from),
            "expires_at": self.expires_at,
        }


@dataclass(frozen=True, slots=True)
class ContextSet:
    fields: Mapping[str, ContextField]

    def __post_init__(self) -> None:
        copied = dict(self.fields)
        for key, item in copied.items():
            if key != item.key:
                raise ValueError(f"context map key {key!r} does not match field key {item.key!r}")
        object.__setattr__(self, "fields", MappingProxyType(copied))


@dataclass(frozen=True, slots=True)
class ReleaseRequest:
    request_id: str
    consumer_id: str
    purpose: str
    required_keys: tuple[str, ...]
    optional_keys: tuple[str, ...] = ()
    allowed_compartments: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _validate_identity("request_id", self.request_id)
        _validate_identity("consumer_id", self.consumer_id)
        _validate_identity("purpose", self.purpose)
        all_keys = list(self.required_keys) + list(self.optional_keys)
        _validate_identity_set("requested context key", all_keys)
        _validate_identity_set("request compartment", self.allowed_compartments)
        if len(set(all_keys)) != len(all_keys):
            raise ValueError("requested context keys must be unique across required/optional sets")

    def canonical_contract(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "consumer_id": self.consumer_id,
            "purpose": self.purpose,
            "required_keys": sorted(self.required_keys),
            "optional_keys": sorted(self.optional_keys),
            "allowed_compartments": sorted(self.allowed_compartments),
        }


@dataclass(frozen=True, slots=True)
class ReleasePolicy:
    policy_id: str
    consumer_id: str
    allowed_purposes: frozenset[str]
    max_sensitivity: Sensitivity
    allowed_compartments: frozenset[str]
    allow_declassification: bool = False

    def __post_init__(self) -> None:
        _validate_identity("policy_id", self.policy_id)
        _validate_identity("policy consumer_id", self.consumer_id)
        if not isinstance(self.max_sensitivity, Sensitivity):
            raise ValueError("policy max_sensitivity must be a Sensitivity")
        if not self.allowed_purposes:
            raise ValueError("policy must permit at least one explicit purpose")
        _validate_identity_set("policy allowed purpose", self.allowed_purposes)
        _validate_identity_set("policy compartment", self.allowed_compartments)

    def canonical_contract(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "consumer_id": self.consumer_id,
            "allowed_purposes": sorted(self.allowed_purposes),
            "max_sensitivity": self.max_sensitivity.name,
            "allowed_compartments": sorted(self.allowed_compartments),
            "allow_declassification": self.allow_declassification,
        }


@dataclass(frozen=True, slots=True)
class DeclassificationGrant:
    grant_id: str
    field_key: str
    from_sensitivity: Sensitivity
    to_sensitivity: Sensitivity
    authority_id: str
    consumer_id: str
    purpose: str
    not_before: str
    not_after: str
    reason_code: str

    def __post_init__(self) -> None:
        if not isinstance(self.from_sensitivity, Sensitivity) or not isinstance(self.to_sensitivity, Sensitivity):
            raise ValueError("grant sensitivities must be Sensitivity values")
        if self.to_sensitivity >= self.from_sensitivity:
            raise ValueError("declassification must lower sensitivity")
        for name in ("grant_id", "field_key", "authority_id", "consumer_id", "purpose", "not_before", "not_after", "reason_code"):
            _validate_identity(name, getattr(self, name), max_length=1024 if name in {"not_before", "not_after"} else 256)

    def canonical_contract(self) -> dict[str, Any]:
        return {
            "grant_id": self.grant_id,
            "field_key": self.field_key,
            "from_sensitivity": self.from_sensitivity.name,
            "to_sensitivity": self.to_sensitivity.name,
            "authority_id": self.authority_id,
            "consumer_id": self.consumer_id,
            "purpose": self.purpose,
            "not_before": self.not_before,
            "not_after": self.not_after,
            "reason_code": self.reason_code,
        }

    def digest(self) -> str:
        return sha256_canonical(self.canonical_contract())


@dataclass(frozen=True, slots=True)
class FieldDecision:
    key: str
    required: bool
    decision: str
    reason_code: str
    effective_sensitivity: str | None
    declassification_grant_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "required": self.required,
            "decision": self.decision,
            "reason_code": self.reason_code,
            "effective_sensitivity": self.effective_sensitivity,
            "declassification_grant_id": self.declassification_grant_id,
        }


@dataclass(frozen=True, slots=True)
class ReleaseReceipt:
    request_id: str
    consumer_id: str
    purpose: str
    status: ReleaseStatus
    request_hash: str
    policy_hash: str
    context_metadata_hash: str
    payload_hash: str | None
    decisions: tuple[FieldDecision, ...]
    evaluated_at: str
    engine_version: str
    receipt_hash: str

    def public_dict(self, include_receipt_hash: bool = True) -> dict[str, Any]:
        result = {
            "request_id": self.request_id,
            "consumer_id": self.consumer_id,
            "purpose": self.purpose,
            "status": self.status.value,
            "request_hash": self.request_hash,
            "policy_hash": self.policy_hash,
            "context_metadata_hash": self.context_metadata_hash,
            "payload_hash": self.payload_hash,
            "decisions": [decision.to_dict() for decision in self.decisions],
            "evaluated_at": self.evaluated_at,
            "engine_version": self.engine_version,
        }
        if include_receipt_hash:
            result["receipt_hash"] = self.receipt_hash
        return result


@dataclass(frozen=True, slots=True)
class ReleaseResult:
    status: ReleaseStatus
    payload: Mapping[str, Any]
    receipt: ReleaseReceipt

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
