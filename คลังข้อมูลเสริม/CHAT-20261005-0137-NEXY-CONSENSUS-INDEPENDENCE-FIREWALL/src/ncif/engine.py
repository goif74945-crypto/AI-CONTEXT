from __future__ import annotations

from collections import defaultdict
import heapq
from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from .canonical import fingerprint
from .models import (
    ConsensusPolicy,
    ConsensusResult,
    ContractError,
    EvidenceNode,
    IndependenceGroup,
    Vote,
    ensure_unique,
)


@dataclass(frozen=True, slots=True)
class _VoteView:
    vote: Vote
    evidence_ids: frozenset[str]
    root_ids: frozenset[str]
    tokens: frozenset[str]


def _correlation_token(kind: str, value: str) -> str:
    # Domain-separated digest prevents raw provenance metadata from leaking into
    # diagnostic output while preserving deterministic equality/correlation.
    return f"{kind}:{fingerprint({'kind': kind, 'value': value})}"


class _DisjointSet:
    def __init__(self, items: Iterable[str]) -> None:
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}

    def find(self, item: str) -> str:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, a: str, b: str) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


def _parse_payload(raw: Any) -> tuple[str, tuple[EvidenceNode, ...], tuple[Vote, ...]]:
    if not isinstance(raw, dict):
        raise ContractError("input must be an object")
    claim_id = raw.get("claim_id")
    if not isinstance(claim_id, str) or not claim_id.strip():
        raise ContractError("claim_id must be a non-empty string")
    evidence_raw = raw.get("evidence", [])
    votes_raw = raw.get("votes", [])
    if not isinstance(evidence_raw, list):
        raise ContractError("evidence must be an array")
    if not isinstance(votes_raw, list):
        raise ContractError("votes must be an array")
    evidence = tuple(EvidenceNode.from_dict(item) for item in evidence_raw)
    votes = tuple(Vote.from_dict(item) for item in votes_raw)
    ensure_unique((node.evidence_id for node in evidence), "evidence_id")
    ensure_unique((vote.actor_id for vote in votes), "actor_id vote")
    evidence_ids = {node.evidence_id for node in evidence}
    for vote in votes:
        unknown = sorted(set(vote.evidence_ids) - evidence_ids)
        if unknown:
            raise ContractError(f"vote[{vote.actor_id}] references unknown evidence: {unknown}")
    return claim_id.strip(), evidence, votes


