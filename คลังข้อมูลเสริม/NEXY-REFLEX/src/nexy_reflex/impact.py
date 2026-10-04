"""Deterministic change-impact analysis for requirement snapshots."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any

from .canonical import canonical_json
from .models import RequirementClaim, Snapshot
from .semantics import snapshot_digest


@dataclass(frozen=True, slots=True)
class ImpactReport:
    before_digest: str
    after_digest: str
    target_changed: bool
    added_requirement_ids: tuple[str, ...]
    removed_requirement_ids: tuple[str, ...]
    changed_requirement_ids: tuple[str, ...]
    transitively_impacted_ids: tuple[str, ...]
    evidence_ids_to_invalidate: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "before_digest": self.before_digest,
            "after_digest": self.after_digest,
            "target_changed": self.target_changed,
            "added_requirement_ids": list(self.added_requirement_ids),
            "removed_requirement_ids": list(self.removed_requirement_ids),
            "changed_requirement_ids": list(self.changed_requirement_ids),
            "transitively_impacted_ids": list(self.transitively_impacted_ids),
            "evidence_ids_to_invalidate": list(self.evidence_ids_to_invalidate),
        }


def diff_snapshots(before: Snapshot, after: Snapshot) -> ImpactReport:
    """Compute conservative evidence invalidation caused by a snapshot change."""
    before_by_id = _unique_requirement_map(before.requirements)
    after_by_id = _unique_requirement_map(after.requirements)

    before_ids = set(before_by_id)
    after_ids = set(after_by_id)
    added = after_ids - before_ids
    removed = before_ids - after_ids
    changed = {
        claim_id
        for claim_id in before_ids & after_ids
        if canonical_json(before_by_id[claim_id].to_dict()) != canonical_json(after_by_id[claim_id].to_dict())
    }

    target_changed = canonical_json(before.target.to_dict()) != canonical_json(after.target.to_dict())
    roots = set(added) | set(removed) | set(changed)
    if target_changed:
        roots.update(after_ids)

    reverse: dict[str, set[str]] = defaultdict(set)
    for claim in after.requirements:
        for dep in claim.dependencies:
            reverse[dep].add(claim.claim_id)

    impacted = set(roots)
    queue: deque[str] = deque(sorted(roots))
    while queue:
        current = queue.popleft()
        for dependent in sorted(reverse.get(current, ())):
            if dependent not in impacted:
                impacted.add(dependent)
                queue.append(dependent)

    invalidated_evidence = tuple(
        sorted(record.evidence_id for record in after.evidence if record.requirement_id in impacted)
    )
    return ImpactReport(
        before_digest=snapshot_digest(before),
        after_digest=snapshot_digest(after),
        target_changed=target_changed,
        added_requirement_ids=tuple(sorted(added)),
        removed_requirement_ids=tuple(sorted(removed)),
        changed_requirement_ids=tuple(sorted(changed)),
        transitively_impacted_ids=tuple(sorted(impacted)),
        evidence_ids_to_invalidate=invalidated_evidence,
    )


def _unique_requirement_map(requirements: tuple[RequirementClaim, ...]) -> dict[str, RequirementClaim]:
    result: dict[str, RequirementClaim] = {}
    for claim in requirements:
        if claim.claim_id in result:
            raise ValueError(f"duplicate requirement id prevents impact analysis: {claim.claim_id}")
        result[claim.claim_id] = claim
    return result
