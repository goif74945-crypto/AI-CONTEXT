import importlib
import math
import random
import unittest

from frontier_assurance_lab import (
    Constraint,
    EffectSpec,
    FrontierAssurancePipeline,
    PerturbationExperiment,
    Plan,
    RecoveryPolicy,
    TelemetryEventSpec,
)
from ghostedge_campaign_assurance import CampaignExperiment, PerturbationCampaignContract
from muscle_input_assurance import MuscleSearchBudget
from muscle_conflict_coverage import ConflictCoverageContract
from obsure_runtime_assurance import EffectRunExpectation, RuntimeEvent
from obsure_trace_cohesion import TraceCohesionContract
from parex_metric_integrity import AttestedPlan, MetricAxis, ParexMetricContract
from recert_attestation_binding import RecoveryAttestationContract
from recert_path_integrity import PointerRecoveryPolicy


BASE_FIELDS = ("trace_id", "action_id", "effect_id", "timestamp")


def api(testcase):
    try:
        return importlib.import_module("frontier_composed_assurance")
    except ModuleNotFoundError:
        testcase.fail("frontier_composed_assurance implementation is missing")


def metric_contract():
    axes = (
        MetricAxis("benefit", "MAX", "benefit_point", 0, 100),
        MetricAxis("evidence", "MAX", "evidence_point", 0, 100),
        MetricAxis("cost", "MIN", "cost_point", 0, 100),
        MetricAxis("latency", "MIN", "millisecond", 0, 10000),
        MetricAxis("risk", "MIN", "risk_point", 0, 100),
    )
    return ParexMetricContract("profile-v1", "a" * 64, axes)


def attested_plan(contract, pid="safe", values=(10, 10, 3, 4, 1), eligible=True):
    return AttestedPlan(
        pid,
        contract.profile_hash(),
        *values,
        tuple(
            (axis, f"evidence://{pid}/{axis}")
            for axis in ("benefit", "evidence", "cost", "latency", "risk")
        ),
        eligible,
    )


def telemetry_schemas():
    return [
        TelemetryEventSpec(f"write-{phase.lower()}", "write", phase, BASE_FIELDS)
        for phase in ("INTENT", "START", "SUCCESS", "FAILURE")
    ]


def runtime_events(phases=("INTENT", "START", "SUCCESS"), action="action-1"):
    values = {
        "trace_id": "trace-1",
        "action_id": action,
        "effect_id": "write",
        "timestamp": "logical-time",
    }
    return [
        RuntimeEvent(f"write-{phase.lower()}", "write", index, values)
        for index, phase in enumerate(phases)
    ]


def base_request():
    contract = metric_contract()
    return {
        "domains": {"mode": ("safe", "fast")},
        "constraints": [Constraint("c1", "mode", "EQ", ("safe",))],
        "muscle_budget": MuscleSearchBudget(),
        "conflict_coverage_contract": ConflictCoverageContract(),
        "metric_contract": contract,
        "plans": [
            attested_plan(contract),
            attested_plan(contract, "worse", (5, 5, 8, 8, 3)),
        ],
        "campaign_contract": PerturbationCampaignContract(
            {"vault": ("judge",)}, min_interventions_per_source=2, min_shams=2
        ),
        "campaign_experiments": [
            CampaignExperiment("i1", "INTERVENTION", "vault", ("judge",), ()),
            CampaignExperiment("i2", "INTERVENTION", "vault", ("judge",), ()),
            CampaignExperiment("s1", "SHAM", None, ("judge",), ()),
            CampaignExperiment("s2", "SHAM", None, ("judge",), ()),
        ],
        "declared_dependencies": {"judge": ()},
        "before_state": {"law": {"epoch": 7}},
        "after_state": {"law": {"epoch": 7}},
        "recovery_policy": RecoveryPolicy(),
        "pointer_policy": PointerRecoveryPolicy(),
        "recovery_attestation": RecoveryAttestationContract(
            "attestation-1", "incident-1", "before-rev", "after-rev"
        ),
        "effects": [EffectSpec("write", "LOW", False)],
        "telemetry_schemas": telemetry_schemas(),
        "runtime_expectations": [EffectRunExpectation("write", "SUCCESS")],
        "runtime_events": runtime_events(),
        "trace_contract": TraceCohesionContract(
            "trace-1", "action-1", {"write": ()}
        ),
    }


