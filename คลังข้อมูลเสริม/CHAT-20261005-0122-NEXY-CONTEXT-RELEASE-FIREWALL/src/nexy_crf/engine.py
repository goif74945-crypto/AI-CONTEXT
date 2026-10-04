from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from .canonical import CanonicalizationError, sha256_canonical
from .model import (
    ContextField,
    ContextSet,
    DeclassificationGrant,
    FieldDecision,
    ReleasePolicy,
    ReleaseReceipt,
    ReleaseRequest,
    ReleaseResult,
    ReleaseStatus,
    Sensitivity,
)


ENGINE_VERSION = "0.1.0-reference"


class ContextValidationError(ValueError):
    pass


class PolicyValidationError(ValueError):
    pass


def _parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"invalid ISO-8601 timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must include timezone: {value!r}")
    return parsed.astimezone(timezone.utc)


def _max_sensitivity(values: Iterable[Sensitivity]) -> Sensitivity:
    return max(values, default=Sensitivity.PUBLIC)


class ContextReleaseFirewall:
    """Deterministic reference engine for purpose-bound least-context release.

    This module is intentionally model-free. It does not infer intent, infer
    purpose, or auto-declassify content. All authority-bearing inputs are
    explicit data supplied by the caller.
    """

    def __init__(self, trusted_grant_digests: Mapping[str, str] | None = None) -> None:
        self._trusted_grants = dict(trusted_grant_digests or {})

    def validate_context(self, context: ContextSet) -> None:
        # Canonicalizability is checked up front so a release cannot fail after
        # policy decisions have already been made.
        for field in context.fields.values():
            if not field.key:
                raise ContextValidationError("context field key must be non-empty")
            if not field.provenance:
                raise ContextValidationError(f"field {field.key!r} lacks provenance")
            try:
                sha256_canonical(field.value)
            except CanonicalizationError as exc:
                raise ContextValidationError(f"field {field.key!r} has non-canonical value: {exc}") from exc
            if field.expires_at is not None:
                _parse_time(field.expires_at)

        visiting: set[str] = set()
        visited: set[str] = set()

        def walk(key: str) -> tuple[Sensitivity, frozenset[str], frozenset[str] | None]:
            if key in visited:
                field = context.fields[key]
                return field.sensitivity, field.compartments, field.allowed_purposes or None
            if key in visiting:
                raise ContextValidationError(f"derived context cycle detected at {key!r}")
            field = context.fields.get(key)
            if field is None:
                raise ContextValidationError(f"derived context references unknown field {key!r}")
            visiting.add(key)

            if not field.derived_from:
                effective_purposes = field.allowed_purposes or None
            else:
                source_meta = [walk(source_key) for source_key in field.derived_from]
                required_sensitivity = _max_sensitivity(item[0] for item in source_meta)
                required_compartments = frozenset().union(*(item[1] for item in source_meta))
                restricted_sets = [item[2] for item in source_meta if item[2] is not None]
                inherited_purposes = (
                    frozenset.intersection(*restricted_sets) if restricted_sets else None
                )

                if field.sensitivity < required_sensitivity:
                    raise ContextValidationError(
                        f"derived field {field.key!r} understates sensitivity: "
                        f"declared={field.sensitivity.name} required>={required_sensitivity.name}"
                    )
                if not required_compartments.issubset(field.compartments):
                    raise ContextValidationError(
                        f"derived field {field.key!r} narrows required compartments"
                    )
                if inherited_purposes is not None:
                    if not field.allowed_purposes:
                        raise ContextValidationError(
                            f"derived field {field.key!r} removes inherited purpose restriction"
                        )
                    if not field.allowed_purposes.issubset(inherited_purposes):
                        raise ContextValidationError(
                            f"derived field {field.key!r} broadens inherited purpose restriction"
                        )
                effective_purposes = field.allowed_purposes or inherited_purposes

            visiting.remove(key)
            visited.add(key)
            return field.sensitivity, field.compartments, effective_purposes

        for key in sorted(context.fields):
            walk(key)

    def validate_policy(self, request: ReleaseRequest, policy: ReleasePolicy) -> None:
        if request.consumer_id != policy.consumer_id:
            raise PolicyValidationError("request consumer does not match policy consumer")
        if request.purpose not in policy.allowed_purposes:
            raise PolicyValidationError("request purpose is not permitted by policy")
        if not request.allowed_compartments.issubset(policy.allowed_compartments):
            raise PolicyValidationError("request asks for compartments outside policy")

    def _context_metadata_hash(self, context: ContextSet, requested_keys: Iterable[str]) -> str:
        # Values are deliberately excluded, and unrequested fields are excluded
        # too. The receipt should not become a correlation oracle for unrelated
        # context merely because that context happened to exist beside the task.
        metadata = [
            context.fields[key].metadata()
            for key in sorted(set(requested_keys))
            if key in context.fields
        ]
        return sha256_canonical(metadata)

    def _matching_grant(
        self,
        field: ContextField,
        request: ReleaseRequest,
        policy: ReleasePolicy,
        grants: Iterable[DeclassificationGrant],
        evaluated_at: datetime,
    ) -> DeclassificationGrant | None:
        if not policy.allow_declassification:
            return None
        for grant in sorted(grants, key=lambda item: item.grant_id):
            if grant.field_key != field.key:
                continue
            if grant.consumer_id != request.consumer_id or grant.purpose != request.purpose:
                continue
            if grant.from_sensitivity != field.sensitivity:
                continue
            if grant.to_sensitivity > policy.max_sensitivity:
                continue
            trusted_digest = self._trusted_grants.get(grant.grant_id)
            if trusted_digest is None or trusted_digest != grant.digest():
                continue
            if not (_parse_time(grant.not_before) <= evaluated_at < _parse_time(grant.not_after)):
                continue
            return grant
        return None

    def release(
        self,
        context: ContextSet,
        request: ReleaseRequest,
        policy: ReleasePolicy,
        *,
        evaluated_at: str,
        declassification_grants: Iterable[DeclassificationGrant] = (),
    ) -> ReleaseResult:
        self.validate_context(context)
        self.validate_policy(request, policy)
        now = _parse_time(evaluated_at)

        required = set(request.required_keys)
        requested_order = tuple(sorted(required)) + tuple(sorted(request.optional_keys))
        decisions: list[FieldDecision] = []
        tentative_payload: dict[str, Any] = {}
        required_blocked = False

        for key in requested_order:
            is_required = key in required
            field = context.fields.get(key)
            if field is None:
                reason = "MISSING_REQUIRED" if is_required else "MISSING_OPTIONAL"
                decisions.append(FieldDecision(key, is_required, "BLOCK", reason, None))
                required_blocked = required_blocked or is_required
                continue

            if field.expires_at is not None and now >= _parse_time(field.expires_at):
                decisions.append(FieldDecision(key, is_required, "BLOCK", "EXPIRED", field.sensitivity.name))
                required_blocked = required_blocked or is_required
                continue

            if field.allowed_purposes and request.purpose not in field.allowed_purposes:
                decisions.append(FieldDecision(key, is_required, "BLOCK", "PURPOSE_MISMATCH", field.sensitivity.name))
                required_blocked = required_blocked or is_required
                continue

            if not field.compartments.issubset(request.allowed_compartments):
                decisions.append(FieldDecision(key, is_required, "BLOCK", "COMPARTMENT_MISMATCH", field.sensitivity.name))
                required_blocked = required_blocked or is_required
                continue

            effective_sensitivity = field.sensitivity
            grant_id: str | None = None
            if field.sensitivity > policy.max_sensitivity:
                grant = self._matching_grant(
                    field,
                    request,
                    policy,
                    declassification_grants,
                    now,
                )
                if grant is None:
                    decisions.append(FieldDecision(key, is_required, "BLOCK", "SENSITIVITY_EXCEEDS_POLICY", field.sensitivity.name))
                    required_blocked = required_blocked or is_required
                    continue
                effective_sensitivity = grant.to_sensitivity
                grant_id = grant.grant_id

            tentative_payload[key] = field.value
            decisions.append(
                FieldDecision(
                    key,
                    is_required,
                    "ALLOW",
                    "DECLASSIFIED" if grant_id else "POLICY_ALLOW",
                    effective_sensitivity.name,
                    grant_id,
                )
            )

        status = ReleaseStatus.FROZEN if required_blocked else ReleaseStatus.RELEASED
        payload: dict[str, Any] = {} if required_blocked else tentative_payload
        payload_hash = sha256_canonical(payload) if status is ReleaseStatus.RELEASED else None

        request_hash = sha256_canonical(request.canonical_contract())
        policy_hash = sha256_canonical(policy.canonical_contract())
        context_metadata_hash = self._context_metadata_hash(context, requested_order)
        receipt_core = {
            "request_id": request.request_id,
            "consumer_id": request.consumer_id,
            "purpose": request.purpose,
            "status": status.value,
            "request_hash": request_hash,
            "policy_hash": policy_hash,
            "context_metadata_hash": context_metadata_hash,
            "payload_hash": payload_hash,
            "decisions": [decision.to_dict() for decision in decisions],
            "evaluated_at": evaluated_at,
            "engine_version": ENGINE_VERSION,
        }
        receipt_hash = sha256_canonical(receipt_core)
        receipt = ReleaseReceipt(
            request_id=request.request_id,
            consumer_id=request.consumer_id,
            purpose=request.purpose,
            status=status,
            request_hash=request_hash,
            policy_hash=policy_hash,
            context_metadata_hash=context_metadata_hash,
            payload_hash=payload_hash,
            decisions=tuple(decisions),
            evaluated_at=evaluated_at,
            engine_version=ENGINE_VERSION,
            receipt_hash=receipt_hash,
        )
        return ReleaseResult(status=status, payload=payload, receipt=receipt)
