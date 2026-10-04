from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping

from shared import GateResult, sha256_hex


_EVIDENCE_ORDER = {f"E{i}": i for i in range(8)}


def _evidence_rank(value: str) -> int:
    if value not in _EVIDENCE_ORDER:
        raise ValueError(f"unknown evidence class: {value}")
    return _EVIDENCE_ORDER[value]


@dataclass(frozen=True)
class ClaimNeed:
    claim_id: str
    minimum_class: str

    def __post_init__(self) -> None:
        if not self.claim_id.strip():
            raise ValueError("claim_id must be non-empty")
        _evidence_rank(self.minimum_class)


@dataclass(frozen=True)
class Probe:
    probe_id: str
    cost: int
    produces: Mapping[str, str]
    prerequisites: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.probe_id.strip():
            raise ValueError("probe_id must be non-empty")
        if self.cost < 0:
            raise ValueError("probe cost cannot be negative")
        for evidence_class in self.produces.values():
            _evidence_rank(evidence_class)


def plan_evidence_acquisition(
    needs: Iterable[ClaimNeed],
    probes: Iterable[Probe],
    *,
    available_prerequisites: frozenset[str] = frozenset(),
) -> GateResult:
    need_list = sorted(tuple(needs), key=lambda item: item.claim_id)
    probe_list = sorted(tuple(probes), key=lambda item: item.probe_id)

    claim_ids = [item.claim_id for item in need_list]
    probe_ids = [item.probe_id for item in probe_list]
    if len(set(claim_ids)) != len(claim_ids):
        return GateResult("BLOCKED", "DUPLICATE_CLAIM_ID", {"claim_ids": claim_ids})
    if len(set(probe_ids)) != len(probe_ids):
        return GateResult("BLOCKED", "DUPLICATE_PROBE_ID", {"probe_ids": probe_ids})
    if not need_list:
        return GateResult("PLANNED", "NO_EVIDENCE_NEEDED", {"selected_probes": [], "total_cost": 0})

    index = {need.claim_id: i for i, need in enumerate(need_list)}
    full_mask = (1 << len(need_list)) - 1

    eligible: list[tuple[Probe, int]] = []
    for probe in probe_list:
        if not probe.prerequisites.issubset(available_prerequisites):
            continue
        mask = 0
        for claim_id, produced_class in probe.produces.items():
            if claim_id not in index:
                continue
            need = need_list[index[claim_id]]
            if _evidence_rank(produced_class) >= _evidence_rank(need.minimum_class):
                mask |= 1 << index[claim_id]
        if mask:
            eligible.append((probe, mask))

    # DP value = (cost, probe_count, sorted probe ids)
    best: dict[int, tuple[int, int, tuple[str, ...]]] = {0: (0, 0, ())}
    for probe, probe_mask in eligible:
        snapshot = list(best.items())
        for mask, value in snapshot:
            new_mask = mask | probe_mask
            candidate_ids = tuple(sorted((*value[2], probe.probe_id)))
            candidate = (value[0] + probe.cost, value[1] + 1, candidate_ids)
            current = best.get(new_mask)
            if current is None or candidate < current:
                best[new_mask] = candidate

    if full_mask not in best:
        uncovered = []
        for need in need_list:
            met = any(
                need.claim_id in probe.produces
                and _evidence_rank(probe.produces[need.claim_id]) >= _evidence_rank(need.minimum_class)
                and probe.prerequisites.issubset(available_prerequisites)
                for probe in probe_list
            )
            if not met:
                uncovered.append(need.claim_id)
        return GateResult(
            "FREEZE",
            "NO_COMPLETE_EVIDENCE_PLAN",
            {"uncovered_claims": uncovered, "eligible_probe_count": len(eligible)},
        )

    total_cost, _, selected_ids = best[full_mask]
    selected = {probe.probe_id: probe for probe in probe_list if probe.probe_id in selected_ids}
    witness: dict[str, list[dict[str, str]]] = {}
    for need in need_list:
        witness[need.claim_id] = [
            {"probe_id": probe_id, "produces": selected[probe_id].produces[need.claim_id]}
            for probe_id in selected_ids
            if need.claim_id in selected[probe_id].produces
            and _evidence_rank(selected[probe_id].produces[need.claim_id]) >= _evidence_rank(need.minimum_class)
        ]

    plan_payload = {
        "selected_probes": list(selected_ids),
        "total_cost": total_cost,
        "coverage": witness,
        "available_prerequisites": sorted(available_prerequisites),
    }
    return GateResult(
        "PLANNED",
        "MINIMUM_COST_COMPLETE_EVIDENCE_PLAN",
        {**plan_payload, "plan_hash": sha256_hex(plan_payload)},
    )
