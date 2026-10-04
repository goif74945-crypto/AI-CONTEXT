import unittest

from nexy_vam.assumption_planner import Assumption, Experiment, plan_experiments


class AssumptionPlannerTests(unittest.TestCase):
    def setUp(self):
        self.assumptions = [
            Assumption("A", impact=1.0, uncertainty=1.0),
            Assumption("B", impact=0.8, uncertainty=0.5),
            Assumption("C", impact=0.2, uncertainty=0.5),
        ]

    def test_prefers_high_risk_reduction_per_cost(self):
        experiments = [
            Experiment("cheap-A", frozenset({"A"}), cost=1.0),
            Experiment("expensive-AB", frozenset({"A", "B"}), cost=5.0),
            Experiment("cheap-C", frozenset({"C"}), cost=0.5),
        ]
        plan = plan_experiments(self.assumptions, experiments, budget=1.0)
        self.assertEqual([x.experiment_id for x in plan.selected], ["cheap-A"])
        self.assertEqual(plan.remaining_assumptions, ("B", "C"))

    def test_can_chain_with_budget(self):
        experiments = [
            Experiment("A", frozenset({"A"}), cost=1.0),
            Experiment("B", frozenset({"B"}), cost=1.0),
            Experiment("C", frozenset({"C"}), cost=1.0),
        ]
        plan = plan_experiments(self.assumptions, experiments, budget=2.0)
        self.assertEqual([x.experiment_id for x in plan.selected], ["A", "B"])
        self.assertEqual(plan.remaining_assumptions, ("C",))

    def test_execution_risk_penalizes_utility(self):
        experiments = [
            Experiment("safe", frozenset({"B"}), cost=1.0, execution_risk=0.0),
            Experiment("risky", frozenset({"B"}), cost=1.0, execution_risk=1.0),
        ]
        plan = plan_experiments(self.assumptions, experiments, budget=1.0)
        self.assertEqual(plan.selected[0].experiment_id, "safe")

    def test_generator_input_and_duplicate_guard(self):
        assumptions = (item for item in self.assumptions)
        plan = plan_experiments(
            assumptions,
            [Experiment("A", frozenset({"A"}), cost=1.0)],
            budget=1.0,
        )
        self.assertEqual(plan.selected[0].experiment_id, "A")

        with self.assertRaises(ValueError):
            plan_experiments(
                [Assumption("dup", 1.0, 1.0), Assumption("dup", 0.5, 0.5)],
                [Experiment("probe", frozenset({"dup"}), cost=1.0)],
                budget=1.0,
            )

    def test_unknown_assumption_reference_is_rejected(self):
        with self.assertRaises(ValueError):
            plan_experiments(
                self.assumptions,
                [Experiment("bad", frozenset({"MISSING"}), cost=1.0)],
                budget=1.0,
            )


from nexy_vam.behavioral_canary import CanaryCase, record_baseline, verify_canaries


class BehavioralCanaryTests(unittest.TestCase):
    def setUp(self):
        self.cases = [
            CanaryCase("freeze-empty", {"text": ""}),
            CanaryCase("echo", {"text": "abc"}),
        ]

    @staticmethod
    def adapter_v1(request):
        return {"status": "FREEZE" if not request["text"] else "PASS", "value": request["text"]}

    def test_same_behavior_passes(self):
        baseline = record_baseline(self.cases, self.adapter_v1)
        result = verify_canaries(self.cases, self.adapter_v1, baseline)
        self.assertEqual(result.status, "PASS")

    def test_behavior_change_detects_drift(self):
        baseline = record_baseline(self.cases, self.adapter_v1)

        def adapter_v2(request):
            return {"status": "PASS", "value": request["text"]}

        result = verify_canaries(self.cases, adapter_v2, baseline)
        self.assertEqual(result.status, "DRIFT")
        self.assertEqual(
            {w.case_id for w in result.witnesses if w.status == "DRIFT"},
            {"freeze-empty"},
        )

    def test_ignored_nondeterministic_field(self):
        baseline = record_baseline(
            self.cases,
            lambda req: {**self.adapter_v1(req), "trace_id": "old"},
            ignored_top_level_fields=frozenset({"trace_id"}),
        )
        result = verify_canaries(
            self.cases,
            lambda req: {**self.adapter_v1(req), "trace_id": "new"},
            baseline,
        )
        self.assertEqual(result.status, "PASS")

    def test_ignore_rule_does_not_hide_nested_drift(self):
        cases = [CanaryCase("nested", {})]
        baseline = record_baseline(
            cases,
            lambda _req: {"trace_id": "top-old", "nested": {"trace_id": "nested-old"}},
            ignored_top_level_fields=frozenset({"trace_id"}),
        )
        result = verify_canaries(
            cases,
            lambda _req: {"trace_id": "top-new", "nested": {"trace_id": "nested-new"}},
            baseline,
        )
        self.assertEqual(result.status, "DRIFT")


from nexy_vam.correlated_evidence import EvidenceItem, EvidenceRequirement, assess_evidence


