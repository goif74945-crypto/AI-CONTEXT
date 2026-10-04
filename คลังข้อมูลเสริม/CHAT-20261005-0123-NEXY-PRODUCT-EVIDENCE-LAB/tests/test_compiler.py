import dataclasses
import math
import unittest

from helpers import valid_proposal
from nexy_product_evidence.compiler import compile_experiment
from nexy_product_evidence.errors import ExperimentValidationError
from nexy_product_evidence.model import Direction, GuardrailSpec, MetricKind, MetricSpec
from nexy_product_evidence.serialization import canonical_contract_json, contract_hash


class CompilerTests(unittest.TestCase):
    def test_valid_proposal_compiles(self):
        contract = compile_experiment(valid_proposal())
        self.assertEqual(contract.schema_version, "npel.contract.v1")
        self.assertGreater(contract.planned_sample_per_arm, 0)
        self.assertEqual(contract.authority, "human_product_decision")

    def test_hash_is_deterministic(self):
        a = compile_experiment(valid_proposal())
        b = compile_experiment(valid_proposal())
        self.assertEqual(contract_hash(a), contract_hash(b))
        self.assertEqual(canonical_contract_json(a), canonical_contract_json(b))

    def test_hash_length(self):
        self.assertEqual(len(contract_hash(compile_experiment(valid_proposal()))), 64)

    def assert_issue(self, proposal, code):
        with self.assertRaises(ExperimentValidationError) as ctx:
            compile_experiment(proposal)
        self.assertIn(code, {i.code for i in ctx.exception.issues})

    def test_invalid_id(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), experiment_id="!"), "EXPERIMENT_ID_INVALID")

    def test_title_required(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), title=" "), "TITLE_REQUIRED")

    def test_hypothesis_required(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), hypothesis=""), "HYPOTHESIS_REQUIRED")

    def test_population_required(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), population=""), "POPULATION_REQUIRED")

    def test_guardrail_required(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), guardrails=()), "GUARDRAIL_REQUIRED")

    def test_prohibited_dark_pattern(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), risk_flags=frozenset({"dark_pattern"})), "PROHIBITED_RISK")

    def test_prohibited_privacy_violation(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), risk_flags=frozenset({"privacy_violation"})), "PROHIBITED_RISK")

    def test_allocation_zero_unsupported(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), allocation_fraction=0), "ALLOCATION_UNSUPPORTED")

    def test_allocation_one_unsupported(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), allocation_fraction=1), "ALLOCATION_UNSUPPORTED")

    def test_unequal_allocation_unsupported(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), allocation_fraction=0.3), "ALLOCATION_UNSUPPORTED")

    def test_duration_invalid(self):
        self.assert_issue(dataclasses.replace(valid_proposal(), duration_days=0), "DURATION_INVALID")

    def test_mde_invalid(self):
        p = valid_proposal()
        m = dataclasses.replace(p.primary_metric, mde_abs=0)
        self.assert_issue(dataclasses.replace(p, primary_metric=m), "MDE_INVALID")

    def test_alpha_invalid(self):
        p = valid_proposal()
        m = dataclasses.replace(p.primary_metric, alpha=1)
        self.assert_issue(dataclasses.replace(p, primary_metric=m), "ALPHA_INVALID")

    def test_power_invalid(self):
        p = valid_proposal()
        m = dataclasses.replace(p.primary_metric, power=0.5)
        self.assert_issue(dataclasses.replace(p, primary_metric=m), "POWER_INVALID")

    def test_proportion_baseline_invalid(self):
        p = valid_proposal()
        m = dataclasses.replace(p.primary_metric, baseline=1.0)
        self.assert_issue(dataclasses.replace(p, primary_metric=m), "PROPORTION_BASELINE_INVALID")

    def test_proportion_target_invalid(self):
        p = valid_proposal()
        m = dataclasses.replace(p.primary_metric, baseline=0.98, mde_abs=0.05)
        self.assert_issue(dataclasses.replace(p, primary_metric=m), "PROPORTION_TARGET_INVALID")

    def test_proportion_stddev_forbidden(self):
        p = valid_proposal()
        m = dataclasses.replace(p.primary_metric, planning_stddev=1.0)
        self.assert_issue(dataclasses.replace(p, primary_metric=m), "STDDEV_NOT_ALLOWED")

    def test_mean_stddev_required(self):
        p = valid_proposal()
        m = MetricSpec("latency", MetricKind.MEAN, Direction.LOWER_IS_BETTER, 100, 10, 0.05, 0.8, None)
        self.assert_issue(dataclasses.replace(p, primary_metric=m), "STDDEV_REQUIRED")

    def test_duplicate_guardrail(self):
        p = valid_proposal()
        self.assert_issue(dataclasses.replace(p, guardrails=p.guardrails + p.guardrails), "GUARDRAIL_DUPLICATE")

    def test_negative_guardrail_threshold(self):
        p = valid_proposal()
        g = GuardrailSpec("g", Direction.LOWER_IS_BETTER, 0.1, -0.1)
        self.assert_issue(dataclasses.replace(p, guardrails=(g,)), "GUARDRAIL_THRESHOLD_INVALID")

    def test_nonfinite_baseline(self):
        p = valid_proposal()
        m = dataclasses.replace(p.primary_metric, baseline=math.nan)
        self.assert_issue(dataclasses.replace(p, primary_metric=m), "BASELINE_NOT_FINITE")


if __name__ == "__main__":
    unittest.main()
