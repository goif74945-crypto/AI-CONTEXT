from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable
import json

_TIER_WEIGHT = {
    "generated": 1.0,
    "observed": 2.0,
    "verified": 3.0,
    "authoritative": 4.0,
}


def _canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class Claim:
    claim_id: str
    proposition: str
    value: Any
    modality: str
    source_id: str
    source_tier: str
    confidence: float


@dataclass(frozen=True)
class Policy:
    min_score: float = 2.0
    min_margin: float = 0.75


@dataclass(frozen=True)
class Decision:
    status: str
    proposition: str
    value: Any | None
    reason: str
    scores: dict[str, float]
    supporting_claim_ids: tuple[str, ...]


def arbitrate(claims: Iterable[Claim], policy: Policy = Policy()) -> Decision:
    items = list(claims)
    if not items:
        return Decision("FREEZE", "", None, "NO_CLAIMS", {}, ())
    proposition = items[0].proposition
    if not proposition or any(c.proposition != proposition for c in items):
        return Decision("FREEZE", proposition, None, "PROPOSITION_MISMATCH", {}, ())
    if policy.min_score < 0 or policy.min_margin < 0:
        return Decision("FREEZE", proposition, None, "INVALID_POLICY", {}, ())

    for c in items:
        if not c.claim_id or not c.source_id or not c.modality:
            return Decision("FREEZE", proposition, None, "MALFORMED_CLAIM", {}, ())
        if c.source_tier not in _TIER_WEIGHT:
            return Decision("FREEZE", proposition, None, "UNKNOWN_SOURCE_TIER", {}, ())
        if not (0.0 <= c.confidence <= 1.0):
            return Decision("FREEZE", proposition, None, "INVALID_CONFIDENCE", {}, ())

    # Prevent a single source from manufacturing consensus through repetition.
    dedup: dict[str, Claim] = {}
    for c in items:
        prev = dedup.get(c.source_id)
        if prev is None or (_TIER_WEIGHT[c.source_tier], c.confidence, c.claim_id) > (
            _TIER_WEIGHT[prev.source_tier], prev.confidence, prev.claim_id
        ):
            dedup[c.source_id] = c
    effective = list(dedup.values())

    top_weight = max(_TIER_WEIGHT[c.source_tier] for c in effective)
    top_values = {_canon(c.value) for c in effective if _TIER_WEIGHT[c.source_tier] == top_weight}
    if len(top_values) > 1:
        return Decision("CONFLICT", proposition, None, "TOP_TIER_DISAGREEMENT", {}, ())

    scores: dict[str, float] = {}
    value_by_key: dict[str, Any] = {}
    ids_by_key: dict[str, list[str]] = {}
    for c in effective:
        key = _canon(c.value)
        value_by_key[key] = c.value
        ids_by_key.setdefault(key, []).append(c.claim_id)
        scores[key] = scores.get(key, 0.0) + _TIER_WEIGHT[c.source_tier] * c.confidence

    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    winner_key, winner_score = ranked[0]
    runner_score = ranked[1][1] if len(ranked) > 1 else 0.0
    if winner_score < policy.min_score:
        return Decision("FREEZE", proposition, None, "INSUFFICIENT_SCORE", scores, ())
    if winner_score - runner_score < policy.min_margin:
        return Decision("FREEZE", proposition, None, "INSUFFICIENT_MARGIN", scores, ())
    return Decision(
        "ALLOW",
        proposition,
        value_by_key[winner_key],
        "ARBITRATED",
        scores,
        tuple(sorted(ids_by_key[winner_key])),
    )
