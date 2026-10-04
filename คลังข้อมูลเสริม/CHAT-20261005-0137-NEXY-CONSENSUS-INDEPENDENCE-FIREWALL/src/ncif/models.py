from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


class ContractError(ValueError):
    """Raised when the NCIF input contract is malformed or ambiguous."""


_ALLOWED_STANCES = frozenset({"SUPPORT", "OPPOSE", "ABSTAIN"})
_ALLOWED_KINDS = frozenset(
    {
        "source",
        "repo",
        "runtime",
        "external",
        "test",
        "derived",
        "model",
        "document",
        "operator",
    }
)


def _require_nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be a non-empty string")
    return value.strip()


def _string_tuple(value: Any, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ContractError(f"{field} must be an array")
    out: list[str] = []
    seen: set[str] = set()
    for item in value:
        item = _require_nonempty_string(item, field)
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return tuple(sorted(out))


@dataclass(frozen=True, slots=True)
class EvidenceNode:
    evidence_id: str
    kind: str
    source_identity: str
    parents: tuple[str, ...]
    correlation_keys: tuple[str, ...]

    @classmethod
    def from_dict(cls, raw: Any) -> "EvidenceNode":
        if not isinstance(raw, dict):
            raise ContractError("each evidence entry must be an object")
        evidence_id = _require_nonempty_string(raw.get("evidence_id"), "evidence_id")
        kind = _require_nonempty_string(raw.get("kind"), f"evidence[{evidence_id}].kind").lower()
        if kind not in _ALLOWED_KINDS:
            raise ContractError(f"unsupported evidence kind: {kind}")
        source_identity = _require_nonempty_string(
            raw.get("source_identity"), f"evidence[{evidence_id}].source_identity"
        )
        parents = _string_tuple(raw.get("parents", []), f"evidence[{evidence_id}].parents")
        correlation_keys = _string_tuple(
            raw.get("correlation_keys", []), f"evidence[{evidence_id}].correlation_keys"
        )
        if evidence_id in parents:
            # This is still represented as a lineage cycle by the engine, but
            # retaining it here allows a deterministic FREEZE rather than a parse crash.
            pass
        return cls(
            evidence_id=evidence_id,
            kind=kind,
            source_identity=source_identity,
            parents=parents,
            correlation_keys=correlation_keys,
        )


@dataclass(frozen=True, slots=True)
class Vote:
    actor_id: str
    stance: str
    evidence_ids: tuple[str, ...]
    correlation_keys: tuple[str, ...]

    @classmethod
    def from_dict(cls, raw: Any) -> "Vote":
        if not isinstance(raw, dict):
            raise ContractError("each vote entry must be an object")
        actor_id = _require_nonempty_string(raw.get("actor_id"), "actor_id")
        stance = _require_nonempty_string(raw.get("stance"), f"vote[{actor_id}].stance").upper()
        if stance not in _ALLOWED_STANCES:
            raise ContractError(f"unsupported stance: {stance}")
        return cls(
            actor_id=actor_id,
            stance=stance,
            evidence_ids=_string_tuple(raw.get("evidence_ids", []), f"vote[{actor_id}].evidence_ids"),
            correlation_keys=_string_tuple(
                raw.get("correlation_keys", []), f"vote[{actor_id}].correlation_keys"
            ),
        )


@dataclass(frozen=True, slots=True)
class ConsensusPolicy:
    min_support_groups: int = 2
    max_opposition_groups: int = 0
    require_single_root_resilience: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.min_support_groups, bool) or not isinstance(self.min_support_groups, int):
            raise ContractError("min_support_groups must be an integer")
        if self.min_support_groups <= 0:
            raise ContractError("min_support_groups must be > 0")
        if isinstance(self.max_opposition_groups, bool) or not isinstance(self.max_opposition_groups, int):
            raise ContractError("max_opposition_groups must be an integer")
        if self.max_opposition_groups < 0:
            raise ContractError("max_opposition_groups must be >= 0")
        if not isinstance(self.require_single_root_resilience, bool):
            raise ContractError("require_single_root_resilience must be boolean")

    def to_dict(self) -> dict[str, Any]:
        return {
            "min_support_groups": self.min_support_groups,
            "max_opposition_groups": self.max_opposition_groups,
            "require_single_root_resilience": self.require_single_root_resilience,
        }


@dataclass(frozen=True, slots=True)
class IndependenceGroup:
    stance: str
    actor_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    root_evidence_ids: tuple[str, ...]
    correlation_keys: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "stance": self.stance,
            "actor_ids": list(self.actor_ids),
            "evidence_ids": list(self.evidence_ids),
            "root_evidence_ids": list(self.root_evidence_ids),
            "correlation_keys": list(self.correlation_keys),
        }


@dataclass(frozen=True, slots=True)
class ConsensusResult:
    claim_id: str
    decision: str
    support_groups: tuple[IndependenceGroup, ...]
    opposition_groups: tuple[IndependenceGroup, ...]
    abstain_count: int
    freeze_reasons: tuple[str, ...]
    lineage_warnings: tuple[str, ...]
    single_root_resilience_min_support_groups: int | None
    policy: ConsensusPolicy
    verification_status: str
    fingerprint: str

    @property
    def support_group_count(self) -> int:
        return len(self.support_groups)

    @property
    def opposition_group_count(self) -> int:
        return len(self.opposition_groups)

    def without_fingerprint(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "decision": self.decision,
            "support_group_count": self.support_group_count,
            "opposition_group_count": self.opposition_group_count,
            "support_groups": [group.to_dict() for group in self.support_groups],
            "opposition_groups": [group.to_dict() for group in self.opposition_groups],
            "abstain_count": self.abstain_count,
            "freeze_reasons": list(self.freeze_reasons),
            "lineage_warnings": list(self.lineage_warnings),
            "single_root_resilience_min_support_groups": self.single_root_resilience_min_support_groups,
            "policy": self.policy.to_dict(),
            "verification_status": self.verification_status,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self.without_fingerprint(), "fingerprint": self.fingerprint}


def ensure_unique(items: Iterable[str], label: str) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    if duplicates:
        raise ContractError(f"duplicate {label}: {sorted(duplicates)}")
