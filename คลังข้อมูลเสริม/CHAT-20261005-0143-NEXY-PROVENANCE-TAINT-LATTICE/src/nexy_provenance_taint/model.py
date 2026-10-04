from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Mapping, Tuple


class Taint(str, Enum):
    """Sticky risk markers that must not disappear through ordinary transforms."""

    UNKNOWN_ORIGIN = "UNKNOWN_ORIGIN"
    UNVERIFIED = "UNVERIFIED"
    CONFLICT = "CONFLICT"
    EXTERNAL_UNTRUSTED = "EXTERNAL_UNTRUSTED"
    NONDETERMINISTIC = "NONDETERMINISTIC"
    POLICY_MISMATCH = "POLICY_MISMATCH"


PROTECTED_TAINTS: FrozenSet[Taint] = frozenset(
    {
        Taint.UNKNOWN_ORIGIN,
        Taint.CONFLICT,
        Taint.EXTERNAL_UNTRUSTED,
        Taint.POLICY_MISMATCH,
    }
)


@dataclass(frozen=True)
class SourceSpec:
    """Explicit source metadata.

    authority_rank is intentionally policy-defined rather than hard-coded to a NEXY
    authority hierarchy. Higher numeric values mean stronger authority *inside the
    caller's policy domain only*.
    """

    origin_id: str
    source_kind: str
    authority_rank: int
    assurance_tags: FrozenSet[str] = field(default_factory=frozenset)
    taints: FrozenSet[Taint] = field(default_factory=frozenset)
    epoch: int = 0


@dataclass(frozen=True)
class TransformContract:
    contract_id: str
    deterministic: bool = True
    required_assurances: FrozenSet[str] = field(default_factory=frozenset)
    preserved_assurances: FrozenSet[str] = field(default_factory=frozenset)
    introduced_taints: FrozenSet[Taint] = field(default_factory=frozenset)


@dataclass(frozen=True)
class VerificationReceipt:
    receipt_id: str
    verifier_id: str
    artifact_id: str
    added_assurances: FrozenSet[str] = field(default_factory=frozenset)
    cleared_taints: FrozenSet[Taint] = field(default_factory=frozenset)
    issued_epoch: int = 0
    expires_epoch: int | None = None


@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    payload_digest: str
    operation_id: str
    parent_ids: Tuple[str, ...]
    root_origins: Tuple[str, ...]
    authority_floor: int
    assurances: FrozenSet[str]
    taints: FrozenSet[Taint]
    created_epoch: int
    metadata: Tuple[Tuple[str, str], ...] = field(default_factory=tuple)
    applied_receipts: Tuple[str, ...] = field(default_factory=tuple)

    def metadata_map(self) -> Mapping[str, str]:
        return dict(self.metadata)


@dataclass(frozen=True)
class ReleasePolicy:
    policy_id: str
    min_authority_rank: int = 0
    required_assurances: FrozenSet[str] = field(default_factory=frozenset)
    forbidden_taints: FrozenSet[Taint] = field(default_factory=lambda: frozenset(Taint))
    allowed_root_origins: FrozenSet[str] | None = None
    max_age_epochs: int | None = None
    require_deterministic_lineage: bool = True


@dataclass(frozen=True)
class ReleaseDecision:
    allowed: bool
    state: str
    reason_codes: Tuple[str, ...]
    artifact_id: str
    policy_id: str
