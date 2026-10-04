"""Correlated Evidence Firewall (CEF).

The core rule is intentionally conservative: evidence items that share any
provenance root are treated as one independence cluster. Multiple paraphrases,
model votes, or reports derived from the same upstream source therefore do not
inflate the independent-evidence count.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Mapping


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    evidence_id: str
    claim_id: str
    provenance_roots: frozenset[str]
    confidence: float = 1.0
    source_kind: str = "unspecified"

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id must be non-empty")
        if not self.claim_id.strip():
            raise ValueError("claim_id must be non-empty")
        if not self.provenance_roots:
            raise ValueError("provenance_roots must contain at least one root")
        if any(not root.strip() for root in self.provenance_roots):
            raise ValueError("provenance roots must be non-empty strings")
        if not isfinite(self.confidence) or not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be finite and in [0, 1]")


@dataclass(frozen=True, slots=True)
class EvidenceRequirement:
    minimum_independent_clusters: int = 2
    minimum_effective_weight: float = 1.5

    def __post_init__(self) -> None:
        if self.minimum_independent_clusters < 1:
            raise ValueError("minimum_independent_clusters must be >= 1")
        if not isfinite(self.minimum_effective_weight) or self.minimum_effective_weight < 0:
            raise ValueError("minimum_effective_weight must be finite and >= 0")


@dataclass(frozen=True, slots=True)
class EvidenceAssessment:
    claim_id: str
    status: str
    independent_clusters: tuple[tuple[str, ...], ...]
    cluster_weights: tuple[float, ...]
    effective_weight: float
    reasons: tuple[str, ...]


class _UnionFind:
    def __init__(self, ids: Iterable[str]) -> None:
        self.parent = {item: item for item in ids}

    def find(self, item: str) -> str:
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != item:
            nxt = self.parent[item]
            self.parent[item] = root
            item = nxt
        return root

    def union(self, left: str, right: str) -> None:
        a, b = self.find(left), self.find(right)
        if a == b:
            return
        # Deterministic representative choice prevents order-sensitive output.
        low, high = sorted((a, b))
        self.parent[high] = low


def assess_evidence(
    claim_id: str,
    evidence: Iterable[EvidenceItem],
    requirement: EvidenceRequirement = EvidenceRequirement(),
) -> EvidenceAssessment:
    """Assess evidence independence for exactly one claim.

    Cluster weight is the maximum confidence in the cluster, not the sum. This
    prevents correlated duplicates from manufacturing confidence.
    """

    items = tuple(sorted(evidence, key=lambda item: item.evidence_id))
    if not claim_id.strip():
        raise ValueError("claim_id must be non-empty")
    if any(item.claim_id != claim_id for item in items):
        raise ValueError("all evidence items must match claim_id")
    if len({item.evidence_id for item in items}) != len(items):
        raise ValueError("evidence_id values must be unique")

    if not items:
        return EvidenceAssessment(
            claim_id=claim_id,
            status="FREEZE",
            independent_clusters=(),
            cluster_weights=(),
            effective_weight=0.0,
            reasons=("no evidence supplied",),
        )

    uf = _UnionFind(item.evidence_id for item in items)
    root_owner: dict[str, str] = {}
    by_id: Mapping[str, EvidenceItem] = {item.evidence_id: item for item in items}

    for item in items:
        for root in sorted(item.provenance_roots):
            prior = root_owner.get(root)
            if prior is None:
                root_owner[root] = item.evidence_id
            else:
                uf.union(prior, item.evidence_id)

    grouped: dict[str, list[str]] = {}
    for item in items:
        grouped.setdefault(uf.find(item.evidence_id), []).append(item.evidence_id)

    clusters = tuple(
        sorted((tuple(sorted(members)) for members in grouped.values()), key=lambda c: c[0])
    )
    weights = tuple(max(by_id[eid].confidence for eid in cluster) for cluster in clusters)
    effective_weight = sum(weights)

    reasons: list[str] = []
    if len(clusters) < requirement.minimum_independent_clusters:
        reasons.append(
            f"independent clusters {len(clusters)} < required {requirement.minimum_independent_clusters}"
        )
    if effective_weight < requirement.minimum_effective_weight:
        reasons.append(
            f"effective weight {effective_weight:.6f} < required {requirement.minimum_effective_weight:.6f}"
        )

    return EvidenceAssessment(
        claim_id=claim_id,
        status="PASS" if not reasons else "FREEZE",
        independent_clusters=clusters,
        cluster_weights=weights,
        effective_weight=effective_weight,
        reasons=tuple(reasons),
    )
