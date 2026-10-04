"""Value-free deterministic receipt construction."""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Iterable, Mapping

from .model import Action, EgressRequest, FirewallPolicy
from .utils import sha256_json


@dataclass(frozen=True)
class EgressReceipt:
    request_id: str
    purpose: str
    recipient: str
    recipient_class: str
    action: str
    included_item_ids: tuple[str, ...]
    redacted_item_ids: tuple[str, ...]
    blocked_item_ids: tuple[str, ...]
    consent_required_item_ids: tuple[str, ...]
    field_redactions: Mapping[str, tuple[str, ...]]
    reason_codes: tuple[str, ...]
    policy_fingerprint: str
    digest: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "purpose": self.purpose,
            "recipient": self.recipient,
            "recipient_class": self.recipient_class,
            "action": self.action,
            "included_item_ids": list(self.included_item_ids),
            "redacted_item_ids": list(self.redacted_item_ids),
            "blocked_item_ids": list(self.blocked_item_ids),
            "consent_required_item_ids": list(self.consent_required_item_ids),
            "field_redactions": {k: list(v) for k, v in sorted(self.field_redactions.items())},
            "reason_codes": list(self.reason_codes),
            "policy_fingerprint": self.policy_fingerprint,
            "digest": self.digest,
        }


def policy_fingerprint(policy: FirewallPolicy) -> str:
    return sha256_json({
        "external_sensitive_requires_consent": policy.external_sensitive_requires_consent,
        "forbid_secret_external_egress": policy.forbid_secret_external_egress,
        "sensitive_requires_explicit_recipient_binding": policy.sensitive_requires_explicit_recipient_binding,
    })


def make_receipt(
    *,
    req: EgressRequest,
    policy: FirewallPolicy,
    action: Action,
    included: Iterable[str] = (),
    redacted: Iterable[str] = (),
    blocked: Iterable[str] = (),
    consent_required: Iterable[str] = (),
    field_redactions: Mapping[str, tuple[str, ...]] | None = None,
    reasons: Iterable[str] = (),
) -> EgressReceipt:
    receipt = EgressReceipt(
        request_id=req.request_id if isinstance(req.request_id, str) else "",
        purpose=req.purpose if isinstance(req.purpose, str) else "",
        recipient=req.recipient if isinstance(req.recipient, str) else "",
        recipient_class=req.recipient_class.value if hasattr(req.recipient_class, "value") else "INVALID",
        action=action.value,
        included_item_ids=tuple(sorted(set(included))),
        redacted_item_ids=tuple(sorted(set(redacted))),
        blocked_item_ids=tuple(sorted(set(blocked))),
        consent_required_item_ids=tuple(sorted(set(consent_required))),
        field_redactions={k: tuple(sorted(v)) for k, v in sorted((field_redactions or {}).items())},
        reason_codes=tuple(sorted(set(reasons))),
        policy_fingerprint=policy_fingerprint(policy),
    )
    raw = receipt.to_dict()
    raw["digest"] = ""
    return replace(receipt, digest=sha256_json(raw))