class ComposedAssurancePositiveTests(unittest.TestCase):
    def test_ready_requires_all_five_hardened_gates(self):
        result = api(self).ComposedFrontierAssurancePipeline().assess(**base_request())
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["completed_gates"], [
            "MUSCLE", "PAREX", "GHOSTEDGE", "RECERT", "OBSURE"
        ])
        self.assertEqual(result["reasons"], [])
        self.assertEqual(result["gates"]["obsure"]["status"], "CERTIFIED")
        self.assertRegex(result["result_hash"], r"^[0-9a-f]{64}$")

    def test_valid_composition_preserves_hardened_gate_bindings(self):
        request = base_request()
        result = api(self).ComposedFrontierAssurancePipeline().assess(**request)
        self.assertEqual(
            result["gates"]["parex"]["metric_profile_hash"],
            request["metric_contract"].profile_hash(),
        )
        self.assertRegex(result["gates"]["muscle"]["input_hash"], r"^[0-9a-f]{64}$")
        self.assertEqual(result["gates"]["ghostedge"]["controlled"]["gaps"], [])


class ComposedAssuranceNegativeTests(unittest.TestCase):
    def setUp(self):
        self.pipeline = api(self).ComposedFrontierAssurancePipeline()

    def assert_freeze(self, request, reason, final_gate):
        result = self.pipeline.assess(**request)
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reasons"], [reason])
        self.assertEqual(result["completed_gates"][-1], final_gate)
        return result

    def test_unsat_constraints_freeze_at_muscle(self):
        request = base_request()
        request["constraints"] = [
            Constraint("a", "mode", "EQ", ("safe",)),
            Constraint("b", "mode", "EQ", ("fast",)),
        ]
        result = self.assert_freeze(request, "UNSAT_CONSTRAINTS", "MUSCLE")
        self.assertEqual(
            result["gates"]["muscle"]["reason"],
            "EXHAUSTIVE_MINIMUM_CONFLICT_COVERAGE",
        )

    def test_independent_unsat_variables_are_all_covered_at_muscle(self):
        request = base_request()
        request["domains"] = {"a": ("safe", "fast"), "b": ("on", "off")}
        request["constraints"] = [
            Constraint("a-fast", "a", "EQ", ("fast",)),
            Constraint("a-safe", "a", "EQ", ("safe",)),
            Constraint("b-off", "b", "EQ", ("off",)),
            Constraint("b-on", "b", "EQ", ("on",)),
        ]
        result = self.assert_freeze(request, "UNSAT_CONSTRAINTS", "MUSCLE")
        self.assertEqual(result["gates"]["muscle"]["unsat_variables"], ["a", "b"])
        self.assertEqual(set(result["gates"]["muscle"]["conflict_families"]), {"a", "b"})

    def test_conflict_coverage_budget_freezes_at_muscle(self):
        request = base_request()
        request["constraints"] = [
            Constraint("deny-fast", "mode", "DENY", ("fast",)),
            Constraint("deny-safe", "mode", "DENY", ("safe",)),
            Constraint("eq-fast", "mode", "EQ", ("fast",)),
            Constraint("eq-safe", "mode", "EQ", ("safe",)),
        ]
        request["conflict_coverage_contract"] = ConflictCoverageContract(
            max_cores_per_variable=3,
            max_total_cores=128,
        )
        self.assert_freeze(
            request,
            "MUSCLE_CONFLICT_COVERAGE_BUDGET_EXCEEDED",
            "MUSCLE",
        )

    def test_no_eligible_plan_freezes_at_parex(self):
        request = base_request()
        request["plans"] = [attested_plan(request["metric_contract"], eligible=False)]
        self.assert_freeze(request, "NO_ELIGIBLE_PLAN", "PAREX")

    def test_controlled_hidden_dependency_freezes_at_ghostedge(self):
        request = base_request()
        request["campaign_experiments"] = [
            CampaignExperiment("i1", "INTERVENTION", "vault", ("judge",), ("judge",)),
            CampaignExperiment("i2", "INTERVENTION", "vault", ("judge",), ("judge",)),
            CampaignExperiment("s1", "SHAM", None, ("judge",), ()),
            CampaignExperiment("s2", "SHAM", None, ("judge",), ()),
        ]
        self.assert_freeze(request, "UNDECLARED_DEPENDENCY", "GHOSTEDGE")

    def test_recovery_mismatch_freezes_at_recert(self):
        request = base_request()
        request["after_state"] = {"law": {"epoch": 6}}
        self.assert_freeze(request, "RECOVERY_NOT_EQUIVALENT", "RECERT")

    def test_missing_runtime_phase_freezes_at_obsure(self):
        request = base_request()
        request["runtime_events"] = runtime_events(("INTENT", "SUCCESS"))
        self.assert_freeze(request, "RUNTIME_WITNESS_INVALID", "OBSURE")


