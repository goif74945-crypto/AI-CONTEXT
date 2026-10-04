from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from .common import FrontierInputError, canonical_json, require_text, stable_hash


@dataclass(frozen=True, slots=True)
class Observation:
    observation_id: str
    fields: tuple[tuple[str, Any], ...]


@dataclass(frozen=True, slots=True)
class ShadowInvariant:
    invariant_id: str
    kind: str
    fields: tuple[str, ...]
    expected_json: str
    support: int
    status: str = "Lo4_AI_PROPOSAL_ONLY"


@dataclass(frozen=True, slots=True)
class Falsification:
    invariant_id: str
    observation_id: str
    observed_json: str


@dataclass(frozen=True, slots=True)
class MiningReport:
    candidates: tuple[ShadowInvariant, ...]
    fingerprint: str


@dataclass(frozen=True, slots=True)
class FalsificationReport:
    surviving: tuple[ShadowInvariant, ...]
    falsified: tuple[Falsification, ...]
    fingerprint: str


def _canon_observation(o: Observation) -> Observation:
    oid = require_text(o.observation_id, "observation_id")
    values: dict[str, Any] = {}
    for pair in o.fields:
        if not isinstance(pair, tuple) or len(pair) != 2:
            raise FrontierInputError(f"{oid}:FIELD_NOT_PAIR")
        key = require_text(pair[0], f"{oid}.field")
        canonical_json(pair[1])
        if key in values and values[key] != pair[1]:
            raise FrontierInputError(f"{oid}:DUPLICATE_FIELD:{key}")
        values[key] = pair[1]
    if not values:
        raise FrontierInputError(f"{oid}:NO_FIELDS")
    return Observation(oid, tuple(sorted(values.items())))


def mine_shadow_invariants(observations: Iterable[Observation]) -> MiningReport:
    obs = tuple(sorted((_canon_observation(o) for o in observations), key=lambda o: o.observation_id))
    if len(obs) < 2:
        raise FrontierInputError("AT_LEAST_TWO_OBSERVATIONS_REQUIRED")
    ids = [o.observation_id for o in obs]
    if len(ids) != len(set(ids)):
        raise FrontierInputError("DUPLICATE_OBSERVATION_ID")
    maps = [dict(o.fields) for o in obs]
    common_fields = sorted(set.intersection(*(set(m) for m in maps)))
    candidates: list[ShadowInvariant] = []

    for field in common_fields:
        vals = [m[field] for m in maps]
        if all(v == vals[0] for v in vals[1:]):
            expected = canonical_json(vals[0])
            iid = "const-" + stable_hash({"field": field, "value": vals[0]})[:16]
            candidates.append(ShadowInvariant(iid, "CONSTANT", (field,), expected, len(obs)))
        if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in vals):
            lo, hi = min(vals), max(vals)
            expected = canonical_json({"min": lo, "max": hi})
            iid = "range-" + stable_hash({"field": field, "min": lo, "max": hi})[:16]
            candidates.append(ShadowInvariant(iid, "NUMERIC_RANGE", (field,), expected, len(obs)))

    for i, left in enumerate(common_fields):
        for right in common_fields[i + 1 :]:
            if all(m[left] == m[right] for m in maps):
                iid = "eq-" + stable_hash({"left": left, "right": right})[:16]
                candidates.append(ShadowInvariant(iid, "FIELD_EQUALITY", (left, right), "true", len(obs)))

    ordered = tuple(sorted(candidates, key=lambda c: (c.kind, c.fields, c.invariant_id)))
    return MiningReport(ordered, stable_hash(ordered))


def _holds(inv: ShadowInvariant, fields: Mapping[str, Any]) -> tuple[bool, Any]:
    if any(k not in fields for k in inv.fields):
        return False, {"missing": [k for k in inv.fields if k not in fields]}
    if inv.kind == "CONSTANT":
        expected = inv.expected_json
        observed = canonical_json(fields[inv.fields[0]])
        return observed == expected, fields[inv.fields[0]]
    if inv.kind == "NUMERIC_RANGE":
        import json
        bounds = json.loads(inv.expected_json)
        value = fields[inv.fields[0]]
        ok = isinstance(value, (int, float)) and not isinstance(value, bool) and bounds["min"] <= value <= bounds["max"]
        return ok, value
    if inv.kind == "FIELD_EQUALITY":
        left, right = inv.fields
        return fields[left] == fields[right], {left: fields[left], right: fields[right]}
    raise FrontierInputError(f"UNKNOWN_INVARIANT_KIND:{inv.kind}")


def falsify_shadow_invariants(candidates: Sequence[ShadowInvariant], challenges: Iterable[Observation]) -> FalsificationReport:
    obs = tuple(sorted((_canon_observation(o) for o in challenges), key=lambda o: o.observation_id))
    falsified: list[Falsification] = []
    dead: set[str] = set()
    for inv in sorted(candidates, key=lambda x: x.invariant_id):
        if inv.status != "Lo4_AI_PROPOSAL_ONLY":
            raise FrontierInputError(f"{inv.invariant_id}:UNEXPECTED_PROMOTION_STATE")
        for o in obs:
            ok, observed = _holds(inv, dict(o.fields))
            if not ok:
                falsified.append(Falsification(inv.invariant_id, o.observation_id, canonical_json(observed)))
                dead.add(inv.invariant_id)
                break
    surviving = tuple(inv for inv in sorted(candidates, key=lambda x: x.invariant_id) if inv.invariant_id not in dead)
    falsifications = tuple(sorted(falsified, key=lambda x: (x.invariant_id, x.observation_id)))
    return FalsificationReport(surviving, falsifications, stable_hash({"surviving": surviving, "falsified": falsifications}))
