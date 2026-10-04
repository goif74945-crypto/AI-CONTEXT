from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class FieldConstraint:
    kind: str
    values: tuple[Any, ...] = ()
    minimum: float | None = None
    maximum: float | None = None


@dataclass(frozen=True)
class RequirementSpec:
    requirement_id: str
    constraints: Mapping[str, FieldConstraint]
    evidence_class: int


@dataclass(frozen=True)
class Delta:
    requirement_id: str
    change: str
    field_changes: tuple[tuple[str, str], ...]
    required_evidence_class: int
    gates: tuple[str, ...]


def _constraint_relation(old: FieldConstraint, new: FieldConstraint) -> str:
    if old == new:
        return "UNCHANGED"
    if old.kind != new.kind:
        return "MIXED"
    if old.kind == "allowed_set":
        a, b = set(old.values), set(new.values)
        if b < a:
            return "TIGHTENED"
        if a < b:
            return "LOOSENED"
        return "MIXED"
    if old.kind == "interval":
        old_min = float("-inf") if old.minimum is None else old.minimum
        old_max = float("inf") if old.maximum is None else old.maximum
        new_min = float("-inf") if new.minimum is None else new.minimum
        new_max = float("inf") if new.maximum is None else new.maximum
        new_inside = new_min >= old_min and new_max <= old_max
        old_inside = old_min >= new_min and old_max <= new_max
        if new_inside and (new_min > old_min or new_max < old_max):
            return "TIGHTENED"
        if old_inside and (old_min > new_min or old_max < new_max):
            return "LOOSENED"
        return "MIXED"
    return "MIXED"


class RequirementDeltaRevalidationCompiler:
    """Compiles structured requirement deltas into deterministic revalidation obligations."""

    @staticmethod
    def _map(items: Iterable[RequirementSpec]) -> dict[str, RequirementSpec]:
        out: dict[str, RequirementSpec] = {}
        for item in items:
            if item.requirement_id in out:
                raise ValueError(f"duplicate requirement_id: {item.requirement_id}")
            if not 0 <= item.evidence_class <= 7:
                raise ValueError("evidence_class must be within E0..E7")
            out[item.requirement_id] = item
        return out

    @classmethod
    def compare(cls, old: Iterable[RequirementSpec], new: Iterable[RequirementSpec]) -> tuple[Delta, ...]:
        before, after = cls._map(old), cls._map(new)
        deltas: list[Delta] = []
        for req_id in sorted(set(before) | set(after)):
            a, b = before.get(req_id), after.get(req_id)
            if a is None and b is not None:
                deltas.append(Delta(req_id, "ADDED", (), b.evidence_class, ("implement", "positive", "negative", "traceability")))
                continue
            if b is None and a is not None:
                deltas.append(Delta(req_id, "REMOVED", (), 1, ("traceability", "orphan-reference-audit")))
                continue
            assert a is not None and b is not None

            fields: list[tuple[str, str]] = []
            relations: list[str] = []
            for field in sorted(set(a.constraints) | set(b.constraints)):
                ca, cb = a.constraints.get(field), b.constraints.get(field)
                if ca is None:
                    relation = "TIGHTENED"
                elif cb is None:
                    relation = "LOOSENED"
                else:
                    relation = _constraint_relation(ca, cb)
                if relation != "UNCHANGED":
                    fields.append((field, relation))
                    relations.append(relation)

            if b.evidence_class > a.evidence_class:
                fields.append(("evidence_class", "TIGHTENED"))
                relations.append("TIGHTENED")
            elif b.evidence_class < a.evidence_class:
                fields.append(("evidence_class", "LOOSENED"))
                relations.append("LOOSENED")

            if not relations:
                change = "UNCHANGED"
                gates: tuple[str, ...] = ()
                required = b.evidence_class
            elif set(relations) == {"TIGHTENED"}:
                change = "TIGHTENED"
                required = max(a.evidence_class, b.evidence_class)
                gates = ("positive", "negative", "regression", "traceability")
            elif set(relations) == {"LOOSENED"}:
                change = "LOOSENED"
                required = max(1, b.evidence_class)
                gates = ("policy-review", "negative", "regression", "traceability")
            else:
                change = "MIXED"
                required = max(a.evidence_class, b.evidence_class)
                gates = ("positive", "negative", "regression", "policy-review", "traceability")
            deltas.append(Delta(req_id, change, tuple(fields), required, gates))
        return tuple(deltas)
