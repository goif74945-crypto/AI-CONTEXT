"""Metric-integrity admission adapter for experimental PAREX.

AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from frontier_assurance_lab import FreezeError, ParetoPruner, Plan, stable_hash


_PAREX_DIRECTIONS = {
    "benefit": "MAX",
    "evidence": "MAX",
    "cost": "MIN",
    "latency": "MIN",
    "risk": "MIN",
}
_DIGEST = re.compile(r"^[0-9a-f]{64}$")


def _exact_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True)
class MetricAxis:
    name: str
    direction: str
    unit: str
    minimum: int
    maximum: int

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise FreezeError("metric axis name must be a non-empty string")
        if self.direction not in {"MAX", "MIN"}:
            raise FreezeError("metric axis direction must be MAX or MIN")
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise FreezeError("metric axis unit must be a non-empty string")
        if not _exact_int(self.minimum) or not _exact_int(self.maximum):
            raise FreezeError("metric axis bounds must be exact integers")
        if self.minimum > self.maximum:
            raise FreezeError("metric axis minimum exceeds maximum")


@dataclass(frozen=True)
class ParexMetricContract:
    contract_id: str
    transformation_digest: str
    axes: tuple[MetricAxis, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.contract_id, str) or not self.contract_id.strip():
            raise FreezeError("metric contract id must be a non-empty string")
        if (
            not isinstance(self.transformation_digest, str)
            or not _DIGEST.fullmatch(self.transformation_digest)
        ):
            raise FreezeError("transformation digest must be 64 lowercase hex characters")
        if not isinstance(self.axes, tuple) or not self.axes:
            raise FreezeError("metric contract requires tuple axes")
        if any(not isinstance(axis, MetricAxis) for axis in self.axes):
            raise FreezeError("metric contract axes must be MetricAxis values")
        names = [axis.name for axis in self.axes]
        if len(set(names)) != len(names):
            raise FreezeError("metric axis names must be unique")

    def canonical_record(self) -> dict:
        return {
            "contract_id": self.contract_id,
            "transformation_digest": self.transformation_digest,
            "axes": [
                {
                    "name": axis.name,
                    "direction": axis.direction,
                    "unit": axis.unit,
                    "minimum": axis.minimum,
                    "maximum": axis.maximum,
                }
                for axis in sorted(self.axes, key=lambda item: item.name)
            ],
        }

    def profile_hash(self) -> str:
        return stable_hash(self.canonical_record())


@dataclass(frozen=True)
class AttestedPlan:
    pid: str
    profile_hash: str
    benefit: object
    evidence: object
    cost: object
    latency: object
    risk: object
    metric_evidence: tuple[tuple[str, str], ...]
    hard_eligible: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.pid, str) or not self.pid.strip():
            raise FreezeError("attested plan id must be a non-empty string")
        if not isinstance(self.profile_hash, str) or not _DIGEST.fullmatch(self.profile_hash):
            raise FreezeError("attested plan profile hash must be 64 lowercase hex characters")
        if not isinstance(self.metric_evidence, tuple):
            raise FreezeError("metric evidence must be a tuple")
        if not isinstance(self.hard_eligible, bool):
            raise FreezeError("hard_eligible must be boolean")


class MetricIntegrityPruner:
    """Admit comparable, evidence-bound metrics then delegate to PAREX."""

    @staticmethod
    def _axes(contract: ParexMetricContract) -> dict[str, MetricAxis]:
        if not isinstance(contract, ParexMetricContract):
            raise FreezeError("invalid PAREX metric contract")
        axes = {axis.name: axis for axis in contract.axes}
        if set(axes) != set(_PAREX_DIRECTIONS):
            raise FreezeError("metric contract must define exactly the five PAREX axes")
        for name, direction in _PAREX_DIRECTIONS.items():
            if axes[name].direction != direction:
                raise FreezeError(f"PAREX axis {name} must use direction {direction}")
        return axes

    @staticmethod
    def _evidence(plan: AttestedPlan) -> dict[str, str]:
        pairs = plan.metric_evidence
        if any(not isinstance(pair, tuple) or len(pair) != 2 for pair in pairs):
            raise FreezeError(f"plan {plan.pid} has malformed metric evidence")
        if any(
            not isinstance(name, str)
            or not name.strip()
            or not isinstance(reference, str)
            or not reference.strip()
            for name, reference in pairs
        ):
            raise FreezeError(f"plan {plan.pid} has invalid metric evidence reference")
        names = [pair[0] for pair in pairs]
        if len(set(names)) != len(names):
            raise FreezeError(f"plan {plan.pid} has duplicate metric evidence axes")
        evidence = dict(pairs)
        if set(evidence) != set(_PAREX_DIRECTIONS):
            raise FreezeError(f"plan {plan.pid} must evidence exactly all PAREX axes")
        return evidence

    def prune(
        self,
        contract: ParexMetricContract,
        plans: Iterable[AttestedPlan],
    ) -> dict:
        axes = self._axes(contract)
        items = tuple(plans)
        if not items:
            raise FreezeError("at least one attested plan is required")
        if any(not isinstance(item, AttestedPlan) for item in items):
            raise FreezeError("all candidates must be AttestedPlan values")
        items = tuple(sorted(items, key=lambda item: item.pid))
        if len({item.pid for item in items}) != len(items):
            raise FreezeError("attested plan ids must be unique")

        expected_profile = contract.profile_hash()
        original_plans: list[Plan] = []
        admitted: list[dict] = []
        for item in items:
            if item.profile_hash != expected_profile:
                raise FreezeError(f"plan {item.pid} metric profile mismatch")
            evidence = self._evidence(item)
            values: dict[str, int] = {}
            for name in _PAREX_DIRECTIONS:
                value = getattr(item, name)
                if not _exact_int(value):
                    raise FreezeError(f"plan {item.pid} metric {name} must be an exact integer")
                axis = axes[name]
                if not axis.minimum <= value <= axis.maximum:
                    raise FreezeError(f"plan {item.pid} metric {name} is outside contract bounds")
                values[name] = value

            original_plans.append(
                Plan(
                    item.pid,
                    values["benefit"],
                    values["evidence"],
                    values["cost"],
                    values["latency"],
                    values["risk"],
                    item.hard_eligible,
                )
            )
            admitted.append(
                {
                    "pid": item.pid,
                    "metrics": values,
                    "metric_evidence": {
                        name: evidence[name] for name in sorted(evidence)
                    },
                    "hard_eligible": item.hard_eligible,
                }
            )

        pareto = ParetoPruner().prune(original_plans)
        result = {
            "status": pareto["status"],
            "frontier": pareto["frontier"],
            "pruned": pareto["pruned"],
            "pareto_result_hash": pareto["result_hash"],
            "metric_profile_hash": expected_profile,
            "admitted_candidates_hash": stable_hash(admitted),
        }
        result["result_hash"] = stable_hash(result)
        return result
