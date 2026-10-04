from __future__ import annotations

from dataclasses import dataclass
import hmac
from hashlib import sha256
from typing import Any, Iterable

from .common import Verdict, allow, canonical_json, digest, freeze


@dataclass(frozen=True)
class ApprovalSeal:
    authority_id: str
    plan_hash: str
    allowed_scope: tuple[str, ...]
    expires_at: int
    directive_epoch: int
    max_mutations: int
    signature: str

    def unsigned_dict(self) -> dict[str, Any]:
        return {
            "allowed_scope": list(self.allowed_scope),
            "authority_id": self.authority_id,
            "directive_epoch": self.directive_epoch,
            "expires_at": self.expires_at,
            "max_mutations": self.max_mutations,
            "plan_hash": self.plan_hash,
        }


def _sign(payload: dict[str, Any], key: bytes) -> str:
    return hmac.new(key, canonical_json(payload), sha256).hexdigest()


def issue_seal(
    plan: dict[str, Any],
    *,
    authority_id: str,
    allowed_scope: Iterable[str],
    expires_at: int,
    directive_epoch: int,
    max_mutations: int,
    key: bytes,
) -> ApprovalSeal:
    if not authority_id:
        raise ValueError("authority_id required")
    if expires_at < 0 or directive_epoch < 0 or max_mutations < 0:
        raise ValueError("numeric fields must be non-negative")
    scope = tuple(sorted(set(allowed_scope)))
    payload = {
        "allowed_scope": list(scope),
        "authority_id": authority_id,
        "directive_epoch": directive_epoch,
        "expires_at": expires_at,
        "max_mutations": max_mutations,
        "plan_hash": digest(plan),
    }
    return ApprovalSeal(signature=_sign(payload, key), **payload)


def verify_seal(
    plan: dict[str, Any],
    seal: ApprovalSeal,
    *,
    requested_scope: Iterable[str],
    mutation_count: int,
    now: int,
    current_directive_epoch: int,
    key: bytes,
) -> Verdict:
    reasons: list[str] = []
    if not hmac.compare_digest(seal.signature, _sign(seal.unsigned_dict(), key)):
        reasons.append("SEAL_SIGNATURE_INVALID")
    if digest(plan) != seal.plan_hash:
        reasons.append("PLAN_HASH_MISMATCH")
    if now > seal.expires_at:
        reasons.append("APPROVAL_EXPIRED")
    if current_directive_epoch != seal.directive_epoch:
        reasons.append("DIRECTIVE_EPOCH_MISMATCH")
    if mutation_count < 0 or mutation_count > seal.max_mutations:
        reasons.append("MUTATION_BUDGET_EXCEEDED")
    requested = set(requested_scope)
    allowed_scope = set(seal.allowed_scope)
    if not requested.issubset(allowed_scope):
        reasons.append("SCOPE_ESCALATION")
    if reasons:
        return freeze(*reasons, payload={"plan_hash": digest(plan)})
    return allow({
        "authority_id": seal.authority_id,
        "directive_epoch": seal.directive_epoch,
        "plan_hash": seal.plan_hash,
        "scope": sorted(requested),
    })
