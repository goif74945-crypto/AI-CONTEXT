from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class ProofPlanError(ValueError):
    """Raised when a legal exact proof plan cannot be produced."""


@dataclass(frozen=True)
class ClaimRequirement:
    claim_id: str
    min_evidence_class: int

    def validate(self) -> None:
        if not self.claim_id.strip():
            raise ProofPlanError("claim_id is empty")
        if not 0 <= self.min_evidence_class <= 7:
            raise ProofPlanError("evidence class must be in E0..E7")


@dataclass(frozen=True)
class Probe:
    probe_id: str
    cost: int
    evidence_class: int
    covers: frozenset[str]
    available: bool = True

    def validate(self) -> None:
        if not self.probe_id.strip():
            raise ProofPlanError("probe_id is empty")
        if self.cost < 0:
            raise ProofPlanError(f"probe {self.probe_id}: cost cannot be negative")
        if not 0 <= self.evidence_class <= 7:
            raise ProofPlanError(f"probe {self.probe_id}: invalid evidence class")
        if not self.covers:
            raise ProofPlanError(f"probe {self.probe_id}: covers cannot be empty")


@dataclass(frozen=True)
class PlanResult:
    selected_probe_ids: tuple[str, ...]
    total_cost: int
    coverage: tuple[tuple[str, str], ...]


class MinimumProofPlanner:
    """Exact minimum-cost proof planner using claim-mask dynamic programming.

    Runtime is bounded by the number of claims rather than 2^number-of-probes. The
    planner never downgrades an evidence-class obligation to obtain a cheaper plan.
    """

    def __init__(self, max_exact_claims: int = 18, max_candidate_probes: int = 512) -> None:
        if max_exact_claims < 1:
            raise ProofPlanError("max_exact_claims must be >= 1")
        if max_candidate_probes < 1:
            raise ProofPlanError("max_candidate_probes must be >= 1")
        self.max_exact_claims = max_exact_claims
        self.max_candidate_probes = max_candidate_probes

    def plan(
        self,
        requirements: Iterable[ClaimRequirement],
        probes: Iterable[Probe],
    ) -> PlanResult:
        reqs: dict[str, ClaimRequirement] = {}
        for req in requirements:
            req.validate()
            if req.claim_id in reqs:
                raise ProofPlanError(f"duplicate requirement: {req.claim_id}")
            reqs[req.claim_id] = req
        if not reqs:
            return PlanResult((), 0, ())
        if len(reqs) > self.max_exact_claims:
            raise ProofPlanError(
                f"exact planning claim limit exceeded: {len(reqs)} > {self.max_exact_claims}"
            )

        seen_probe_ids: set[str] = set()
        raw_candidates: list[Probe] = []
        for probe in probes:
            probe.validate()
            if probe.probe_id in seen_probe_ids:
                raise ProofPlanError(f"duplicate probe_id: {probe.probe_id}")
            seen_probe_ids.add(probe.probe_id)
            if probe.available:
                raw_candidates.append(probe)

        claim_ids = tuple(sorted(reqs))
        bit_for = {claim_id: 1 << idx for idx, claim_id in enumerate(claim_ids)}

        candidates: list[tuple[Probe, int]] = []
        for probe in sorted(raw_candidates, key=lambda p: p.probe_id):
            mask = 0
            for claim_id in claim_ids:
                req = reqs[claim_id]
                if claim_id in probe.covers and probe.evidence_class >= req.min_evidence_class:
                    mask |= bit_for[claim_id]
            if mask:
                candidates.append((probe, mask))

        candidates = self._prune_dominated(candidates)

        if len(candidates) > self.max_candidate_probes:
            raise ProofPlanError(
                f"candidate probe limit exceeded: {len(candidates)} > {self.max_candidate_probes}"
            )

        satisfiable_mask = 0
        for _, mask in candidates:
            satisfiable_mask |= mask
        full_mask = (1 << len(claim_ids)) - 1
        if satisfiable_mask != full_mask:
            missing = [
                claim_id
                for claim_id in claim_ids
                if not (satisfiable_mask & bit_for[claim_id])
            ]
            details = ", ".join(
                f"{cid}@E{reqs[cid].min_evidence_class}" for cid in missing
            )
            raise ProofPlanError(f"no available probe satisfies: {details}")

        dp: dict[int, tuple[int, int, tuple[str, ...]]] = {0: (0, 0, ())}
        for probe, probe_mask in candidates:
            snapshot = list(dp.items())
            for mask, state in snapshot:
                new_mask = mask | probe_mask
                if new_mask == mask:
                    continue
                new_ids = state[2] + (probe.probe_id,)
                candidate_state = (state[0] + probe.cost, state[1] + 1, new_ids)
                previous = dp.get(new_mask)
                if previous is None or candidate_state < previous:
                    dp[new_mask] = candidate_state

        if full_mask not in dp:
            raise ProofPlanError("no legal proof plan exists")

        best = dp[full_mask]
        selected_ids = best[2]
        selected = {probe.probe_id: probe for probe, _ in candidates if probe.probe_id in selected_ids}

        coverage: list[tuple[str, str]] = []
        for claim_id in claim_ids:
            req = reqs[claim_id]
            valid = [
                p
                for p in selected.values()
                if claim_id in p.covers and p.evidence_class >= req.min_evidence_class
            ]
            chosen = min(valid, key=lambda p: (p.cost, p.probe_id))
            coverage.append((claim_id, chosen.probe_id))

        return PlanResult(
            selected_probe_ids=selected_ids,
            total_cost=best[0],
            coverage=tuple(coverage),
        )

    @staticmethod
    def _prune_dominated(candidates: list[tuple[Probe, int]]) -> list[tuple[Probe, int]]:
        """Remove probes that cannot participate in the defined optimal solution.

        Safe rules only:
        - strictly cheaper superset dominates a more expensive subset;
        - for identical coverage+cost, lexicographically smaller ID dominates because
          cost and probe count tie before ID order.
        """
        kept: list[tuple[Probe, int]] = []
        for idx, (probe, mask) in enumerate(candidates):
            dominated = False
            for other_idx, (other, other_mask) in enumerate(candidates):
                if idx == other_idx:
                    continue
                superset = (other_mask | mask) == other_mask
                if not superset:
                    continue
                if other.cost < probe.cost:
                    dominated = True
                    break
                if (
                    other.cost == probe.cost
                    and other_mask == mask
                    and other.probe_id < probe.probe_id
                ):
                    dominated = True
                    break
            if not dominated:
                kept.append((probe, mask))
        return kept
