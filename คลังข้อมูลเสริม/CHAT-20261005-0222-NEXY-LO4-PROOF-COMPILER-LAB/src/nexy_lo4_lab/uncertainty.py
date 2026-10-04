from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class LatticeError(ValueError):
    """Raised for invalid epistemic dependency graphs."""


class EpistemicStatus(str, Enum):
    PASS = "PASS"
    UNKNOWN = "UNKNOWN"
    NOT_VERIFIED = "NOT_VERIFIED"
    CONFLICT = "CONFLICT"
    FAIL = "FAIL"


_RANK = {
    EpistemicStatus.PASS: 0,
    EpistemicStatus.UNKNOWN: 1,
    EpistemicStatus.NOT_VERIFIED: 2,
    EpistemicStatus.CONFLICT: 3,
    EpistemicStatus.FAIL: 4,
}


@dataclass(frozen=True)
class ClaimNode:
    claim_id: str
    local_status: EpistemicStatus
    depends_on: tuple[str, ...] = ()


@dataclass(frozen=True)
class EffectiveClaimState:
    claim_id: str
    local_status: EpistemicStatus
    effective_status: EpistemicStatus
    blockers: tuple[str, ...]


class UncertaintyContainmentLattice:
    """Propagates epistemic blockers only through declared dependencies.

    This avoids the unsafe opposite extremes of (a) ignoring uncertainty and (b)
    freezing unrelated claims merely because some other branch is unresolved.
    """

    def evaluate(self, nodes: Iterable[ClaimNode]) -> dict[str, EffectiveClaimState]:
        by_id: dict[str, ClaimNode] = {}
        for node in nodes:
            if not isinstance(node.local_status, EpistemicStatus):
                raise LatticeError(f"claim {node.claim_id}: invalid epistemic status")
            if not node.claim_id.strip():
                raise LatticeError("claim_id is empty")
            if node.claim_id in by_id:
                raise LatticeError(f"duplicate claim_id: {node.claim_id}")
            if len(set(node.depends_on)) != len(node.depends_on):
                raise LatticeError(f"claim {node.claim_id}: duplicate dependency")
            by_id[node.claim_id] = node

        for node in by_id.values():
            missing = sorted(set(node.depends_on) - by_id.keys())
            if missing:
                raise LatticeError(
                    f"claim {node.claim_id}: missing dependencies {missing}"
                )

        memo: dict[str, EffectiveClaimState] = {}
        visiting: set[str] = set()

        def resolve(claim_id: str) -> EffectiveClaimState:
            if claim_id in memo:
                return memo[claim_id]
            if claim_id in visiting:
                raise LatticeError(f"dependency cycle at {claim_id}")
            visiting.add(claim_id)
            node = by_id[claim_id]
            effective = node.local_status
            blockers: set[str] = set()
            if node.local_status != EpistemicStatus.PASS:
                blockers.add(claim_id)

            for dep_id in sorted(node.depends_on):
                dep = resolve(dep_id)
                if _RANK[dep.effective_status] > _RANK[effective]:
                    effective = dep.effective_status
                if dep.effective_status != EpistemicStatus.PASS:
                    blockers.update(dep.blockers)

            visiting.remove(claim_id)
            state = EffectiveClaimState(
                claim_id=claim_id,
                local_status=node.local_status,
                effective_status=effective,
                blockers=tuple(sorted(blockers)),
            )
            memo[claim_id] = state
            return state

        for claim_id in sorted(by_id):
            resolve(claim_id)
        return {claim_id: memo[claim_id] for claim_id in sorted(memo)}
