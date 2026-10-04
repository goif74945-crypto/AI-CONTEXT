from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Optional, Tuple


class StrEnum(str, Enum):
    """String enum with stable JSON representation."""


class SystemState(StrEnum):
    INIT = "INIT"
    READY = "READY"
    RUNNING = "RUNNING"
    VERIFYING = "VERIFYING"
    CONSENSUS = "CONSENSUS"
    STABLE = "STABLE"
    FREEZE = "FREEZE"
    STOP = "STOP"


class Role(StrEnum):
    OWNER = "OWNER"
    OPERATOR = "OPERATOR"
    AUDITOR = "AUDITOR"
    SYSTEM = "SYSTEM"
    PUBLIC_USER = "PUBLIC_USER"


class EvidenceStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    BLOCKED = "BLOCKED"
    NOT_VERIFIED = "NOT_VERIFIED"
    UNKNOWN = "UNKNOWN"
    CONFLICT = "CONFLICT"


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class DetailLevel(StrEnum):
    COMPACT = "COMPACT"
    STANDARD = "STANDARD"
    FORENSIC = "FORENSIC"


class Action(StrEnum):
    VIEW_RESULT = "VIEW_RESULT"
    OPEN_TRACE = "OPEN_TRACE"
    SUBMIT_DIRECTIVE = "SUBMIT_DIRECTIVE"
    RECOVER_FREEZE = "RECOVER_FREEZE"
    EXPORT_ARTIFACT = "EXPORT_ARTIFACT"
    EXPORT_AUDIT = "EXPORT_AUDIT"
    CONFIG_CHANGE = "CONFIG_CHANGE"
    HARD_DELETE = "HARD_DELETE"


class Confirmation(StrEnum):
    NONE = "NONE"
    CONFIRM = "CONFIRM"
    TYPE_TO_CONFIRM = "TYPE_TO_CONFIRM"


class TrustLabel(StrEnum):
    INITIALIZING = "INITIALIZING"
    READY_UNRELEASED = "READY_UNRELEASED"
    IN_PROGRESS = "IN_PROGRESS"
    VERIFIED_FINAL = "VERIFIED_FINAL"
    UNVERIFIED = "UNVERIFIED"
    REJECTED = "REJECTED"
    FROZEN = "FROZEN"
    STOPPED = "STOPPED"
    CONTRACT_CONFLICT = "CONTRACT_CONFLICT"


@dataclass(frozen=True, slots=True)
class SurfaceInput:
    system_state: SystemState
    role: Role
    evidence_status: EvidenceStatus
    requested_action: Action
    risk: RiskLevel
    preferred_detail: DetailLevel
    backend_authorized: bool
    release_authorized: bool
    recoverable: bool
    irreversible: bool = False
    incident_code: Optional[str] = None
    blocking_layer: Optional[str] = None
    backend_reason_code: Optional[str] = None

    def to_primitive(self) -> dict:
        raw = asdict(self)
        for key, value in tuple(raw.items()):
            if isinstance(value, Enum):
                raw[key] = value.value
        return raw


@dataclass(frozen=True, slots=True)
class ActionDecision:
    action: Action
    enabled: bool
    reason_code: str
    confirmation: Confirmation

    def to_primitive(self) -> dict:
        return {
            "action": self.action.value,
            "enabled": self.enabled,
            "reason_code": self.reason_code,
            "confirmation": self.confirmation.value,
        }


@dataclass(frozen=True, slots=True)
class SurfacePlan:
    schema_version: str
    trust_label: TrustLabel
    detail_level: DetailLevel
    banner: Optional[str]
    action: ActionDecision
    mandatory_disclosures: Tuple[str, ...]
    optional_sections: Tuple[str, ...]
    conflict_codes: Tuple[str, ...]
    reasons: Tuple[str, ...]
    fingerprint: str

    def to_primitive(self, *, include_fingerprint: bool = True) -> dict:
        result = {
            "schema_version": self.schema_version,
            "trust_label": self.trust_label.value,
            "detail_level": self.detail_level.value,
            "banner": self.banner,
            "action": self.action.to_primitive(),
            "mandatory_disclosures": list(self.mandatory_disclosures),
            "optional_sections": list(self.optional_sections),
            "conflict_codes": list(self.conflict_codes),
            "reasons": list(self.reasons),
        }
        if include_fingerprint:
            result["fingerprint"] = self.fingerprint
        return result
