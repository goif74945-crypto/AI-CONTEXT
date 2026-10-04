"""Deterministic purpose-bound context egress evaluator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .model import (
    Action,
    ConsentGrant,
    ConsentMode,
    DataItem,
    EgressRequest,
    FirewallPolicy,
    RecipientClass,
    Sensitivity,
)
from .receipt import EgressReceipt, make_receipt
from .utils import aware_utc, first_duplicate, is_expired, sorted_mapping


@dataclass(frozen=True)
class EvaluationResult:
    action: Action
    payload: Mapping[str, Any]
    receipt: EgressReceipt


class PrivacyFirewall:
    """Pure evaluator: no network, persistence, environment, or subprocess access."""

    def __init__(self, policy: FirewallPolicy | None = None) -> None:
        self.policy = policy or FirewallPolicy()

    def evaluate(self, req: EgressRequest) -> EvaluationResult:
        request_error = self._validate_request(req)
        if request_error:
            return self._terminal(req, Action.FREEZE, (request_error,))
        if not isinstance(req.items, tuple) or any(not isinstance(item, DataItem) for item in req.items):
            return self._terminal(req, Action.FREEZE, ("INVALID_ITEM_METADATA", "INVALID_ITEM_COLLECTION"))
        grant_error = self._validate_grants(req)
        if grant_error:
            return self._terminal(req, Action.FREEZE, ("INVALID_GRANT_METADATA", grant_error))
        if first_duplicate(item.item_id for item in req.items) is not None:
            return self._terminal(req, Action.FREEZE, ("DUPLICATE_ITEM_ID",))
        for item in req.items:
            item_error = self._validate_item(item)
            if item_error:
                return self._terminal(req, Action.FREEZE, ("INVALID_ITEM_METADATA", item_error))

        payload: dict[str, Any] = {}
        included: list[str] = []
        redacted: list[str] = []
        blocked: list[str] = []
        consent_required: list[str] = []
        field_redactions: dict[str, tuple[str, ...]] = {}
        reasons: list[str] = []
        required_ask = required_block = any_redaction = False

        for item in sorted(req.items, key=lambda candidate: candidate.item_id):
            if is_expired(item.expires_at, req.now):
                reasons.append("ITEM_EXPIRED")
                required_block, any_redaction = self._reject(item, blocked, redacted, required_block, any_redaction)
                continue
            if req.purpose not in item.allowed_purposes:
                reasons.append("PURPOSE_MISMATCH")
                required_block, any_redaction = self._reject(item, blocked, redacted, required_block, any_redaction)
                continue
            if req.recipient not in item.allowed_recipients:
                reasons.append("RECIPIENT_MISMATCH")
                required_block, any_redaction = self._reject(item, blocked, redacted, required_block, any_redaction)
                continue
            if self._secret_external_forbidden(item, req):
                reasons.append("SECRET_EXTERNAL_EGRESS_FORBIDDEN")
                required_block, any_redaction = self._reject(item, blocked, redacted, required_block, any_redaction)
                continue
            if self._consent_needed(item, req) and not self._has_valid_consent(item, req):
                reasons.append("CONSENT_REQUIRED")
                if item.required:
                    consent_required.append(item.item_id)
                    required_ask = True
                else:
                    redacted.append(item.item_id)
                    any_redaction = True
                continue

            minimized, removed = self._minimize_fields(item, req.purpose)
            if removed:
                field_redactions[item.item_id] = removed
                reasons.append("FIELD_MINIMIZATION_APPLIED")
                any_redaction = True
            if isinstance(item.value, Mapping) and item.field_purposes and not minimized:
                reasons.append("NO_PURPOSE_NECESSARY_FIELDS")
                required_block, any_redaction = self._reject(item, blocked, redacted, required_block, any_redaction)
                continue
            payload[item.item_id] = minimized
            included.append(item.item_id)

        if required_block:
            return self._result(req, Action.BLOCK, {}, (), redacted, blocked, consent_required, field_redactions, reasons)
        if required_ask:
            return self._result(req, Action.ASK, {}, (), redacted, blocked, consent_required, field_redactions, reasons)
        action = Action.REDACT if any_redaction or redacted else Action.ALLOW
        return self._result(req, action, payload, included, redacted, blocked, consent_required, field_redactions, reasons)

    @staticmethod
    def _reject(
        item: DataItem,
        blocked: list[str],
        redacted: list[str],
        required_block: bool,
        any_redaction: bool,
    ) -> tuple[bool, bool]:
        if item.required:
            blocked.append(item.item_id)
            return True, any_redaction
        redacted.append(item.item_id)
        return required_block, True

    def _secret_external_forbidden(self, item: DataItem, req: EgressRequest) -> bool:
        return (
            self.policy.forbid_secret_external_egress
            and item.sensitivity is Sensitivity.SECRET
            and req.recipient_class is not RecipientClass.LOCAL_TRUSTED
        )

    def _validate_request(self, req: EgressRequest) -> str | None:
        if not isinstance(req.request_id, str) or not req.request_id.strip():
            return "INVALID_REQUEST_ID"
        if not isinstance(req.purpose, str) or not req.purpose.strip():
            return "INVALID_REQUEST_PURPOSE"
        if not isinstance(req.recipient, str) or not req.recipient.strip():
            return "INVALID_REQUEST_RECIPIENT"
        if not isinstance(req.recipient_class, RecipientClass):
            return "INVALID_REQUEST_RECIPIENT_CLASS"
        try:
            aware_utc(req.now)
        except (TypeError, ValueError):
            return "INVALID_REQUEST_TIME"
        return None

    def _validate_grants(self, req: EgressRequest) -> str | None:
        if not isinstance(req.consent_grants, tuple):
            return "INVALID_GRANT_COLLECTION"
        for grant in req.consent_grants:
            if not isinstance(grant, ConsentGrant):
                return "INVALID_GRANT_OBJECT"
            if not all(
                isinstance(value, str) and bool(value.strip())
                for value in (grant.grant_id, grant.item_id, grant.purpose, grant.recipient)
            ):
                return "INVALID_GRANT_BINDING"
            if not isinstance(grant.revoked, bool):
                return "INVALID_GRANT_REVOCATION"
            try:
                aware_utc(grant.expires_at)
            except (TypeError, ValueError):
                return "INVALID_GRANT_EXPIRY"
        return None

    def _validate_item(self, item: DataItem) -> str | None:
        if not isinstance(item.item_id, str) or not item.item_id.strip():
            return "EMPTY_OR_INVALID_ITEM_ID"
        if not isinstance(item.sensitivity, Sensitivity):
            return "INVALID_SENSITIVITY"
        if not isinstance(item.consent_mode, ConsentMode):
            return "INVALID_CONSENT_MODE"
        if not isinstance(item.required, bool):
            return "INVALID_REQUIRED_FLAG"
        if not _valid_string_scope(item.allowed_purposes, allow_empty=False):
            return "EMPTY_OR_INVALID_PURPOSE_SET"
        if not _valid_string_scope(item.allowed_recipients, allow_empty=True):
            return "INVALID_RECIPIENT_SET"
        if (
            self.policy.sensitive_requires_explicit_recipient_binding
            and item.sensitivity >= Sensitivity.SENSITIVE
            and (not item.allowed_recipients or "*" in item.allowed_recipients)
        ):
            return "SENSITIVE_ITEM_WITHOUT_EXPLICIT_RECIPIENT_BINDING"
        if item.expires_at is not None:
            try:
                aware_utc(item.expires_at)
            except (TypeError, ValueError):
                return "INVALID_ITEM_EXPIRY"
        if item.field_purposes:
            if not isinstance(item.field_purposes, Mapping):
                return "INVALID_FIELD_RULES"
            if not isinstance(item.value, Mapping):
                return "FIELD_RULES_REQUIRE_MAPPING_VALUE"
            if set(item.field_purposes) - set(item.value):
                return "FIELD_RULE_REFERENCES_UNKNOWN_FIELD"
            for field_name, purposes in item.field_purposes.items():
                if not isinstance(field_name, str) or not field_name.strip():
                    return "INVALID_FIELD_NAME"
                if not _valid_string_scope(purposes, allow_empty=True):
                    return "INVALID_FIELD_PURPOSE"
        return None

    def _consent_needed(self, item: DataItem, req: EgressRequest) -> bool:
        return item.consent_mode is ConsentMode.EXPLICIT or (
            self.policy.external_sensitive_requires_consent
            and item.sensitivity >= Sensitivity.SENSITIVE
            and req.recipient_class is not RecipientClass.LOCAL_TRUSTED
        )

    @staticmethod
    def _has_valid_consent(item: DataItem, req: EgressRequest) -> bool:
        return any(
            grant.is_valid_for(item_id=item.item_id, purpose=req.purpose, recipient=req.recipient, now=req.now)
            for grant in req.consent_grants
        )

    @staticmethod
    def _minimize_fields(item: DataItem, purpose: str) -> tuple[Any, tuple[str, ...]]:
        if not item.field_purposes or not isinstance(item.value, Mapping):
            return item.value, ()
        allowed: dict[str, Any] = {}
        removed: list[str] = []
        for field_name in sorted(item.value):
            purposes = item.field_purposes.get(field_name)
            if purposes is None or purpose not in purposes:
                removed.append(field_name)
            else:
                allowed[field_name] = item.value[field_name]
        return allowed, tuple(removed)

    def _terminal(self, req: EgressRequest, action: Action, reasons: tuple[str, ...]) -> EvaluationResult:
        return self._result(req, action, {}, (), (), (), (), {}, reasons)

    def _result(
        self,
        req: EgressRequest,
        action: Action,
        payload: Mapping[str, Any],
        included: tuple[str, ...] | list[str],
        redacted: tuple[str, ...] | list[str],
        blocked: tuple[str, ...] | list[str],
        consent_required: tuple[str, ...] | list[str],
        field_redactions: Mapping[str, tuple[str, ...]],
        reasons: tuple[str, ...] | list[str],
    ) -> EvaluationResult:
        receipt = make_receipt(
            req=req,
            policy=self.policy,
            action=action,
            included=included,
            redacted=redacted,
            blocked=blocked,
            consent_required=consent_required,
            field_redactions=field_redactions,
            reasons=reasons,
        )
        return EvaluationResult(action=action, payload=sorted_mapping(payload), receipt=receipt)


def _valid_string_scope(value: object, *, allow_empty: bool) -> bool:
    if not isinstance(value, (set, frozenset)):
        return False
    if not allow_empty and not value:
        return False
    return all(isinstance(entry, str) and bool(entry.strip()) for entry in value)
