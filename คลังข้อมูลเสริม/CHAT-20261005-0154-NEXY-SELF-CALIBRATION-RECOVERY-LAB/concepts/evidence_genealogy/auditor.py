from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Callable, Iterable

from core.canonical import fingerprint


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    claim_id: str
    source_root: str
    method_family: str
    content_fingerprint: str
    revision: str

    def __post_init__(self) -> None:
        for name in ("evidence_id", "claim_id", "source_root", "method_family", "content_fingerprint", "revision"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


class _UnionFind:
    def __init__(self, ids: Iterable[str]) -> None:
        self.parent = {x: x for x in ids}

    def find(self, x: str) -> str:
        p = self.parent[x]
        if p != x:
            self.parent[x] = self.find(p)
        return self.parent[x]

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            if ra < rb:
                self.parent[rb] = ra
            else:
                self.parent[ra] = rb


def _group_edges(
    rows: list[EvidenceItem],
    key: Callable[[EvidenceItem], str],
    reason: str,
) -> list[dict[str, str]]:
    groups: dict[str, list[str]] = {}
    for item in rows:
        groups.setdefault(key(item), []).append(item.evidence_id)
    edges: list[dict[str, str]] = []
    for group_key in sorted(groups):
        ids = sorted(groups[group_key])
        if len(ids) < 2:
            continue
        anchor = ids[0]
        for other in ids[1:]:
            edges.append({"left": anchor, "right": other, "reason": reason})
    return edges


def audit_independence(
    items: Iterable[EvidenceItem],
    *,
    target_revision: str,
    required_independent_groups: int = 2,
    correlate_by_method_family: bool = False,
) -> dict[str, object]:
    rows = sorted(list(items), key=lambda x: x.evidence_id)
    if not target_revision.strip():
        raise ValueError("target_revision must be non-empty")
    if required_independent_groups < 1:
        raise ValueError("required_independent_groups must be >= 1")
    ids = [x.evidence_id for x in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate evidence_id")
    claim_ids = {x.claim_id for x in rows}
    if len(claim_ids) > 1:
        raise ValueError("all evidence items must target one claim_id")

    uf = _UnionFind(ids)
    reasons = _group_edges(rows, lambda x: x.content_fingerprint, "IDENTICAL_CONTENT")
    reasons += _group_edges(rows, lambda x: x.source_root, "SHARED_SOURCE_ROOT")
    if correlate_by_method_family:
        reasons += _group_edges(rows, lambda x: x.method_family, "SHARED_METHOD_FAMILY")

    # Index-group union is O(n alpha(n)) after sorting, avoiding all-pairs O(n²).
    for edge in reasons:
        uf.union(edge["left"], edge["right"])

    clusters: dict[str, list[str]] = {}
    for item in rows:
        root = uf.find(item.evidence_id)
        clusters.setdefault(root, []).append(item.evidence_id)
    cluster_list = sorted((sorted(v) for v in clusters.values()), key=lambda x: x[0])
    stale = sorted(x.evidence_id for x in rows if x.revision != target_revision)

    if stale:
        status = "STALE_EVIDENCE"
    elif len(cluster_list) < required_independent_groups:
        status = "INSUFFICIENT_INDEPENDENCE"
    else:
        status = "READY"

    payload = {
        "status": status,
        "claim_id": next(iter(claim_ids), None),
        "target_revision": target_revision,
        "evidence_count": len(rows),
        "independent_group_count": len(cluster_list),
        "required_independent_groups": required_independent_groups,
        "clusters": cluster_list,
        "correlation_edges": sorted(reasons, key=lambda x: (x["left"], x["right"], x["reason"])),
        "stale_evidence": stale,
        "interpretation": "GROUP_COUNT_IS_STRUCTURAL_NOT_PROBABILISTIC_PROOF",
    }
    payload["audit_fingerprint"] = fingerprint(payload)
    return payload