class ComposedAssuranceAdversarialTests(unittest.TestCase):
    def test_original_pipeline_ready_on_unknown_literal_but_composed_freezes(self):
        original = FrontierAssurancePipeline({"mode": ("safe", "fast")}).assess(
            constraints=[Constraint("typo", "mode", "NEQ", ("saef",))],
            plans=[Plan("safe", 10, 10, 3, 4, 1)],
            experiments=[
                PerturbationExperiment("i1", "vault", ("judge",), ()),
                PerturbationExperiment("i2", "vault", ("judge",), ()),
            ],
            declared_dependencies={"judge": ()},
            before_state={"law": {"epoch": 7}},
            after_state={"law": {"epoch": 7}},
            recovery_policy=RecoveryPolicy(),
            effects=[EffectSpec("write", "LOW", False)],
            telemetry=telemetry_schemas(),
        )
        self.assertEqual(original["status"], "READY")

        request = base_request()
        request["constraints"] = [Constraint("typo", "mode", "NEQ", ("saef",))]
        result = api(self).ComposedFrontierAssurancePipeline().assess(**request)
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reasons"], ["MUSCLE_INPUT_REJECTED"])
        self.assertEqual(result["gates"]["muscle"]["status"], "FREEZE")

    def test_nan_metric_is_captured_as_fail_closed_pipeline_result(self):
        request = base_request()
        contract = request["metric_contract"]
        bad = attested_plan(contract)
        object.__setattr__(bad, "benefit", math.nan)
        request["plans"] = [bad]
        result = api(self).ComposedFrontierAssurancePipeline().assess(**request)
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reasons"], ["PAREX_INPUT_REJECTED"])

    def test_empty_campaign_cannot_reach_ready(self):
        request = base_request()
        request["campaign_experiments"] = []
        self.assertEqual(
            api(self).ComposedFrontierAssurancePipeline().assess(**request)["reasons"],
            ["CAMPAIGN_INSUFFICIENT_OR_INVALID"],
        )

    def test_dotted_path_alias_cannot_reach_ready(self):
        request = base_request()
        request["before_state"] = {"a": {"b": 1}, "a.b": 9}
        request["after_state"] = {"a": {"b": 2}, "a.b": 9}
        result = api(self).ComposedFrontierAssurancePipeline().assess(**request)
        self.assertEqual(result["reasons"], ["RECOVERY_NOT_EQUIVALENT"])
        self.assertEqual(result["gates"]["recert"]["original"]["status"], "CERTIFIED")

    def test_permutations_are_deterministic(self):
        pipeline = api(self).ComposedFrontierAssurancePipeline()
        baseline = pipeline.assess(**base_request())
        rng = random.Random(74945)
        for _ in range(50):
            request = base_request()
            for key in (
                "constraints", "plans", "campaign_experiments", "telemetry_schemas", "runtime_events"
            ):
                rng.shuffle(request[key])
            self.assertEqual(pipeline.assess(**request), baseline)

    def test_plan_generator_is_rejected_before_materialization(self):
        request = base_request()
        request["plans"] = (item for item in request["plans"])
        result = api(self).ComposedFrontierAssurancePipeline().assess(**request)
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reasons"], ["PAREX_INPUT_REJECTED"])
        self.assertIn("finite built-in list or tuple", result["gates"]["parex"]["error"])

    def test_foreign_campaign_element_is_structured_rejection(self):
        request = base_request()
        request["campaign_experiments"] = [object()]
        result = api(self).ComposedFrontierAssurancePipeline().assess(**request)
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reasons"], ["GHOSTEDGE_INPUT_REJECTED"])

    def test_runtime_generator_is_rejected_before_materialization(self):
        request = base_request()
        request["runtime_events"] = (item for item in request["runtime_events"])
        result = api(self).ComposedFrontierAssurancePipeline().assess(**request)
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reasons"], ["OBSURE_INPUT_REJECTED"])