class CorrelatedEvidenceTests(unittest.TestCase):
    def test_shared_root_counts_once(self):
        evidence = [
            EvidenceItem("e1", "c", frozenset({"doc-A"}), 0.9),
            EvidenceItem("e2", "c", frozenset({"doc-A", "model-X"}), 0.8),
            EvidenceItem("e3", "c", frozenset({"independent-lab"}), 0.7),
        ]
        result = assess_evidence("c", evidence, EvidenceRequirement(2, 1.5))
        self.assertEqual(result.status, "PASS")
        self.assertEqual(len(result.independent_clusters), 2)
        self.assertAlmostEqual(result.effective_weight, 1.6)

    def test_correlated_votes_freeze(self):
        evidence = [
            EvidenceItem("e1", "c", frozenset({"same"}), 1.0),
            EvidenceItem("e2", "c", frozenset({"same"}), 1.0),
            EvidenceItem("e3", "c", frozenset({"same"}), 1.0),
        ]
        result = assess_evidence("c", evidence)
        self.assertEqual(result.status, "FREEZE")
        self.assertEqual(len(result.independent_clusters), 1)
        self.assertEqual(result.effective_weight, 1.0)

    def test_empty_evidence_freezes(self):
        result = assess_evidence("c", [])
        self.assertEqual(result.status, "FREEZE")
        self.assertIn("no evidence", result.reasons[0])


from nexy_vam.counterexample import minimize_sequence


class CounterexampleTests(unittest.TestCase):
    def test_minimizes_cross_chunk_failure(self):
        original = ["noise1", "A", "noise2", "B", "noise3"]
        result = minimize_sequence(original, lambda seq: "A" in seq and "B" in seq)
        self.assertEqual(result.minimized, ("A", "B"))
        self.assertGreater(result.evaluations, 0)

    def test_single_trigger(self):
        result = minimize_sequence([1, 2, 99, 3, 4], lambda seq: 99 in seq)
        self.assertEqual(result.minimized, (99,))

    def test_rejects_non_failing_input(self):
        with self.assertRaises(ValueError):
            minimize_sequence([1, 2, 3], lambda seq: 99 in seq)


from nexy_vam.metamorphic import MetamorphicRelation, verify_metamorphic


class MeshIntegrationTests(unittest.TestCase):
    def test_drift_to_counterexample_to_epistemic_plan(self):
        cases = [CanaryCase("empty", []), CanaryCase("ordered", ["A", "B", "C"])]

        def stable_adapter(values):
            return {"status": "FREEZE" if not values else "PASS", "value": sorted(values)}

        baseline = record_baseline(cases, stable_adapter)

        def candidate_adapter(values):
            return {"status": "PASS", "value": list(values)}

        canary = verify_canaries(cases, candidate_adapter, baseline)
        self.assertEqual(canary.status, "DRIFT")

        relation = MetamorphicRelation(
            "permutation-invariance",
            lambda values: list(reversed(values)),
            lambda _a, _b, out_a, out_b: out_a["value"] == out_b["value"],
        )
        meta = verify_metamorphic(candidate_adapter, ["A", "B", "C"], [relation])
        self.assertEqual(meta.status, "FAIL")

        def reproduces(values):
            return verify_metamorphic(candidate_adapter, list(values), [relation]).status == "FAIL"

        minimized = minimize_sequence(["noise", "A", "B", "C"], reproduces)
        self.assertEqual(len(minimized.minimized), 2)
        self.assertNotEqual(minimized.minimized[0], minimized.minimized[1])

        evidence = [
            EvidenceItem("agent-1", "order-bug", frozenset({"same-run"}), 0.95),
            EvidenceItem("agent-2", "order-bug", frozenset({"same-run"}), 0.95),
        ]
        assessment = assess_evidence(
            "order-bug",
            evidence,
            EvidenceRequirement(minimum_independent_clusters=2, minimum_effective_weight=1.5),
        )
        self.assertEqual(assessment.status, "FREEZE")

        plan = plan_experiments(
            [Assumption("independent-reproduction", impact=1.0, uncertainty=1.0)],
            [
                Experiment(
                    "rerun-independent-harness",
                    frozenset({"independent-reproduction"}),
                    cost=1.0,
                    execution_risk=0.0,
                    confidence=0.95,
                )
            ],
            budget=1.0,
        )
        self.assertEqual(plan.selected[0].experiment_id, "rerun-independent-harness")


class MetamorphicTests(unittest.TestCase):
    def test_permutation_invariant_system_passes(self):
        sut = lambda values: tuple(sorted(set(values)))
        relation = MetamorphicRelation(
            "permute",
            lambda values: list(reversed(values)),
            lambda _a, _b, out_a, out_b: out_a == out_b,
            "set normalization must ignore order",
        )
        result = verify_metamorphic(sut, [3, 1, 2, 1], [relation])
        self.assertEqual(result.status, "PASS")

    def test_order_sensitive_bug_fails(self):
        sut = lambda values: tuple(values)
        relation = MetamorphicRelation(
            "permute",
            lambda values: list(reversed(values)),
            lambda _a, _b, out_a, out_b: out_a == out_b,
        )
        result = verify_metamorphic(sut, [1, 2, 3], [relation])
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.witnesses[0].status, "FAIL")

    def test_relation_exception_is_failure_evidence(self):
        relation = MetamorphicRelation(
            "boom",
            lambda value: value,
            lambda *_args: (_ for _ in ()).throw(RuntimeError("bad relation")),
        )
        result = verify_metamorphic(lambda x: x, 1, [relation])
        self.assertEqual(result.status, "FAIL")
        self.assertIn("RuntimeError", result.witnesses[0].detail)

    def test_base_execution_exception_is_captured(self):
        relation = MetamorphicRelation("id", lambda x: x, lambda *_: True)
        result = verify_metamorphic(
            lambda _x: (_ for _ in ()).throw(ValueError("sut failed")),
            1,
            [relation],
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("base execution raised ValueError", result.witnesses[0].detail)


if __name__ == "__main__":
    unittest.main()
