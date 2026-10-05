"""Controlled campaign sufficiency extension for experimental GHOSTEDGE.

AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from frontier_assurance_lab import (
    FreezeError,
    HiddenDependencyDetector,
    PerturbationExperiment,
    stable_hash,
)


@dataclass(frozen=True)
class PerturbationCampaignContract:
    expected_observations: Mapping[str, tuple[str, ...]]
    min_interventions_per_source: int = 2
    min_shams: int = 2
    min_lift_milli: int = 500

    def __post_init__(self) -> None:
        if not self.expected_observations:
            raise FreezeError("campaign requires at least one perturbation source")
        for source, targets in self.expected_observations.items():
            if not isinstance(source, str) or not source.strip():
                raise FreezeError("campaign source must be a non-empty string")
            if isinstance(targets, str) or not targets:
                raise FreezeError(f"campaign source {source!r} requires targets")
            if any(not isinstance(target, str) or not target.strip() for target in targets):
                raise FreezeError(f"campaign source {source!r} has invalid target")
            if len(set(targets)) != len(targets):
                raise FreezeError(f"campaign source {source!r} has duplicate targets")
            if source in targets:
                raise FreezeError("campaign targets must be downstream only")
        if (
            isinstance(self.min_interventions_per_source, bool)
            or not isinstance(self.min_interventions_per_source, int)
            or self.min_interventions_per_source < 1
        ):
            raise FreezeError("min_interventions_per_source must be a positive integer")
        if isinstance(self.min_shams, bool) or not isinstance(self.min_shams, int) or self.min_shams < 1:
            raise FreezeError("min_shams must be a positive integer")
        if (
            isinstance(self.min_lift_milli, bool)
            or not isinstance(self.min_lift_milli, int)
            or not 0 <= self.min_lift_milli <= 1000
        ):
            raise FreezeError("min_lift_milli must be an integer from 0 to 1000")


@dataclass(frozen=True)
class CampaignExperiment:
    eid: str
    kind: str
    source: str | None
    observed: tuple[str, ...]
    failed: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            not isinstance(self.eid, str)
            or not self.eid.strip()
            or self.kind not in {"INTERVENTION", "SHAM"}
        ):
            raise FreezeError("invalid campaign experiment identity/kind")
        if self.kind == "INTERVENTION":
            if not isinstance(self.source, str) or not self.source.strip():
                raise FreezeError("intervention requires a perturbation source")
        elif self.source is not None:
            raise FreezeError("sham experiment must not declare a source")
        if isinstance(self.observed, str) or isinstance(self.failed, str):
            raise FreezeError("campaign observed/failed values must be collections")
        if len(set(self.observed)) != len(self.observed):
            raise FreezeError("campaign observed targets must be unique")
        if len(set(self.failed)) != len(self.failed):
            raise FreezeError("campaign failed targets must be unique")
        if any(not isinstance(item, str) or not item.strip() for item in self.observed):
            raise FreezeError("campaign observed target must be a non-empty string")
        if not set(self.failed).issubset(set(self.observed)):
            raise FreezeError("campaign failures must be observed")


class ControlledCampaignDetector:
    def __init__(self, *, min_hits: int = 2, min_ratio_milli: int = 750) -> None:
        if isinstance(min_hits, bool) or not isinstance(min_hits, int) or min_hits < 1:
            raise FreezeError("min_hits must be a positive integer")
        if (
            isinstance(min_ratio_milli, bool)
            or not isinstance(min_ratio_milli, int)
            or not 0 <= min_ratio_milli <= 1000
        ):
            raise FreezeError("min_ratio_milli must be an integer from 0 to 1000")
        self.min_hits = min_hits
        self.min_ratio_milli = min_ratio_milli

    @staticmethod
    def _normalize_declared(
        declared_dependencies: Mapping[str, Iterable[str]],
    ) -> dict[str, set[str]]:
        normalized: dict[str, set[str]] = {}
        for child, parents in declared_dependencies.items():
            if not isinstance(child, str) or not child.strip() or isinstance(parents, str):
                raise FreezeError("invalid declared dependency mapping")
            parent_set = set(parents)
            if any(not isinstance(parent, str) or not parent.strip() for parent in parent_set):
                raise FreezeError("invalid declared dependency parent")
            normalized[child] = parent_set
        return normalized

    def detect(
        self,
        contract: PerturbationCampaignContract,
        experiments: Iterable[CampaignExperiment],
        declared_dependencies: Mapping[str, Iterable[str]],
    ) -> dict:
        items = tuple(sorted(experiments, key=lambda item: item.eid))
        if len({item.eid for item in items}) != len(items):
            raise FreezeError("campaign experiment ids must be unique")

        matrix = {
            source: tuple(sorted(targets))
            for source, targets in sorted(contract.expected_observations.items())
        }
        all_targets = tuple(sorted({target for targets in matrix.values() for target in targets}))
        declared = self._normalize_declared(declared_dependencies)
        interventions = {source: [] for source in matrix}
        shams: list[CampaignExperiment] = []
        gaps: list[dict] = []

        for experiment in items:
            if experiment.kind == "SHAM":
                if tuple(sorted(experiment.observed)) != all_targets:
                    gaps.append(
                        {
                            "code": "SHAM_OBSERVATION_COVERAGE_MISMATCH",
                            "eid": experiment.eid,
                            "expected": list(all_targets),
                            "observed": sorted(experiment.observed),
                        }
                    )
                shams.append(experiment)
                continue

            if experiment.source is None:
                raise FreezeError("intervention source missing after validation")
            if experiment.source not in matrix:
                gaps.append(
                    {
                        "code": "UNKNOWN_PERTURBATION_SOURCE",
                        "eid": experiment.eid,
                        "source": experiment.source,
                    }
                )
                continue
            expected = matrix[experiment.source]
            if tuple(sorted(experiment.observed)) != expected:
                gaps.append(
                    {
                        "code": "INTERVENTION_OBSERVATION_COVERAGE_MISMATCH",
                        "eid": experiment.eid,
                        "source": experiment.source,
                        "expected": list(expected),
                        "observed": sorted(experiment.observed),
                    }
                )
            interventions[experiment.source].append(experiment)

        for source in sorted(matrix):
            count = len(interventions[source])
            if count < contract.min_interventions_per_source:
                gaps.append(
                    {
                        "code": "INSUFFICIENT_INTERVENTIONS",
                        "source": source,
                        "observed": count,
                        "required": contract.min_interventions_per_source,
                    }
                )
        if len(shams) < contract.min_shams:
            gaps.append(
                {
                    "code": "INSUFFICIENT_SHAMS",
                    "observed": len(shams),
                    "required": contract.min_shams,
                }
            )

        gaps = sorted(
            gaps,
            key=lambda gap: (
                gap["code"],
                str(gap.get("source", "")),
                str(gap.get("eid", "")),
            ),
        )
        if gaps:
            result = {"status": "FREEZE", "gaps": gaps, "candidates": []}
            result["result_hash"] = stable_hash(result)
            return result

        sham_hits = {
            target: sum(target in experiment.failed for experiment in shams)
            for target in all_targets
        }
        candidates: list[dict] = []
        diagnostics: list[dict] = []
        for source in sorted(matrix):
            source_experiments = interventions[source]
            for child in matrix[source]:
                hits = sum(child in experiment.failed for experiment in source_experiments)
                opportunities = len(source_experiments)
                control_hits = sham_hits[child]
                control_opportunities = len(shams)
                ratio = (hits * 1000) // opportunities
                control_ratio = (control_hits * 1000) // control_opportunities
                lift = ratio - control_ratio
                row = {
                    "parent": source,
                    "child": child,
                    "hits": hits,
                    "opportunities": opportunities,
                    "ratio_milli": ratio,
                    "sham_hits": control_hits,
                    "sham_opportunities": control_opportunities,
                    "sham_ratio_milli": control_ratio,
                    "lift_milli": lift,
                }
                diagnostics.append(row)
                if source in declared.get(child, set()):
                    continue
                if (
                    hits >= self.min_hits
                    and ratio >= self.min_ratio_milli
                    and lift >= contract.min_lift_milli
                ):
                    candidates.append(
                        {
                            **row,
                            "reason": "CONTROLLED_PERTURBATION_EXCESS_FAILURE_RATE",
                        }
                    )

        result = {
            "status": "CANDIDATES_FOUND" if candidates else "CLEAN",
            "gaps": [],
            "candidates": candidates,
            "diagnostics": diagnostics,
        }
        result["result_hash"] = stable_hash(result)
        return result


class GhostedgeCampaignAssurance:
    """Integrates original GHOSTEDGE with controlled campaign evidence."""

    def __init__(self, *, min_hits: int = 2, min_ratio_milli: int = 750) -> None:
        self.original = HiddenDependencyDetector(
            min_hits=min_hits, min_ratio_milli=min_ratio_milli
        )
        self.controlled = ControlledCampaignDetector(
            min_hits=min_hits, min_ratio_milli=min_ratio_milli
        )

    def assess(
        self,
        contract: PerturbationCampaignContract,
        experiments: Iterable[CampaignExperiment],
        declared_dependencies: Mapping[str, Iterable[str]],
    ) -> dict:
        items = tuple(experiments)
        original_inputs = [
            PerturbationExperiment(
                experiment.eid,
                experiment.source,
                experiment.observed,
                experiment.failed,
            )
            for experiment in items
            if experiment.kind == "INTERVENTION" and experiment.source is not None
        ]
        original = self.original.detect(original_inputs, declared_dependencies)
        controlled = self.controlled.detect(contract, items, declared_dependencies)

        if controlled["status"] == "FREEZE":
            status = "FREEZE"
            reason = "INSUFFICIENT_OR_INVALID_CAMPAIGN"
        elif original["status"] == "CANDIDATES_FOUND" and controlled["status"] == "CLEAN":
            status = "FREEZE"
            reason = "UNCONTROLLED_SIGNAL_REJECTED_BY_SHAM_BASELINE"
        else:
            status = controlled["status"]
            reason = (
                "CONTROLLED_CANDIDATES_FOUND"
                if status == "CANDIDATES_FOUND"
                else "CONTROLLED_CAMPAIGN_CLEAN"
            )

        result = {
            "status": status,
            "reason": reason,
            "original": original,
            "controlled": controlled,
        }
        result["result_hash"] = stable_hash(result)
        return result
