"""Input and deterministic work-budget admission for experimental MUSCLE.

AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from frontier_assurance_lab import Constraint, ConstraintEngine, FreezeError, stable_hash


def _positive_exact_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


@dataclass(frozen=True)
class MuscleSearchBudget:
    max_variables: int = 64
    max_domain_values: int = 4096
    max_constraints: int = 128
    max_constraint_values: int = 512
    max_subset_checks: int = 65535

    def __post_init__(self) -> None:
        for name in (
            "max_variables",
            "max_domain_values",
            "max_constraints",
            "max_constraint_values",
            "max_subset_checks",
        ):
            if not _positive_exact_int(getattr(self, name)):
                raise FreezeError(f"{name} must be a positive exact integer")


class MuscleInputAssurance:
    """Validate and budget inputs before delegating to ConstraintEngine."""

    @staticmethod
    def _normalize_domains(domains: Mapping[str, tuple[str, ...]]) -> dict[str, tuple[str, ...]]:
        if not isinstance(domains, Mapping) or not domains:
            raise FreezeError("MUSCLE domains must be a non-empty mapping")
        normalized: dict[str, tuple[str, ...]] = {}
        for name, values in domains.items():
            if not isinstance(name, str) or not name.strip():
                raise FreezeError("domain names must be non-empty exact strings")
            if not isinstance(values, tuple) or not values:
                raise FreezeError(f"domain {name!r} values must be a non-empty tuple")
            if any(not isinstance(value, str) or not value.strip() for value in values):
                raise FreezeError(f"domain {name!r} has an invalid value")
            if len(set(values)) != len(values):
                raise FreezeError(f"domain {name!r} values must be unique")
            normalized[name] = tuple(sorted(values))
        return {name: normalized[name] for name in sorted(normalized)}

    @staticmethod
    def _normalize_constraints(
        constraints: list[Constraint] | tuple[Constraint, ...],
        domains: Mapping[str, tuple[str, ...]],
    ) -> tuple[Constraint, ...]:
        if type(constraints) not in (list, tuple):
            raise FreezeError("constraints must be a finite built-in list or tuple")
        items = tuple(constraints)
        if any(not isinstance(item, Constraint) for item in items):
            raise FreezeError("all MUSCLE inputs must be Constraint values")
        if len({item.cid for item in items}) != len(items):
            raise FreezeError("constraint ids must be unique")
        for item in items:
            if item.variable not in domains:
                raise FreezeError(f"constraint {item.cid} references an unknown variable")
            if not isinstance(item.values, tuple):
                raise FreezeError(f"constraint {item.cid} values must be a tuple")
            if any(not isinstance(value, str) or not value.strip() for value in item.values):
                raise FreezeError(f"constraint {item.cid} has an invalid value")
            if len(set(item.values)) != len(item.values):
                raise FreezeError(f"constraint {item.cid} values must be unique")
            unknown = sorted(set(item.values) - set(domains[item.variable]))
            if unknown:
                raise FreezeError(
                    f"constraint {item.cid} has values outside domain {item.variable}: {unknown}"
                )
        return tuple(sorted(items, key=lambda item: item.cid))

    @staticmethod
    def _input_record(
        domains: Mapping[str, tuple[str, ...]], constraints: tuple[Constraint, ...]
    ) -> dict:
        return {
            "domains": {name: list(values) for name, values in domains.items()},
            "constraints": [
                {
                    "cid": item.cid,
                    "variable": item.variable,
                    "op": item.op,
                    "values": sorted(item.values),
                }
                for item in constraints
            ],
        }

    def solve(
        self,
        domains: Mapping[str, tuple[str, ...]],
        constraints: list[Constraint] | tuple[Constraint, ...],
        budget: MuscleSearchBudget,
    ) -> dict:
        if not isinstance(budget, MuscleSearchBudget):
            raise FreezeError("invalid MUSCLE search budget")
        normalized_domains = self._normalize_domains(domains)
        items = self._normalize_constraints(constraints, normalized_domains)

        counts = {name: 0 for name in normalized_domains}
        for item in items:
            counts[item.variable] += 1
        domain_values = sum(len(values) for values in normalized_domains.values())
        constraint_values = sum(len(item.values) for item in items)
        subset_checks = sum((1 << count) - 1 for count in counts.values())
        budget_record = {
            "variables": len(normalized_domains),
            "domain_values": domain_values,
            "constraints": len(items),
            "constraint_values": constraint_values,
            "constraints_per_variable": counts,
            "subset_checks_upper_bound": subset_checks,
            "limits": {
                "max_variables": budget.max_variables,
                "max_domain_values": budget.max_domain_values,
                "max_constraints": budget.max_constraints,
                "max_constraint_values": budget.max_constraint_values,
                "max_subset_checks": budget.max_subset_checks,
            },
        }
        input_hash = stable_hash(self._input_record(normalized_domains, items))

        gaps: list[str] = []
        if len(normalized_domains) > budget.max_variables:
            gaps.append("VARIABLE_BUDGET_EXCEEDED")
        if domain_values > budget.max_domain_values:
            gaps.append("DOMAIN_VALUE_BUDGET_EXCEEDED")
        if len(items) > budget.max_constraints:
            gaps.append("CONSTRAINT_BUDGET_EXCEEDED")
        if constraint_values > budget.max_constraint_values:
            gaps.append("CONSTRAINT_VALUE_BUDGET_EXCEEDED")
        if subset_checks > budget.max_subset_checks:
            gaps.append("SUBSET_CHECK_BUDGET_EXCEEDED")

        if gaps:
            result = {
                "status": "FREEZE",
                "reason": "INPUT_OR_SEARCH_BUDGET_EXCEEDED",
                "gaps": sorted(gaps),
                "input_hash": input_hash,
                "budget": budget_record,
            }
            result["result_hash"] = stable_hash(result)
            return result

        max_per_variable = max((count for count in counts.values()), default=0)
        original = ConstraintEngine(
            normalized_domains,
            max_constraints_per_variable=max(1, max_per_variable),
        ).solve(items)
        result = {
            "status": original["status"],
            "reason": "ADMITTED_TO_EXACT_MUSCLE",
            "gaps": [],
            "input_hash": input_hash,
            "budget": budget_record,
            "original": original,
        }
        result["result_hash"] = stable_hash(result)
        return result
