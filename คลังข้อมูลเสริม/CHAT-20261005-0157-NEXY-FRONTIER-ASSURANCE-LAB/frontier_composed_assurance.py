"""Fail-closed composition of the five hardened frontier assurance adapters.

AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from frontier_assurance_lab import (
    Constraint,
    EffectSpec,
    FreezeError,
    RecoveryPolicy,
    TelemetryEventSpec,
    stable_hash,
)
from ghostedge_campaign_assurance import (
    CampaignExperiment,
    GhostedgeCampaignAssurance,
    PerturbationCampaignContract,
)
from muscle_input_assurance import MuscleInputAssurance, MuscleSearchBudget
from obsure_runtime_assurance import (
    EffectRunExpectation,
    RuntimeEvent,
)
from obsure_trace_cohesion import (
    ObsureTraceCohesionAssurance,
    TraceCohesionContract,
)
from parex_metric_integrity import (
    AttestedPlan,
    MetricIntegrityPruner,
    ParexMetricContract,
)
from recert_path_integrity import PointerRecoveryPolicy, RecertPathIntegrityAssurance


class ComposedFrontierAssurancePipeline:
    """Admit a proposal only after every hardened adapter passes in fixed order."""

    def __init__(self) -> None:
        self.muscle = MuscleInputAssurance()
        self.parex = MetricIntegrityPruner()
        self.ghostedge = GhostedgeCampaignAssurance()
        self.recert = RecertPathIntegrityAssurance()
        self.obsure = ObsureTraceCohesionAssurance()

    @staticmethod
    def _result(
        status: str,
        reasons: list[str],
        completed_gates: list[str],
        gates: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        result: dict[str, Any] = {
            "status": status,
            "reasons": reasons,
            "completed_gates": completed_gates,
            "gates": gates,
        }
        result["result_hash"] = stable_hash(result)
        return result

    @classmethod
    def _freeze(
        cls,
        reason: str,
        completed_gates: list[str],
        gates: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        return cls._result("FREEZE", [reason], completed_gates, gates)

    @staticmethod
    def _rejection(error: FreezeError) -> dict[str, Any]:
        return {
            "status": "FREEZE",
            "error_type": type(error).__name__,
            "error": str(error),
        }

    @staticmethod
    def _finite_sequence(name: str, value: object, member_type: type) -> list | tuple:
        if type(value) not in (list, tuple):
            raise FreezeError(f"{name} must be a finite built-in list or tuple")
        if any(not isinstance(item, member_type) for item in value):
            raise FreezeError(f"{name} contains an invalid value")
        return value

    def assess(
        self,
        *,
        domains: Mapping[str, tuple[str, ...]],
        constraints: list[Constraint] | tuple[Constraint, ...],
        muscle_budget: MuscleSearchBudget,
        metric_contract: ParexMetricContract,
        plans: Iterable[AttestedPlan],
        campaign_contract: PerturbationCampaignContract,
        campaign_experiments: Iterable[CampaignExperiment],
        declared_dependencies: Mapping[str, Iterable[str]],
        before_state: Mapping[str, Any],
        after_state: Mapping[str, Any],
        recovery_policy: RecoveryPolicy,
        pointer_policy: PointerRecoveryPolicy,
        trace_contract: TraceCohesionContract,
        effects: Iterable[EffectSpec],
        telemetry_schemas: Iterable[TelemetryEventSpec],
        runtime_expectations: Iterable[EffectRunExpectation],
        runtime_events: Iterable[RuntimeEvent],
    ) -> dict[str, Any]:
        gates: dict[str, dict[str, Any]] = {}
        completed: list[str] = []

        try:
            gates["muscle"] = self.muscle.solve(domains, constraints, muscle_budget)
        except FreezeError as error:
            gates["muscle"] = self._rejection(error)
            completed.append("MUSCLE")
            return self._freeze("MUSCLE_INPUT_REJECTED", completed, gates)
        completed.append("MUSCLE")
        if gates["muscle"]["status"] == "UNSAT":
            return self._freeze("UNSAT_CONSTRAINTS", completed, gates)
        if gates["muscle"]["status"] != "SAT":
            return self._freeze("MUSCLE_BUDGET_EXCEEDED", completed, gates)

        try:
            plan_items = self._finite_sequence("plans", plans, AttestedPlan)
            gates["parex"] = self.parex.prune(metric_contract, plan_items)
        except FreezeError as error:
            gates["parex"] = self._rejection(error)
            completed.append("PAREX")
            return self._freeze("PAREX_INPUT_REJECTED", completed, gates)
        completed.append("PAREX")
        if gates["parex"]["status"] != "PASS":
            return self._freeze("NO_ELIGIBLE_PLAN", completed, gates)

        try:
            campaign_items = self._finite_sequence(
                "campaign_experiments", campaign_experiments, CampaignExperiment
            )
            gates["ghostedge"] = self.ghostedge.assess(
                campaign_contract, campaign_items, declared_dependencies
            )
        except FreezeError as error:
            gates["ghostedge"] = self._rejection(error)
            completed.append("GHOSTEDGE")
            return self._freeze("GHOSTEDGE_INPUT_REJECTED", completed, gates)
        completed.append("GHOSTEDGE")
        if gates["ghostedge"]["status"] == "CANDIDATES_FOUND":
            return self._freeze("UNDECLARED_DEPENDENCY", completed, gates)
        if gates["ghostedge"]["status"] != "CLEAN":
            reason = (
                "CAMPAIGN_INSUFFICIENT_OR_INVALID"
                if gates["ghostedge"]["reason"] == "INSUFFICIENT_OR_INVALID_CAMPAIGN"
                else "UNCONTROLLED_DEPENDENCY_SIGNAL"
            )
            return self._freeze(reason, completed, gates)

        try:
            gates["recert"] = self.recert.assess(
                before_state, after_state, recovery_policy, pointer_policy
            )
        except FreezeError as error:
            gates["recert"] = self._rejection(error)
            completed.append("RECERT")
            return self._freeze("RECERT_INPUT_REJECTED", completed, gates)
        completed.append("RECERT")
        if gates["recert"]["status"] != "CERTIFIED":
            return self._freeze("RECOVERY_NOT_EQUIVALENT", completed, gates)

        try:
            effect_items = self._finite_sequence("effects", effects, EffectSpec)
            schema_items = self._finite_sequence(
                "telemetry_schemas", telemetry_schemas, TelemetryEventSpec
            )
            expectation_items = self._finite_sequence(
                "runtime_expectations", runtime_expectations, EffectRunExpectation
            )
            runtime_items = self._finite_sequence(
                "runtime_events", runtime_events, RuntimeEvent
            )
            gates["obsure"] = self.obsure.assess(
                trace_contract,
                effect_items,
                schema_items,
                expectation_items,
                runtime_items,
            )
        except FreezeError as error:
            gates["obsure"] = self._rejection(error)
            completed.append("OBSURE")
            return self._freeze("OBSURE_INPUT_REJECTED", completed, gates)
        completed.append("OBSURE")
        if gates["obsure"]["status"] != "CERTIFIED":
            reason = gates["obsure"]["reason"]
            if reason == "BASE_RUNTIME_INVALID":
                reason = gates["obsure"]["base"]["reason"]
            return self._freeze(reason, completed, gates)

        return self._result("READY", [], completed, gates)
