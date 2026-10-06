"""Bounded exhaustive minimum-conflict coverage for experimental MUSCLE.

AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from itertools import combinations

from frontier_assurance_lab import Constraint, ConstraintEngine, FreezeError, stable_hash
from muscle_input_assurance import MuscleInputAssurance, MuscleSearchBudget


def _positive_exact_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


@dataclass(frozen=True)
class ConflictCoverageContract:
    """Bound the size of an exhaustive minimum-core certificate."""

    max_cores_per_variable: int = 256
    max_total_cores: int = 1024

    def __post_init__(self) -> None:
        for name in ("max_cores_per_variable", "max_total_cores"):
            if not _positive_exact_int(getattr(self, name)):
                raise FreezeError(f"{name} must be a positive exact integer")

    def contract_hash(self) -> str:
        return stable_hash(
            {
                "max_cores_per_variable": self.max_cores_per_variable,
                "max_total_cores": self.max_total_cores,
            }
        )


class MuscleConflictCoverageAssurance:
    """Enumerate every minimum-cardinality conflict for every unsat variable."""

    def __init__(self) -> None:
        self.base = MuscleInputAssurance()

    @staticmethod
    def _result(payload: dict) -> dict:
        payload["result_hash"] = stable_hash(payload)
        return payload

    def assess(
        self,
        domains: Mapping[str, tuple[str, ...]],
        constraints: list[Constraint] | tuple[Constraint, ...],
        search_budget: MuscleSearchBudget,
        contract: ConflictCoverageContract,
    ) -> dict:
        if not isinstance(contract, ConflictCoverageContract):
            raise FreezeError("invalid MUSCLE conflict coverage contract")

        base = self.base.solve(domains, constraints, search_budget)
        contract_hash = contract.contract_hash()
        common = {
            "contract_hash": contract_hash,
            "input_hash": base["input_hash"],
            "base": base,
        }

        if base["status"] == "SAT":
            coverage = {"unsat_variables": [], "conflict_families": {}}
            return self._result(
                {
                    "status": "SAT",
                    "reason": "NO_CONFLICTS",
                    "gaps": [],
                    **common,
                    **coverage,
                    "subset_checks_executed": 0,
                    "coverage_hash": stable_hash(coverage),
                }
            )

        if base["status"] != "UNSAT":
            coverage = {"unsat_variables": [], "conflict_families": {}}
            return self._result(
                {
                    "status": "FREEZE",
                    "reason": "BASE_MUSCLE_NOT_ADMITTED",
                    "gaps": list(base.get("gaps", [])),
                    **common,
                    **coverage,
                    "subset_checks_executed": 0,
                    "coverage_hash": stable_hash(coverage),
                }
            )

        normalized_domains = self.base._normalize_domains(domains)
        items = self.base._normalize_constraints(constraints, normalized_domains)
        counts = {name: 0 for name in normalized_domains}
        for item in items:
            counts[item.variable] += 1
        engine = ConstraintEngine(
            normalized_domains,
            max_constraints_per_variable=max(1, max(counts.values(), default=0)),
        )

        unsat_variables = sorted(
            name
            for name, values in base["original"]["final_domains"].items()
            if not values
        )
        families: dict[str, dict] = {}
        subset_checks = 0
        total_cores = 0
        gaps: list[str] = []

        for variable in unsat_variables:
            variable_items = tuple(item for item in items if item.variable == variable)
            minimum_cores: list[tuple[Constraint, ...]] = []
            for size in range(1, len(variable_items) + 1):
                for subset in combinations(variable_items, size):
                    subset_checks += 1
                    if not engine._remaining(variable, subset):
                        minimum_cores.append(subset)
                if minimum_cores:
                    break

            if not minimum_cores:
                raise FreezeError(f"unable to enumerate an unsat core for {variable}")

            total_cores += len(minimum_cores)
            if len(minimum_cores) > contract.max_cores_per_variable:
                gaps.append(f"PER_VARIABLE_CORE_BUDGET_EXCEEDED:{variable}")
            if total_cores > contract.max_total_cores:
                gaps.append("TOTAL_CORE_BUDGET_EXCEEDED")

            family_cores = []
            for core in minimum_cores:
                core_ids = [item.cid for item in core]
                deletion_witnesses = []
                for removed in core:
                    remainder = tuple(item for item in core if item.cid != removed.cid)
                    remaining_domain = list(engine._remaining(variable, remainder))
                    if not remaining_domain:
                        raise FreezeError("minimum core lacks a satisfiable deletion witness")
                    deletion_witnesses.append(
                        {"removed": removed.cid, "remaining_domain": remaining_domain}
                    )
                family_cores.append(
                    {"core_ids": core_ids, "deletion_witnesses": deletion_witnesses}
                )
            families[variable] = {
                "minimum_core_size": len(minimum_cores[0]),
                "cores": family_cores,
            }

        if gaps:
            coverage = {"unsat_variables": unsat_variables, "conflict_families": {}}
            return self._result(
                {
                    "status": "FREEZE",
                    "reason": "CONFLICT_COVERAGE_BUDGET_EXCEEDED",
                    "gaps": sorted(set(gaps)),
                    **common,
                    **coverage,
                    "discovered_core_count": total_cores,
                    "subset_checks_executed": subset_checks,
                    "coverage_hash": stable_hash(coverage),
                }
            )

        coverage = {
            "unsat_variables": unsat_variables,
            "conflict_families": families,
        }
        return self._result(
            {
                "status": "UNSAT",
                "reason": "EXHAUSTIVE_MINIMUM_CONFLICT_COVERAGE",
                "gaps": [],
                **common,
                **coverage,
                "discovered_core_count": total_cores,
                "subset_checks_executed": subset_checks,
                "coverage_hash": stable_hash(coverage),
            }
        )
