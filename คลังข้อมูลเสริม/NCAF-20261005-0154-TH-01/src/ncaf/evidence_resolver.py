from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .common import ContractError, require_nonempty


class ResolutionStatus(str, Enum):
    RESOLVED = "RESOLVED"
    CONFLICT = "CONFLICT"
    INSUFFICIENT = "INSUFFICIENT"


@dataclass(frozen=True)
class Claim:
    key: str
    value: str
    source_id: str
    trust: int
    evidence_count: int

    def __post_init__(self) -> None:
        require_nonempty(self.key, "key")
        require_nonempty(self.value, "value")
        require_nonempty(self.source_id, "source_id")
        if not 0 <= self.trust <= 100:
            raise ContractError("trust must be in [0, 100]")
        if self.evidence_count < 0:
            raise ContractError("evidence_count must be non-negative")


@dataclass(frozen=True)
class Resolution:
    key: str
    status: ResolutionStatus
    value: str | None
    winning_score: int
    runner_up_score: int
    sources: tuple[str, ...]


class EvidenceConflictResolver:
    """Aggregates claims by value and freezes when competing evidence is too close."""

    def __init__(self, *, min_score: int = 60, conflict_margin: int = 15):
        if min_score < 0 or conflict_margin < 0:
            raise ContractError("thresholds must be non-negative")
        self.min_score = min_score
        self.conflict_margin = conflict_margin

    @staticmethod
    def _claim_score(claim: Claim) -> int:
        return claim.trust + min(claim.evidence_count, 20) * 2

    def resolve(self, claims: Iterable[Claim]) -> Resolution:
        claims = tuple(claims)
        if not claims:
            raise ContractError("at least one claim is required")
        keys = {c.key for c in claims}
        if len(keys) != 1:
            raise ContractError("all claims in one resolution must share the same key")
        key = next(iter(keys))
        by_value: dict[str, list[Claim]] = {}
        for claim in claims:
            by_value.setdefault(claim.value, []).append(claim)

        scored = []
        for value, group in by_value.items():
            score = sum(self._claim_score(c) for c in group)
            scored.append((score, value, tuple(sorted(c.source_id for c in group))))
        scored.sort(key=lambda x: (-x[0], x[1], x[2]))
        winner_score, winner_value, winner_sources = scored[0]
        runner_score = scored[1][0] if len(scored) > 1 else 0
        all_sources = tuple(sorted(c.source_id for c in claims))

        if winner_score < self.min_score:
            return Resolution(key, ResolutionStatus.INSUFFICIENT, None, winner_score, runner_score, all_sources)
        if len(scored) > 1 and winner_score - runner_score < self.conflict_margin:
            return Resolution(key, ResolutionStatus.CONFLICT, None, winner_score, runner_score, all_sources)
        return Resolution(key, ResolutionStatus.RESOLVED, winner_value, winner_score, runner_score, winner_sources)
