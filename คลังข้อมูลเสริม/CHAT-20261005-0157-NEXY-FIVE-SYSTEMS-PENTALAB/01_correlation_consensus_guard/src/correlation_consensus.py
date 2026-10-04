from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable, Mapping, Sequence


class ConsensusInputError(ValueError):
    """Raised when consensus input is structurally invalid."""


@dataclass(frozen=True, slots=True)
class Vote:
    agent_id: str
    choice: str
    trust_bps: int
    dependency_domains: tuple[str, ...]
    evidence_level: int = 0


@dataclass(frozen=True, slots=True)
class ConsensusPolicy:
    quorum_bps: int = 6700
    min_independent_clusters: int = 2
    min_evidence_level: int = 0


@dataclass(frozen=True, slots=True)
class ClusterResult:
    cluster_id: str
    members: tuple[str, ...]
    choice: str | None
    weight_bps: int
    reason: str


@dataclass(frozen=True, slots=True)
class ConsensusResult:
    status: str
    winner: str | None
    support_bps: int
    independent_support_clusters: int
    participating_cluster_count: int
    clusters: tuple[ClusterResult, ...]
    reason_codes: tuple[str, ...]
    fingerprint: str


def _clean_text(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise ConsensusInputError(f"{field}:NOT_STRING")
    value = value.strip()
    if not value:
        raise ConsensusInputError(f"{field}:EMPTY")
    return value


def _canonical_vote(vote: Vote) -> Vote:
    agent_id = _clean_text(vote.agent_id, "agent_id")
    choice = _clean_text(vote.choice, "choice")
    if not isinstance(vote.trust_bps, int) or not 0 <= vote.trust_bps <= 10_000:
        raise ConsensusInputError(f"{agent_id}:TRUST_OUT_OF_RANGE")
    if not isinstance(vote.evidence_level, int) or not 0 <= vote.evidence_level <= 7:
        raise ConsensusInputError(f"{agent_id}:EVIDENCE_OUT_OF_RANGE")
    if not isinstance(vote.dependency_domains, tuple):
        raise ConsensusInputError(f"{agent_id}:DOMAINS_NOT_TUPLE")
    domains = tuple(sorted({_clean_text(d, f"{agent_id}.domain") for d in vote.dependency_domains}))
    if not domains:
        raise ConsensusInputError(f"{agent_id}:NO_DEPENDENCY_DOMAIN")
    return Vote(agent_id, choice, vote.trust_bps, domains, vote.evidence_level)


def _validate_policy(policy: ConsensusPolicy) -> None:
    if not 1 <= policy.quorum_bps <= 10_000:
        raise ConsensusInputError("POLICY_QUORUM_OUT_OF_RANGE")
    if policy.min_independent_clusters < 1:
        raise ConsensusInputError("POLICY_MIN_CLUSTERS_INVALID")
    if not 0 <= policy.min_evidence_level <= 7:
        raise ConsensusInputError("POLICY_EVIDENCE_OUT_OF_RANGE")


def _build_components(votes: Sequence[Vote]) -> list[tuple[Vote, ...]]:
    """Build connected components where any shared dependency domain creates correlation."""
    n = len(votes)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            if ra > rb:
                ra, rb = rb, ra
            parent[rb] = ra

    owner: dict[str, int] = {}
    for i, vote in enumerate(votes):
        for domain in vote.dependency_domains:
            if domain in owner:
                union(i, owner[domain])
            else:
                owner[domain] = i

    groups: dict[int, list[Vote]] = {}
    for i, vote in enumerate(votes):
        groups.setdefault(find(i), []).append(vote)
    return [tuple(sorted(group, key=lambda v: v.agent_id)) for _, group in sorted(groups.items())]


def _cluster_result(component: tuple[Vote, ...], policy: ConsensusPolicy) -> ClusterResult:
    members = tuple(v.agent_id for v in component)
    cluster_id = sha256("".join(members).encode()).hexdigest()[:16]
    eligible = [v for v in component if v.evidence_level >= policy.min_evidence_level and v.trust_bps > 0]
    if not eligible:
        return ClusterResult(cluster_id, members, None, 0, "NO_ELIGIBLE_MEMBER")
    choices = {v.choice for v in eligible}
    if len(choices) != 1:
        return ClusterResult(cluster_id, members, None, max(v.trust_bps for v in eligible), "CORRELATED_CLUSTER_DISAGREEMENT")
    return ClusterResult(cluster_id, members, next(iter(choices)), max(v.trust_bps for v in eligible), "COUNTED_ONCE")


def evaluate_consensus(votes: Iterable[Vote], policy: ConsensusPolicy = ConsensusPolicy()) -> ConsensusResult:
    _validate_policy(policy)
    canonical = sorted((_canonical_vote(v) for v in votes), key=lambda v: v.agent_id)
    if not canonical:
        raise ConsensusInputError("NO_VOTES")
    ids = [v.agent_id for v in canonical]
    if len(ids) != len(set(ids)):
        raise ConsensusInputError("DUPLICATE_AGENT_ID")

    clusters = tuple(_cluster_result(c, policy) for c in _build_components(canonical))
    participating = tuple(c for c in clusters if c.choice is not None and c.weight_bps > 0)
    total_weight = sum(c.weight_bps for c in participating)

    reason_codes: list[str] = []
    if any(c.reason == "CORRELATED_CLUSTER_DISAGREEMENT" for c in clusters):
        reason_codes.append("CORRELATED_CLUSTER_DISAGREEMENT")
    if total_weight == 0:
        reason_codes.append("NO_ELIGIBLE_INDEPENDENT_WEIGHT")
        return _finalize("FREEZE", None, 0, 0, clusters, reason_codes, policy)

    support: dict[str, int] = {}
    support_clusters: dict[str, int] = {}
    for c in participating:
        assert c.choice is not None
        support[c.choice] = support.get(c.choice, 0) + c.weight_bps
        support_clusters[c.choice] = support_clusters.get(c.choice, 0) + 1

    ranked = sorted(support.items(), key=lambda kv: (-kv[1], kv[0]))
    top_choice, top_weight = ranked[0]
    if len(ranked) > 1 and ranked[1][1] == top_weight:
        reason_codes.append("WEIGHT_TIE")
        return _finalize("FREEZE", None, 0, 0, clusters, reason_codes, policy)

    support_bps = (top_weight * 10_000) // total_weight
    independent = support_clusters[top_choice]
    if support_bps < policy.quorum_bps:
        reason_codes.append("QUORUM_NOT_MET")
    if independent < policy.min_independent_clusters:
        reason_codes.append("INSUFFICIENT_INDEPENDENT_CLUSTERS")

    status = "CONSENSUS" if not reason_codes else "FREEZE"
    winner = top_choice if status == "CONSENSUS" else None
    return _finalize(status, winner, support_bps, independent, clusters, reason_codes, policy)


def _finalize(
    status: str,
    winner: str | None,
    support_bps: int,
    independent: int,
    clusters: tuple[ClusterResult, ...],
    reason_codes: Sequence[str],
    policy: ConsensusPolicy,
) -> ConsensusResult:
    payload: Mapping[str, object] = {
        "status": status,
        "winner": winner,
        "support_bps": support_bps,
        "independent_support_clusters": independent,
        "clusters": [
            {
                "cluster_id": c.cluster_id,
                "members": list(c.members),
                "choice": c.choice,
                "weight_bps": c.weight_bps,
                "reason": c.reason,
            }
            for c in clusters
        ],
        "reason_codes": sorted(set(reason_codes)),
        "policy": {
            "quorum_bps": policy.quorum_bps,
            "min_independent_clusters": policy.min_independent_clusters,
            "min_evidence_level": policy.min_evidence_level,
        },
    }
    canonical_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    fingerprint = sha256(canonical_json.encode()).hexdigest()
    return ConsensusResult(
        status=status,
        winner=winner,
        support_bps=support_bps,
        independent_support_clusters=independent,
        participating_cluster_count=sum(1 for c in clusters if c.choice is not None and c.weight_bps > 0),
        clusters=clusters,
        reason_codes=tuple(sorted(set(reason_codes))),
        fingerprint=fingerprint,
    )
