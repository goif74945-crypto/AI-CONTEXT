import dataclasses
import unittest

from helpers import valid_proposal
from nexy_product_evidence.compiler import compile_experiment
from nexy_product_evidence.evaluator import evaluate_experiment
from nexy_product_evidence.model import (
    Direction,
    EvidenceSignal,
    EvaluationEvidence,
    ExperimentProposal,
    GuardrailSpec,
    MetricKind,
    MetricObservation,
    MetricSpec,
)
from nexy_product_evidence.serialization import contract_hash


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.contract = compile_experiment(valid_proposal())
        self.hash = contract_hash(self.contract)
        self.n = self.contract.planned_sample_per_arm

    def evidence(self, treatment=0.50, n=None, guardrail_treatment=0.10):
        n = n or self.n * 4
        return EvaluationEvidence(
            contract_hash=self.hash,
            primary=MetricObservation("completion_rate", 0.40, treatment, n, n),
            guardrails={
                "abandonment_rate": MetricObservation("abandonment_rate", 0.10, guardrail_treatment, n, n)
            },
        )

    def test_supported(self):
        out = evaluate_experiment(self.contract, self.evidence(treatment=0.50))
        self.assertEqual(out.signal, EvidenceSignal.SUPPORTED)
        self.assertTrue(out.human_decision_required)
        self.assertIsNotNone(out.primary_interval)

    def test_rejected_when_interval_below_mde(self):
        out = evaluate_experiment(self.contract, self.evidence(treatment=0.405))
        self.assertEqual(out.signal, EvidenceSignal.REJECTED)

    def test_inconclusive_overlap(self):
        out = evaluate_experiment(self.contract, self.evidence(treatment=0.45, n=self.n))
        self.assertEqual(out.signal, EvidenceSignal.INCONCLUSIVE)

    def test_underpowered(self):
        out = evaluate_experiment(self.contract, self.evidence(treatment=0.60, n=max(1, self.n - 1)))
        self.assertEqual(out.signal, EvidenceSignal.INCONCLUSIVE)
        self.assertIsNone(out.primary_interval)

    def test_hash_mismatch_freezes(self):
        ev = dataclasses.replace(self.evidence(), contract_hash="0" * 64)
        out = evaluate_experiment(self.contract, ev)
        self.assertEqual(out.signal, EvidenceSignal.FREEZE)
        self.assertIn("CONTRACT_HASH_MISMATCH", out.reasons)

    def test_data_quality_freezes(self):
        ev = dataclasses.replace(self.evidence(), data_quality_ok=False)
        self.assertEqual(evaluate_experiment(self.contract, ev).signal, EvidenceSignal.FREEZE)

    def test_invariant_violation_freezes(self):
        ev = dataclasses.replace(self.evidence(), invariant_violations=("sample_ratio_mismatch",))
        out = evaluate_experiment(self.contract, ev)
        self.assertEqual(out.signal, EvidenceSignal.FREEZE)
        self.assertTrue(any(r.startswith("INVARIANT:") for r in out.reasons))

    def test_guardrail_missing_freezes(self):
        ev = dataclasses.replace(self.evidence(), guardrails={})
        self.assertEqual(evaluate_experiment(self.contract, ev).signal, EvidenceSignal.FREEZE)

    def test_guardrail_breach_freezes(self):
        out = evaluate_experiment(self.contract, self.evidence(guardrail_treatment=0.13))
        self.assertEqual(out.signal, EvidenceSignal.FREEZE)
        self.assertTrue(out.reasons[0].startswith("GUARDRAIL_BREACH"))

    def test_guardrail_at_threshold_is_allowed(self):
        out = evaluate_experiment(self.contract, self.evidence(guardrail_treatment=0.12))
        self.assertNotEqual(out.signal, EvidenceSignal.FREEZE)

    def test_primary_name_mismatch(self):
        ev = dataclasses.replace(self.evidence(), primary=MetricObservation("wrong", 0.4, 0.5, self.n*4, self.n*4))
        self.assertEqual(evaluate_experiment(self.contract, ev).signal, EvidenceSignal.FREEZE)

    def test_invalid_primary_sample(self):
        ev = dataclasses.replace(self.evidence(), primary=MetricObservation("completion_rate", 0.4, 0.5, 0, self.n))
        self.assertEqual(evaluate_experiment(self.contract, ev).signal, EvidenceSignal.FREEZE)

    def test_invalid_proportion_value(self):
        ev = dataclasses.replace(self.evidence(), primary=MetricObservation("completion_rate", 0.4, 1.2, self.n, self.n))
        self.assertEqual(evaluate_experiment(self.contract, ev).signal, EvidenceSignal.FREEZE)

    def test_mean_metric_supported_lower_is_better(self):
        proposal = ExperimentProposal(
            experiment_id="latency-exp-001",
            title="Latency reduction",
            hypothesis="Latency drops by at least 10 ms",
            population="Eligible requests in the defined production-like test population",
            primary_metric=MetricSpec("latency_ms", MetricKind.MEAN, Direction.LOWER_IS_BETTER, 100, 10, 0.05, 0.8, 20),
            guardrails=(GuardrailSpec("error_rate", Direction.LOWER_IS_BETTER, 0.01, 0.005),),
            allocation_fraction=0.5,
            duration_days=7,
        )
        contract = compile_experiment(proposal)
        n = contract.planned_sample_per_arm * 4
        ev = EvaluationEvidence(
            contract_hash=contract_hash(contract),
            primary=MetricObservation("latency_ms", 100, 80, n, n, 20, 20),
            guardrails={"error_rate": MetricObservation("error_rate", 0.01, 0.011, n, n)},
        )
        out = evaluate_experiment(contract, ev)
        self.assertEqual(out.signal, EvidenceSignal.SUPPORTED)

    def test_mean_missing_observed_stddev_freezes(self):
        proposal = ExperimentProposal(
            experiment_id="latency-exp-002",
            title="Latency reduction",
            hypothesis="Latency drops by at least 10 ms",
            population="Eligible requests in a stable test population",
            primary_metric=MetricSpec("latency_ms", MetricKind.MEAN, Direction.LOWER_IS_BETTER, 100, 10, 0.05, 0.8, 20),
            guardrails=(GuardrailSpec("error_rate", Direction.LOWER_IS_BETTER, 0.01, 0.005),),
            allocation_fraction=0.5,
            duration_days=7,
        )
        contract = compile_experiment(proposal)
        n = contract.planned_sample_per_arm * 2
        ev = EvaluationEvidence(
            contract_hash=contract_hash(contract),
            primary=MetricObservation("latency_ms", 100, 80, n, n),
            guardrails={"error_rate": MetricObservation("error_rate", 0.01, 0.011, n, n)},
        )
        self.assertEqual(evaluate_experiment(contract, ev).signal, EvidenceSignal.FREEZE)


if __name__ == "__main__":
    unittest.main()
