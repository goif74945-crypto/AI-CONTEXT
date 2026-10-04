from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import Iterable, Mapping

from shared import GateResult, sha256_hex


_EVIDENCE_ORDER = {f"E{i}": i for i in range(8)}


def _rank(value: str) -> int:
    if value not in _EVIDENCE_ORDER:
        raise ValueError(f"unknown evidence class: {value}")
    return _EVIDENCE_ORDER[value]


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    claim_id: str
    evidence_class: str
    producer: str
    failure_domains: frozenset[str]
    derived_from: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.evidence_id.strip() or not self.claim_id.strip() or not self.producer.strip():
            raise ValueError("evidence_id, claim_id, and producer must be non-empty")
        _rank(self.evidence_class)
        if not self.failure_domains:
            raise ValueError("at least one failure domain is required")


@dataclass(frozen=True)
class QuorumNeed:
    claim_id: str
    minimum_class: str
    independent_witnesses: int = 2

    def __post_init__(self) -> None:
        if not self.claim_id.strip():
            raise ValueError("claim_id must be non-empty")
        _rank(self.minimum_class)
        if self.independent_witnesses < 1:
            raise ValueError("independent_witnesses must be >= 1")


def _closure(evidence_id: str, by_id: Mapping[str, EvidenceRecord], stack: tuple[str, ...] = ()) -> tuple[set[str], set[str], set[str]]:
    if evidence_id in stack:
        cycle = " -> ".join((*stack, evidence_id))
        raise ValueError(f"evidence dependency cycle: {cycle}")
    if evidence_id not in by_id:
        raise KeyError(f"missing derived evidence: {evidence_id}")
    record = by_id[evidence_id]
    ids = {record.evidence_id}
    producers = {record.producer}
    domains = set(record.failure_domains)
    for parent in record.derived_from:
        p_ids, p_producers, p_domains = _closure(parent, by_id, (*stack, evidence_id))
        ids |= p_ids
        producers |= p_producers
        domains |= p_domains
    return ids, producers, domains


def evaluate_independent_quorum(
    need: QuorumNeed,
    evidence: Iterable[EvidenceRecord],
) -> GateResult:
    records = sorted(tuple(evidence), key=lambda item: item.evidence_id)
    ids = [item.evidence_id for item in records]
    if len(ids) != len(set(ids)):
        return GateResult("BLOCKED", "DUPLICATE_EVIDENCE_ID", {"evidence_ids": ids})
    by_id = {item.evidence_id: item for item in records}

    closures: dict[str, tuple[set[str], set[str], set[str]]] = {}
    try:
        for record in records:
            closures[record.evidence_id] = _closure(record.evidence_id, by_id)
    except (ValueError, KeyError) as exc:
        return GateResult(
            "BLOCKED",
            "INVALID_EVIDENCE_DEPENDENCY_GRAPH",
            {"error_type": type(exc).__name__, "error": str(exc)},
        )

    candidates = [
        record
        for record in records
        if record.claim_id == need.claim_id and _rank(record.evidence_class) >= _rank(need.minimum_class)
    ]

    for combo in combinations(candidates, need.independent_witnesses):
        seen_ids: set[str] = set()
        seen_producers: set[str] = set()
        seen_domains: set[str] = set()
        independent = True
        for record in combo:
            closure_ids, producers, domains = closures[record.evidence_id]
            if seen_ids & closure_ids or seen_producers & producers or seen_domains & domains:
                independent = False
                break
            seen_ids |= closure_ids
            seen_producers |= producers
            seen_domains |= domains
        if independent:
            selected = [item.evidence_id for item in combo]
            witness_payload = {
                "claim_id": need.claim_id,
                "minimum_class": need.minimum_class,
                "selected_evidence": selected,
                "independent_witnesses": need.independent_witnesses,
                "producer_closure": sorted(seen_producers),
                "failure_domain_closure": sorted(seen_domains),
            }
            return GateResult(
                "PASS",
                "INDEPENDENT_EVIDENCE_QUORUM_SATISFIED",
                {**witness_payload, "quorum_hash": sha256_hex(witness_payload)},
            )

    eligible_ids = [item.evidence_id for item in candidates]
    all_domains = sorted({d for item in candidates for d in closures[item.evidence_id][2]})
    all_producers = sorted({p for item in candidates for p in closures[item.evidence_id][1]})
    return GateResult(
        "FREEZE",
        "NO_INDEPENDENT_EVIDENCE_QUORUM",
        {
            "claim_id": need.claim_id,
            "required_witnesses": need.independent_witnesses,
            "eligible_evidence": eligible_ids,
            "observed_failure_domains": all_domains,
            "observed_producers": all_producers,
        },
    )
