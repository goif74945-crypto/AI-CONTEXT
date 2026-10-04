from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable, Any


class ContractError(ValueError):
    pass


def _clean_id(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{name} must be a non-empty string")
    return value.strip()


def _clean_ids(name: str, values: Iterable[str]) -> tuple[str, ...]:
    cleaned = tuple(sorted({_clean_id(name, value) for value in values}))
    return cleaned


@dataclass(frozen=True)
class Contribution:
    agent_id: str
    independence_domain: str
    claim_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...]

    @classmethod
    def build(
        cls,
        *,
        agent_id: str,
        independence_domain: str,
        claim_ids: Iterable[str] = (),
        evidence_refs: Iterable[str] = (),
    ) -> "Contribution":
        return cls(
            agent_id=_clean_id("agent_id", agent_id),
            independence_domain=_clean_id("independence_domain", independence_domain),
            claim_ids=_clean_ids("claim_id", claim_ids),
            evidence_refs=_clean_ids("evidence_ref", evidence_refs),
        )


@dataclass(frozen=True)
class Round:
    round_id: str
    contributions: tuple[Contribution, ...]

    @classmethod
    def build(cls, *, round_id: str, contributions: Iterable[Contribution]) -> "Round":
        values = tuple(contributions)
        if not values:
            raise ContractError("round must contain at least one contribution")
        if any(not isinstance(value, Contribution) for value in values):
            raise ContractError("round contributions must be Contribution instances")
        agent_ids = [value.agent_id for value in values]
        if len(set(agent_ids)) != len(agent_ids):
            raise ContractError("agent_id must be unique within a round")
        return cls(round_id=_clean_id("round_id", round_id), contributions=values)


@dataclass(frozen=True)
class RoundMetrics:
    round_id: str
    new_claims: tuple[str, ...]
    new_evidence: tuple[str, ...]
    new_independent_support: tuple[str, ...]

    @property
    def novelty_score(self) -> int:
        return len(self.new_claims) + len(self.new_evidence) + len(self.new_independent_support)


@dataclass(frozen=True)
class SaturationReport:
    status: str
    action: str
    reason_codes: tuple[str, ...]
    metrics: tuple[RoundMetrics, ...]
    fingerprint: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "action": self.action,
            "reason_codes": list(self.reason_codes),
            "fingerprint": self.fingerprint,
            "rounds": [
                {
                    "round_id": m.round_id,
                    "new_claims": list(m.new_claims),
                    "new_evidence": list(m.new_evidence),
                    "new_independent_support": list(m.new_independent_support),
                    "novelty_score": m.novelty_score,
                }
                for m in self.metrics
            ],
        }


def _fingerprint(rounds: tuple[Round, ...], patience: int, min_rounds: int) -> str:
    payload = {
        "patience": patience,
        "min_rounds": min_rounds,
        "rounds": [
            {
                "round_id": round_.round_id,
                "contributions": [
                    {
                        "agent_id": c.agent_id,
                        "independence_domain": c.independence_domain,
                        "claim_ids": list(c.claim_ids),
                        "evidence_refs": list(c.evidence_refs),
                    }
                    for c in sorted(round_.contributions, key=lambda c: c.agent_id)
                ],
            }
            for round_ in rounds
        ],
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256(raw).hexdigest()


def analyze_rounds(
    rounds: Iterable[Round],
    *,
    patience: int = 2,
    min_rounds: int = 2,
) -> SaturationReport:
    values = tuple(rounds)
    if not values:
        raise ContractError("at least one round is required")
    if any(not isinstance(value, Round) for value in values):
        raise ContractError("rounds must contain Round instances")
    if not isinstance(patience, int) or patience < 1:
        raise ContractError("patience must be an integer >= 1")
    if not isinstance(min_rounds, int) or min_rounds < 1:
        raise ContractError("min_rounds must be an integer >= 1")
    round_ids = [value.round_id for value in values]
    if len(set(round_ids)) != len(round_ids):
        raise ContractError("round_id values must be unique")

    seen_claims: set[str] = set()
    seen_evidence: set[str] = set()
    seen_support: set[tuple[str, str]] = set()
    metrics: list[RoundMetrics] = []

    for round_ in values:
        round_claims: set[str] = set()
        round_evidence: set[str] = set()
        round_support: set[tuple[str, str]] = set()
        for contribution in round_.contributions:
            round_claims.update(contribution.claim_ids)
            round_evidence.update(contribution.evidence_refs)
            for claim_id in contribution.claim_ids:
                round_support.add((claim_id, contribution.independence_domain))

        new_claims = round_claims - seen_claims
        new_evidence = round_evidence - seen_evidence
        new_support = round_support - seen_support
        metrics.append(
            RoundMetrics(
                round_id=round_.round_id,
                new_claims=tuple(sorted(new_claims)),
                new_evidence=tuple(sorted(new_evidence)),
                new_independent_support=tuple(sorted(f"{claim}@{domain}" for claim, domain in new_support)),
            )
        )
        seen_claims.update(round_claims)
        seen_evidence.update(round_evidence)
        seen_support.update(round_support)

    saturated = False
    if len(metrics) >= max(min_rounds, patience):
        saturated = all(metric.novelty_score == 0 for metric in metrics[-patience:])

    if saturated:
        status = "SATURATED"
        action = "STOP_EXPANSION"
        reasons = ("NO_STRUCTURAL_NOVELTY", "NOT_A_RELEASE_DECISION")
    else:
        status = "ACTIVE"
        action = "CONTINUE"
        reasons = ("NOVELTY_OR_PATIENCE_REMAINING", "NOT_A_RELEASE_DECISION")

    return SaturationReport(
        status=status,
        action=action,
        reason_codes=reasons,
        metrics=tuple(metrics),
        fingerprint=_fingerprint(values, patience, min_rounds),
    )