def _analyze_lineage(
    evidence: Sequence[EvidenceNode],
) -> tuple[
    tuple[str, ...],
    tuple[str, ...],
    dict[str, frozenset[str]],
    dict[str, frozenset[str]],
]:
    """Validate lineage and propagate root IDs/correlation keys iteratively.

    Edges are parent -> child. Kahn topological processing avoids coupling valid
    lineage depth to Python's recursion limit. Missing parents and cycles are
    fail-closed conditions; maps are returned only for the acyclic known graph.
    """
    by_id = {node.evidence_id: node for node in evidence}
    missing: set[str] = set()
    children: dict[str, list[str]] = {node_id: [] for node_id in by_id}
    indegree: dict[str, int] = {node_id: 0 for node_id in by_id}

    for node in evidence:
        for parent in node.parents:
            if parent not in by_id:
                missing.add(f"{node.evidence_id}->{parent}")
                continue
            children[parent].append(node.evidence_id)
            indegree[node.evidence_id] += 1

    freeze_reasons: list[str] = []
    warnings: list[str] = []
    if missing:
        freeze_reasons.append("MISSING_EVIDENCE_PARENT")
        warnings.extend(f"missing_parent:{item}" for item in sorted(missing))
        return tuple(freeze_reasons), tuple(warnings), {}, {}

    ready = [node_id for node_id, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    root_map: dict[str, frozenset[str]] = {}
    lineage_key_map: dict[str, frozenset[str]] = {}
    processed: list[str] = []

    # Deterministic queue without depending on input order. The list sizes here
    # are bounded by the evidence-node population, and correctness matters more
    # than shaving nanoseconds off bookkeeping.
    while ready:
        node_id = heapq.heappop(ready)
        node = by_id[node_id]
        processed.append(node_id)
        if not node.parents:
            roots = frozenset({node_id})
            inherited_keys = frozenset(_correlation_token("key", key) for key in node.correlation_keys)
        else:
            root_union: set[str] = set()
            key_union: set[str] = {_correlation_token("key", key) for key in node.correlation_keys}
            for parent in node.parents:
                root_union.update(root_map[parent])
                key_union.update(lineage_key_map[parent])
            roots = frozenset(root_union)
            inherited_keys = frozenset(key_union)
        root_map[node_id] = roots
        lineage_key_map[node_id] = inherited_keys

        newly_ready: list[str] = []
        for child in sorted(children[node_id]):
            indegree[child] -= 1
            if indegree[child] == 0:
                newly_ready.append(child)
        for child in newly_ready:
            heapq.heappush(ready, child)

    if len(processed) != len(by_id):
        remaining = tuple(sorted(node_id for node_id, degree in indegree.items() if degree > 0))
        freeze_reasons.append("EVIDENCE_LINEAGE_CYCLE")
        preview = ",".join(remaining[:20])
        suffix = "..." if len(remaining) > 20 else ""
        warnings.append(f"cycle_nodes:{preview}{suffix}")
        return tuple(freeze_reasons), tuple(warnings), {}, {}

    return tuple(freeze_reasons), tuple(warnings), root_map, lineage_key_map


def _build_vote_views(
    evidence: Sequence[EvidenceNode],
    votes: Sequence[Vote],
    root_map: dict[str, frozenset[str]],
    lineage_key_map: dict[str, frozenset[str]],
) -> tuple[_VoteView, ...]:
    by_id = {node.evidence_id: node for node in evidence}
    views: list[_VoteView] = []
    for vote in sorted(votes, key=lambda item: item.actor_id):
        root_ids: set[str] = set()
        tokens: set[str] = {_correlation_token("key", key) for key in vote.correlation_keys}
        for evidence_id in vote.evidence_ids:
            root_ids.update(root_map[evidence_id])
            tokens.update(lineage_key_map[evidence_id])

        for root_id in root_ids:
            root = by_id[root_id]
            tokens.add(f"root:{root_id}")
            tokens.add(_correlation_token("source", root.source_identity))
        views.append(
            _VoteView(
                vote=vote,
                evidence_ids=frozenset(vote.evidence_ids),
                root_ids=frozenset(root_ids),
                tokens=frozenset(tokens),
            )
        )
    return tuple(views)

def _groups_for_stance(views: Sequence[_VoteView], stance: str) -> tuple[IndependenceGroup, ...]:
    selected = [view for view in views if view.vote.stance == stance]
    if not selected:
        return ()
    ids = [view.vote.actor_id for view in selected]
    dsu = _DisjointSet(ids)
    token_owner: dict[str, str] = {}
    for view in selected:
        for token in sorted(view.tokens):
            previous = token_owner.get(token)
            if previous is None:
                token_owner[token] = view.vote.actor_id
            else:
                dsu.union(previous, view.vote.actor_id)

    buckets: dict[str, list[_VoteView]] = defaultdict(list)
    for view in selected:
        buckets[dsu.find(view.vote.actor_id)].append(view)

    groups: list[IndependenceGroup] = []
    for bucket in buckets.values():
        actors = tuple(sorted(view.vote.actor_id for view in bucket))
        evidence_ids = tuple(sorted({item for view in bucket for item in view.evidence_ids}))
        root_ids = tuple(sorted({item for view in bucket for item in view.root_ids}))
        correlation_keys = tuple(
            sorted(
                {
                    token
                    for view in bucket
                    for token in view.tokens
                    if not token.startswith("root:")
                }
            )
        )
        groups.append(
            IndependenceGroup(
                stance=stance,
                actor_ids=actors,
                evidence_ids=evidence_ids,
                root_evidence_ids=root_ids,
                correlation_keys=correlation_keys,
            )
        )
    return tuple(sorted(groups, key=lambda group: group.actor_ids))


def _single_root_resilience_min(views: Sequence[_VoteView]) -> int:
    support_views = [view for view in views if view.vote.stance == "SUPPORT"]
    roots = sorted({root for view in support_views for root in view.root_ids})
    if not roots:
        return 0
    counts: list[int] = []
    for removed_root in roots:
        survivors = [view for view in support_views if removed_root not in view.root_ids]
        counts.append(len(_groups_for_stance(survivors, "SUPPORT")))
    return min(counts) if counts else 0


def evaluate_consensus(raw: Any, policy: ConsensusPolicy | None = None) -> ConsensusResult:
    policy = policy or ConsensusPolicy()
    claim_id, evidence, votes = _parse_payload(raw)

    freeze_reasons: list[str] = []
    lineage_warnings: list[str] = []
    lineage_reasons, warnings, root_map, lineage_key_map = _analyze_lineage(evidence)
    freeze_reasons.extend(lineage_reasons)
    lineage_warnings.extend(warnings)

    for vote in votes:
        if vote.stance in {"SUPPORT", "OPPOSE"} and not vote.evidence_ids:
            freeze_reasons.append(f"{vote.stance}_WITHOUT_EVIDENCE")

    views: tuple[_VoteView, ...] = ()
    support_groups: tuple[IndependenceGroup, ...] = ()
    opposition_groups: tuple[IndependenceGroup, ...] = ()
    resilience_min: int | None = None

    if not lineage_reasons:
        views = _build_vote_views(evidence, votes, root_map, lineage_key_map)
        support_groups = _groups_for_stance(views, "SUPPORT")
        opposition_groups = _groups_for_stance(views, "OPPOSE")

        if len(support_groups) < policy.min_support_groups:
            freeze_reasons.append("INSUFFICIENT_INDEPENDENT_SUPPORT")
        if len(opposition_groups) > policy.max_opposition_groups:
            freeze_reasons.append("INDEPENDENT_OPPOSITION_PRESENT")

        support_roots = {root for group in support_groups for root in group.root_evidence_ids}
        opposition_roots = {root for group in opposition_groups for root in group.root_evidence_ids}
        if support_roots & opposition_roots:
            freeze_reasons.append("SHARED_ROOT_STANCE_CONFLICT")

        resilience_min = _single_root_resilience_min(views)
        if policy.require_single_root_resilience and resilience_min < policy.min_support_groups:
            freeze_reasons.append("SINGLE_ROOT_RESILIENCE_FAILED")

    freeze_reasons = sorted(set(freeze_reasons))
    decision = "FREEZE" if freeze_reasons else "CONSENSUS_CANDIDATE"
    abstain_count = sum(1 for vote in votes if vote.stance == "ABSTAIN")

    provisional = ConsensusResult(
        claim_id=claim_id,
        decision=decision,
        support_groups=support_groups,
        opposition_groups=opposition_groups,
        abstain_count=abstain_count,
        freeze_reasons=tuple(freeze_reasons),
        lineage_warnings=tuple(sorted(set(lineage_warnings))),
        single_root_resilience_min_support_groups=resilience_min,
        policy=policy,
        verification_status="NOT_VERIFIED_FINAL_AUTHORITY",
        fingerprint="",
    )
    digest = fingerprint(provisional.without_fingerprint())
    return ConsensusResult(
        claim_id=provisional.claim_id,
        decision=provisional.decision,
        support_groups=provisional.support_groups,
        opposition_groups=provisional.opposition_groups,
        abstain_count=provisional.abstain_count,
        freeze_reasons=provisional.freeze_reasons,
        lineage_warnings=provisional.lineage_warnings,
        single_root_resilience_min_support_groups=provisional.single_root_resilience_min_support_groups,
        policy=provisional.policy,
        verification_status=provisional.verification_status,
        fingerprint=digest,
    )
