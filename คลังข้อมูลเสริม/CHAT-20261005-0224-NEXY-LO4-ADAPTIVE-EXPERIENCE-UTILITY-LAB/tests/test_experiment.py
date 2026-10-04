import unittest

from aeul.common import ContractError
from aeul.experiment import ExperimentPolicy, ExperimentProposal, plan_experiment
from aeul.q64 import Q64

q = Q64.from_decimal


def proposal(**overrides):
    data = dict(
        proposal_id="p1", effect_class="VIEW_ONLY", information_gain=q("0.8"), risk=q("0.1"),
        blast_radius=q("0.1"), rollback_confidence=q("1"), pilot_cost=q("0.1"), sample_budget=100,
        rollback_procedure_id="rollback:view", stop_rule_id="stop:loss"
    )
    data.update(overrides)
    return ExperimentProposal(**data)


def policy(**overrides):
    data = dict(
        min_information_gain=q("0.2"), max_risk=q("0.3"), max_blast_radius=q("0.25"),
        min_rollback_confidence=q("0.9"), max_sample_budget=1000, max_treatment_fraction=q("0.2"),
        min_option_value=q("0.1"), risk_weight=q("0.4"), blast_weight=q("0.3"), cost_weight=q("0.3")
    )
    data.update(overrides)
    return ExperimentPolicy(**data)


class ExperimentTests(unittest.TestCase):
    def test_plans_positive_information_option(self):
        r = plan_experiment(proposal(), policy())
        self.assertEqual(r.status, "PLAN")
        self.assertGreater(r.option_value.raw, q("0.1").raw)
        self.assertLessEqual(r.treatment_fraction.raw, q("0.2").raw)
        self.assertEqual(r.treatment_budget + r.control_budget, 100)
        self.assertGreater(r.control_budget, 0)

    def test_irreversible_effect_rejected_at_contract(self):
        with self.assertRaises(ContractError):
            proposal(effect_class="IRREVERSIBLE")

    def test_risk_rejected(self):
        self.assertEqual(plan_experiment(proposal(risk=q("0.4")), policy()).reason, "RISK_TOO_HIGH")

    def test_blast_radius_rejected(self):
        self.assertEqual(plan_experiment(proposal(blast_radius=q("0.3")), policy()).reason, "BLAST_RADIUS_TOO_HIGH")

    def test_low_rollback_confidence_rejected(self):
        self.assertEqual(plan_experiment(proposal(rollback_confidence=q("0.8")), policy()).reason, "ROLLBACK_CONFIDENCE_TOO_LOW")

    def test_sample_budget_rejected(self):
        self.assertEqual(plan_experiment(proposal(sample_budget=1001), policy()).reason, "SAMPLE_BUDGET_TOO_HIGH")

    def test_low_option_value_holds(self):
        r = plan_experiment(proposal(information_gain=q("0.2"), risk=q("0.2"), blast_radius=q("0.2"), pilot_cost=q("0.8")), policy(min_option_value=q("0.05")))
        self.assertEqual(r.status, "HOLD")
        self.assertEqual(r.reason, "OPTION_VALUE_BELOW_THRESHOLD")

    def test_one_sample_cannot_form_holdout(self):
        r = plan_experiment(proposal(sample_budget=1), policy())
        self.assertEqual(r.status, "REJECT")
        self.assertEqual(r.reason, "NO_CONTROL_HOLDOUT")
