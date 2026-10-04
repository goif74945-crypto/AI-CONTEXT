from __future__ import annotations

from dataclasses import dataclass

from .cawt import WindTunnelReport
from .ccf import CompositionReport
from .drcdo import DifferentialReport
from .edel import DebtReport
from .simf import FalsificationReport
from .common import stable_hash


@dataclass(frozen=True, slots=True)
class FrontierPromotionGate:
    status: str
    blocking_codes: tuple[str, ...]
    advisory_codes: tuple[str, ...]
    fingerprint: str


def evaluate_lo4_candidate(
    wind_tunnel: WindTunnelReport,
    debt: DebtReport,
    capability: CompositionReport,
    invariant_falsification: FalsificationReport,
    replay: DifferentialReport,
) -> FrontierPromotionGate:
    blocks: list[str] = []
    advisories: list[str] = ["Lo4_AI_PROPOSAL_ONLY", "CANON_PROMOTION_REQUIRES_FORMAL_AUTHORITY"]
    if wind_tunnel.status != "PASS":
        blocks.append("COUNTERFACTUAL_AUTHORITY_RISK")
    if debt.status != "PASS":
        blocks.append("EVIDENCE_DEBT_PRESENT")
    if capability.status != "PASS":
        blocks.append("CAPABILITY_COMPOSITION_RISK")
    if replay.status != "PASS":
        blocks.append("REPLAY_DIVERGENCE")
    if invariant_falsification.falsified:
        advisories.append("SHADOW_INVARIANTS_FALSIFIED_AS_EXPECTED")
    if invariant_falsification.surviving:
        advisories.append("SURVIVING_SHADOW_INVARIANTS_ARE_NOT_CANON")
    status = "FREEZE" if blocks else "PASS"
    blocks_t, advisories_t = tuple(sorted(set(blocks))), tuple(sorted(set(advisories)))
    return FrontierPromotionGate(status, blocks_t, advisories_t, stable_hash({"status": status, "blocks": blocks_t, "advisories": advisories_t}))
