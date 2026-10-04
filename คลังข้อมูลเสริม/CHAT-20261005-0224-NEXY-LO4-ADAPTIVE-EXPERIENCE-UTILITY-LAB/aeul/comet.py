from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .common import ContractError, fingerprint, require_text, require_unit
from .q64 import Q64


@dataclass(frozen=True, slots=True)
class OverlapEvidence:
    left_id: str
    right_id: str
    overlap: Q64
    basis_id: str

    def __post_init__(self) -> None:
        require_text(self.left_id, "left_id")
        require_text(self.right_id, "right_id")
        require_text(self.basis_id, "basis_id")
        if self.left_id == self.right_id:
            raise ContractError("self-overlap evidence is invalid")
        require_unit(self.overlap, "overlap")

    @property
    def pair(self) -> tuple[str, str]:
        return tuple(sorted((self.left_id, self.right_id)))  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class MarginalValueDecision:
    status: str
    candidate_id: str
    base_value: Q64
    max_overlap: Q64 | None
    retention: Q64 | None
    marginal_value: Q64 | None
    reason: str
    compared_against: tuple[str, ...]
    fingerprint: str


def build_overlap_index(evidence: Iterable[OverlapEvidence]) -> tuple[dict[tuple[str, str], OverlapEvidence], str | None]:
    index: dict[tuple[str, str], OverlapEvidence] = {}
    for item in evidence:
        prev = index.get(item.pair)
        if prev is not None and (prev.overlap != item.overlap or prev.basis_id != item.basis_id):
            return {}, "CONFLICTING_OVERLAP_EVIDENCE"
        index[item.pair] = item
    return index, None


def evaluate_marginal_value(
    *,
    candidate_id: str,
    base_value: Q64,
    selected_ids: Iterable[str],
    evidence: Iterable[OverlapEvidence],
    max_allowed_overlap: Q64,
) -> MarginalValueDecision:
    require_text(candidate_id, "candidate_id")
    require_unit(base_value, "base_value")
    require_unit(max_allowed_overlap, "max_allowed_overlap")
    selected = tuple(sorted(set(selected_ids)))
    if candidate_id in selected:
        return _result("FREEZE", candidate_id, base_value, None, None, None, "CANDIDATE_ALREADY_SELECTED", selected)
    index, error = build_overlap_index(evidence)
    if error:
        return _result("FREEZE", candidate_id, base_value, None, None, None, error, selected)
    overlaps: list[Q64] = []
    for other in selected:
        pair = tuple(sorted((candidate_id, other)))
        item = index.get(pair)
        if item is None:
            return _result("FREEZE", candidate_id, base_value, None, None, None, f"MISSING_OVERLAP_EVIDENCE:{other}", selected)
        overlaps.append(item.overlap)
    max_overlap = max(overlaps, key=lambda x: x.raw) if overlaps else Q64.zero()
    retention = Q64.one() - max_overlap
    marginal = base_value * retention
    if max_overlap.raw > max_allowed_overlap.raw:
        return _result("COLLISION", candidate_id, base_value, max_overlap, retention, marginal, "OVERLAP_EXCEEDS_LIMIT", selected)
    return _result("VALUE", candidate_id, base_value, max_overlap, retention, marginal, "MARGINAL_VALUE_COMPUTED", selected)


def _result(status: str, candidate_id: str, base: Q64, overlap: Q64 | None, retention: Q64 | None, marginal: Q64 | None, reason: str, selected: tuple[str, ...]) -> MarginalValueDecision:
    core = {
        "status": status,
        "candidate_id": candidate_id,
        "base_value": base,
        "max_overlap": overlap,
        "retention": retention,
        "marginal_value": marginal,
        "reason": reason,
        "compared_against": selected,
    }
    return MarginalValueDecision(status, candidate_id, base, overlap, retention, marginal, reason, selected, fingerprint(core))
