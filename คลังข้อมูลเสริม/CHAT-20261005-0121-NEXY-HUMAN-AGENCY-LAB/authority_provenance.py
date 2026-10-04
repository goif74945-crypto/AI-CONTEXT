from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
from hashlib import sha256
import json
from typing import Any

from human_agency_lab import AgencyDecisionEngine, AgencyPolicy, InteractionDecision, RequestProfile


class AuthorityVerdict(str, Enum):
    VALID = "VALID"
    MISSING = "MISSING"
    REVOKED = "REVOKED"
    NOT_YET_VALID = "NOT_YET_VALID"
    STALE = "STALE"
    ACTION_OUT_OF_SCOPE = "ACTION_OUT_OF_SCOPE"
    SCOPE_LIMIT_EXCEEDED = "SCOPE_LIMIT_EXCEEDED"
    DESTRUCTIVE_NOT_ALLOWED = "DESTRUCTIVE_NOT_ALLOWED"
    EXTERNAL_EFFECT_NOT_ALLOWED = "EXTERNAL_EFFECT_NOT_ALLOWED"
    AUTH_BOUNDARY_NOT_ALLOWED = "AUTH_BOUNDARY_NOT_ALLOWED"


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical_json(value)).hexdigest()


@dataclass(frozen=True)
class AuthorityRef:
    authority_id: str
    issuer: str
    action_prefixes: tuple[str, ...]
    max_scope_breadth: float = 1.0
    allow_destructive: bool = False
    allow_external_effect: bool = False
    allow_auth_boundary: bool = False
    valid_from_revision: int = 0
    valid_through_revision: int | None = None
    revoked: bool = False

    def __post_init__(self) -> None:
        if not self.authority_id.strip():
            raise ValueError("authority_id must be non-empty")
        if not self.issuer.strip():
            raise ValueError("issuer must be non-empty")
        if not self.action_prefixes:
            raise ValueError("action_prefixes must be non-empty")
        if any(not prefix.strip() for prefix in self.action_prefixes):
            raise ValueError("action prefixes must be non-empty")
        if not 0.0 <= self.max_scope_breadth <= 1.0:
            raise ValueError("max_scope_breadth must be within [0, 1]")
        if self.valid_from_revision < 0:
            raise ValueError("valid_from_revision must be >= 0")
        if self.valid_through_revision is not None:
            if self.valid_through_revision < self.valid_from_revision:
                raise ValueError(
                    "valid_through_revision must be >= valid_from_revision"
                )

    def canonical_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["action_prefixes"] = sorted(set(self.action_prefixes))
        return data

    def digest(self) -> str:
        return _digest(self.canonical_dict())


@dataclass(frozen=True)
class PolicyEnvelope:
    policy_id: str
    policy_version: str
    schema_version: str
    policy: AgencyPolicy

    def __post_init__(self) -> None:
        for name in ("policy_id", "policy_version", "schema_version"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "policy": asdict(self.policy),
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "schema_version": self.schema_version,
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


@dataclass(frozen=True)
class AuthorityAssessment:
    verdict: AuthorityVerdict
    authority_digest: str | None
    revision: int

    @property
    def valid(self) -> bool:
        return self.verdict is AuthorityVerdict.VALID


@dataclass(frozen=True)
class GovernedDecision:
    decision: InteractionDecision
    authority: AuthorityAssessment
    policy_digest: str
    request_digest: str

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": {
                "authority_digest": self.authority.authority_digest,
                "revision": self.authority.revision,
                "verdict": self.authority.verdict.value,
            },
            "decision": self.decision.canonical_dict(),
            "policy_digest": self.policy_digest,
            "request_digest": self.request_digest,
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


def request_digest(request: RequestProfile) -> str:
    return _digest(request.canonical_dict())


def assess_authority(
    authority: AuthorityRef | None,
    request: RequestProfile,
    *,
    revision: int,
) -> AuthorityAssessment:
    if revision < 0:
        raise ValueError("revision must be >= 0")
    if authority is None:
        return AuthorityAssessment(AuthorityVerdict.MISSING, None, revision)

    digest = authority.digest()
    if authority.revoked:
        return AuthorityAssessment(AuthorityVerdict.REVOKED, digest, revision)
    if revision < authority.valid_from_revision:
        return AuthorityAssessment(AuthorityVerdict.NOT_YET_VALID, digest, revision)
    if (
        authority.valid_through_revision is not None
        and revision > authority.valid_through_revision
    ):
        return AuthorityAssessment(AuthorityVerdict.STALE, digest, revision)
    if not any(request.action_id.startswith(prefix) for prefix in authority.action_prefixes):
        return AuthorityAssessment(
            AuthorityVerdict.ACTION_OUT_OF_SCOPE, digest, revision
        )
    if request.scope_breadth > authority.max_scope_breadth:
        return AuthorityAssessment(
            AuthorityVerdict.SCOPE_LIMIT_EXCEEDED, digest, revision
        )
    if request.destructive and not authority.allow_destructive:
        return AuthorityAssessment(
            AuthorityVerdict.DESTRUCTIVE_NOT_ALLOWED, digest, revision
        )
    if request.external_side_effect and not authority.allow_external_effect:
        return AuthorityAssessment(
            AuthorityVerdict.EXTERNAL_EFFECT_NOT_ALLOWED, digest, revision
        )
    if request.crosses_auth_boundary and not authority.allow_auth_boundary:
        return AuthorityAssessment(
            AuthorityVerdict.AUTH_BOUNDARY_NOT_ALLOWED, digest, revision
        )
    return AuthorityAssessment(AuthorityVerdict.VALID, digest, revision)


def evaluate_governed(
    request: RequestProfile,
    *,
    authority: AuthorityRef | None,
    revision: int,
    policy: PolicyEnvelope,
) -> GovernedDecision:
    assessment = assess_authority(authority, request, revision=revision)
    normalized = replace(request, explicit_user_authority=assessment.valid)
    engine = AgencyDecisionEngine(policy.policy)
    interaction = engine.evaluate(normalized)
    return GovernedDecision(
        decision=interaction,
        authority=assessment,
        policy_digest=policy.digest(),
        request_digest=request_digest(normalized),
    )
