"""Data model for the NON-GOVERNING NPCEF reference prototype."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from typing import Any, Mapping

from .utils import aware_utc


class Action(str, Enum):
    ALLOW = "ALLOW"
    REDACT = "REDACT"
    ASK = "ASK"
    BLOCK = "BLOCK"
    FREEZE = "FREEZE"


class Sensitivity(IntEnum):
    PUBLIC = 0
    INTERNAL = 1
    PERSONAL = 2
    SENSITIVE = 3
    SECRET = 4


class ConsentMode(str, Enum):
    NONE = "NONE"
    EXPLICIT = "EXPLICIT"


class RecipientClass(str, Enum):
    LOCAL_TRUSTED = "LOCAL_TRUSTED"
    EXTERNAL_MODEL = "EXTERNAL_MODEL"
    CONNECTOR = "CONNECTOR"
    EXPORT = "EXPORT"


@dataclass(frozen=True)
class RecipientRouteProof:
    """Observed recipient resolution metadata; not an authenticated proof."""

    requested_recipient: str
    resolved_recipient: str
    redirect_chain: tuple[str, ...]
    resolver_version: str


@dataclass(frozen=True)
class ConsentGrant:
    grant_id: str
    item_id: str
    purpose: str
    recipient: str
    expires_at: datetime
    revoked: bool = False

    def is_valid_for(self, *, item_id: str, purpose: str, recipient: str, now: datetime) -> bool:
        return (
            not self.revoked
            and self.grant_id.strip() != ""
            and self.item_id == item_id
            and self.purpose == purpose
            and self.recipient == recipient
            and aware_utc(self.expires_at) > aware_utc(now)
        )


@dataclass(frozen=True)
class ConsentBundleGrant:
    """Exact-request, exact-item-set batch consent for the reference lab."""

    grant_id: str
    request_id: str
    item_ids: frozenset[str]
    purpose: str
    recipient: str
    expires_at: datetime
    revoked: bool = False

    def is_valid_for(
        self,
        *,
        request_id: str,
        item_id: str,
        purpose: str,
        recipient: str,
        now: datetime,
    ) -> bool:
        return (
            not self.revoked
            and self.grant_id.strip() != ""
            and self.request_id == request_id
            and item_id in self.item_ids
            and self.purpose == purpose
            and self.recipient == recipient
            and aware_utc(self.expires_at) > aware_utc(now)
        )


@dataclass(frozen=True)
class DataItem:
    item_id: str
    value: Any
    sensitivity: Sensitivity
    allowed_purposes: frozenset[str]
    allowed_recipients: frozenset[str]
    expires_at: datetime | None = None
    consent_mode: ConsentMode = ConsentMode.NONE
    required: bool = False
    field_purposes: Mapping[str, frozenset[str]] = field(default_factory=dict)


@dataclass(frozen=True)
class EgressRequest:
    request_id: str
    purpose: str
    recipient: str
    recipient_class: RecipientClass
    now: datetime
    items: tuple[DataItem, ...]
    consent_grants: tuple[ConsentGrant | ConsentBundleGrant, ...] = ()
    recipient_route_proof: RecipientRouteProof | None = None


@dataclass(frozen=True)
class FirewallPolicy:
    external_sensitive_requires_consent: bool = True
    forbid_secret_external_egress: bool = True
    sensitive_requires_explicit_recipient_binding: bool = True
    require_external_recipient_route_proof: bool = True
