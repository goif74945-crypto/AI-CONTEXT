from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

from .common import Verdict, allow, freeze


@dataclass(frozen=True)
class Witness:
    witness_id: str
    claim_id: str
    artifact_hash: str
    verdict: str
    failure_domains: tuple[str, ...]


def _independent(group: tuple[Witness, ...]) -> bool:
    seen: set[str] = set()
    for witness in group:
        domains = set(witness.failure_domains)
        if seen.intersection(domains):
            return False
        seen.update(domains)
    return True


def verify_independent_quorum(
    witnesses: Iterable[Witness],
    *,
    claim_id: str,
    artifact_hash: str,
    k: int,
) -> Verdict:
    if k <= 0:
        return freeze("INVALID_QUORUM")
    all_w = sorted(witnesses, key=lambda w: w.witness_id)
    if len({w.witness_id for w in all_w}) != len(all_w):
        return freeze("DUPLICATE_WITNESS_ID")
    mismatched = [w.witness_id for w in all_w if w.claim_id != claim_id or w.artifact_hash != artifact_hash]
    if mismatched:
        return freeze("WITNESS_TARGET_MISMATCH", payload={"witnesses": mismatched})
    candidates = tuple(w for w in all_w if w.verdict == "PASS")
    for size in range(k, len(candidates) + 1):
        for group in combinations(candidates, size):
            if _independent(group):
                selected = tuple(w.witness_id for w in group[:k])
                return allow({"quorum": list(selected), "k": k})

    max_group: tuple[Witness, ...] = tuple()
    for size in range(min(k - 1, len(candidates)), 0, -1):
        found = None
        for group in combinations(candidates, size):
            if _independent(group):
                found = group
                break
        if found:
            max_group = found
            break
    counts: dict[str, int] = {}
    for w in candidates:
        for domain in set(w.failure_domains):
            counts[domain] = counts.get(domain, 0) + 1
    repeated = sorted(domain for domain, count in counts.items() if count > 1)
    return freeze(
        "INSUFFICIENT_INDEPENDENT_QUORUM",
        payload={
            "candidate_passes": len(candidates),
            "k": k,
            "max_independent": [w.witness_id for w in max_group],
            "repeated_failure_domains": repeated,
        },
    )