class ComposedAssuranceIntegrationTests(unittest.TestCase):
    def test_ready_result_includes_trace_cohesion_binding(self):
        result = api(self).ComposedFrontierAssurancePipeline().assess(**base_request())
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["gates"]["obsure"]["reason"], "TRACE_COHESIVE")
        self.assertRegex(result["gates"]["obsure"]["contract_hash"], r"^[0-9a-f]{64}$")

    def test_ready_result_includes_recovery_attestation_binding(self):
        result = api(self).ComposedFrontierAssurancePipeline().assess(**base_request())
        self.assertEqual(result["status"], "READY")
        self.assertRegex(result["gates"]["recert"]["binding_hash"], r"^[0-9a-f]{64}$")
        self.assertRegex(result["gates"]["recert"]["before_state_hash"], r"^[0-9a-f]{64}$")
        self.assertRegex(result["gates"]["recert"]["pointer_policy_hash"], r"^[0-9a-f]{64}$")

    def test_passing_recovery_state_change_changes_pipeline_certificate(self):
        first_request = base_request()
        second_request = base_request()
        second_request["before_state"] = {"law": {"epoch": 8}}
        second_request["after_state"] = {"law": {"epoch": 8}}
        first = api(self).ComposedFrontierAssurancePipeline().assess(**first_request)
        second = api(self).ComposedFrontierAssurancePipeline().assess(**second_request)
        self.assertEqual(first["status"], "READY")
        self.assertEqual(second["status"], "READY")
        self.assertEqual(
            first["gates"]["recert"]["base_result_hash"],
            second["gates"]["recert"]["base_result_hash"],
        )
        self.assertNotEqual(
            first["gates"]["recert"]["binding_hash"],
            second["gates"]["recert"]["binding_hash"],
        )
        self.assertNotEqual(first["result_hash"], second["result_hash"])

    def test_spliced_action_identity_freezes_composed_pipeline(self):
        request = base_request()
        request["runtime_events"] = runtime_events(action="action-2")
        result = api(self).ComposedFrontierAssurancePipeline().assess(**request)
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reasons"], ["TRACE_COHESION_INVALID"])

    def test_short_circuit_does_not_claim_unexecuted_gates(self):
        request = base_request()
        request["constraints"] = [Constraint("bad", "mode", "NEQ", ("typo",))]
        result = api(self).ComposedFrontierAssurancePipeline().assess(**request)
        self.assertEqual(result["completed_gates"], ["MUSCLE"])
        self.assertEqual(set(result["gates"]), {"muscle"})

    def test_pipeline_captures_adapter_rejection_without_exception_escape(self):
        request = base_request()
        request["constraints"] = (item for item in request["constraints"])
        result = api(self).ComposedFrontierAssurancePipeline().assess(**request)
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reasons"], ["MUSCLE_INPUT_REJECTED"])
        self.assertIn("finite built-in list or tuple", result["gates"]["muscle"]["error"])


if __name__ == "__main__":
    unittest.main()
