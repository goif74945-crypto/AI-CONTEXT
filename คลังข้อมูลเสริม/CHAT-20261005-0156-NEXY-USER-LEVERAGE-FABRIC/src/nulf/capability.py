from __future__ import annotations

from dataclasses import dataclass
import heapq

from .common import Verdict, canonical_hash


@dataclass(frozen=True)
class Capability:
    capability_id: str
    status: str
    inputs: frozenset[str]
    outputs: frozenset[str]
    data_classes: frozenset[str]
    permissions: frozenset[str]
    risk_units: int
    cost_units: int


@dataclass(frozen=True)
class CompositionRequest:
    available_types: frozenset[str]
    target_type: str
    allowed_data_classes: frozenset[str]
    allowed_permissions: frozenset[str]
    max_risk_units: int
    max_cost_units: int
    max_steps: int = 8


def compose(request: CompositionRequest, capabilities: tuple[Capability, ...]) -> dict:
    if not request.target_type.strip() or request.max_risk_units < 0 or request.max_cost_units < 0 or request.max_steps < 0:
        return {"verdict": Verdict.FREEZE.value, "reason_codes": ["INVALID_REQUEST"], "plan": []}
    ids = [c.capability_id for c in capabilities]
    if len(ids) != len(set(ids)):
        return {"verdict": Verdict.FREEZE.value, "reason_codes": ["DUPLICATE_CAPABILITY_ID"], "plan": []}
    if request.target_type in request.available_types:
        out = {"verdict": Verdict.PASS.value, "reason_codes": [], "plan": [], "risk_units": 0, "cost_units": 0, "final_types": sorted(request.available_types)}
        out["fingerprint"] = canonical_hash({"request": request, "capabilities": sorted(capabilities, key=lambda c: c.capability_id), "result": out})
        return out

    eligible = tuple(sorted(
        (
            c for c in capabilities
            if c.status == "AVAILABLE"
            and c.risk_units >= 0
            and c.cost_units >= 0
            and c.data_classes.issubset(request.allowed_data_classes)
            and c.permissions.issubset(request.allowed_permissions)
        ),
        key=lambda c: c.capability_id,
    ))

    start = frozenset(request.available_types)
    queue: list[tuple[int, int, int, tuple[str, ...], frozenset[str]]] = [(0, 0, 0, (), start)]
    best: dict[frozenset[str], tuple[int, int, int, tuple[str, ...]]] = {start: (0, 0, 0, ())}

    while queue:
        risk, cost, steps, plan, types = heapq.heappop(queue)
        state_key = (risk, cost, steps, plan)J        if best.get(types) != state_key:
            continue
        if request.target_type in types:
            out = {
                "verdict": Verdict.PASS.value,
                "reason_codes": [],
                "plan": list(plan),
                "risk_units": risk,
                "cost_units": cost,
                "final_types": sorted(types),
            }
            out["fingerprint"] = canonical_hash({"request": request, "capabilities": sorted(capabilities, key=lambda c: c.capability_id), "result": out})
            return out
        if steps >= request.max_steps:
            continue
        for cap in eligible:
            if cap.capability_id in plan or not cap.inputs.issubset(types):
                continue
            next_risk = risk + cap.risk_units
            next_cost = cost + cap.cost_units
            if next_risk > request.max_risk_units or next_cost > request.max_cost_units:
                continue
            next_types = frozenset(types | cap.outputs)
            if next_types == types:
                continue
            next_plan = plan + (cap.capability_id,)
            next_key = (next_risk, next_cost, steps + 1, next_plan)
            if next_types not in best or next_key < best[next_types]:
                best[next_types] = next_key
                heapq.heappush(queue, (next_risk, next_cost, steps + 1, next_plan, next_types))

    out = {
        "verdict": Verdict.FREEZE.value,
        "reason_codes": ["NO_POLICY_COMPLIANT_COMPOSITION"],
        "plan": [],
        "eligible_capabilities": [c.capability_id for c in eligible],
    }
    out["fingerprint"] = canonical_hash({"request": request, "capabilities": sorted(capabilities, key=lambda c: c.capability_id), "result": out})
    return out
