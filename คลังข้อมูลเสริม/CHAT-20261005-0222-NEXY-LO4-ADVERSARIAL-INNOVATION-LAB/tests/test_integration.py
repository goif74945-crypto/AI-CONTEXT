import unittest

from lo4lab.aurora import AbstentionCase, AbstentionPolicy, AgentAction
from lo4lab.contract_drift import ContractDriftPolicy
from lo4lab.integration import evaluate_lo4_release
from lo4lab.margin import Constraint, Operator
from lo4lab.traceweight import InfluenceGraph, InfluenceNode
from lo4lab.upa import EvidenceValue, TruthState


BASE = {
    "authorized_scope": ["prototype"],
    "success_invariants": ["tests-pass"],
    "forbidden_actions": ["mutate-nexy"],
    "assumptions": [],
    "required_evidence": ["e2"],
}


class IntegrationTests(unittest.TestCase):
    def _good_graph(self):
        return InfluenceGraph([
            InfluenceNode("a", {}, True, True),
            InfluenceNode("b", {}, True, True),
            InfluenceNode("final", {"a": 1, "b": 1}),
        ])

    def _good_kwargs(self):
        return dict(
            abstention_cases=[
                AbstentionCase("a", True, AgentAction.ANSWER, True, 0.99),
                AbstentionCase("b", False, AgentAction.ABSTAIN),
            ],
            abstention_policy=AbstentionPolicy(max_unsafe_answer_rate=0.0, min_reliability_score=0.99),
            constraints=[Constraint("risk", "0.01", Operator.LE, "0.1", scale="1", required_margin="0.05")],
            evidence_requirements=[EvidenceValue(TruthState.TRUE, ("proof-1",))],
            influence_graph=self._good_graph(),
            influence_target="final",
            before_contract=BASE,
            after_contract=dict(BASE),
            contract_policy=ContractDriftPolicy(max_total_cost=0),
        )

    def test_all_gates_release_candidate(self):
        report = evaluate_lo4_release(**self._good_kwargs())
        self.assertEqual(report.status, "RELEASE_CANDIDATE")
        self.assertEqual(report.blockers, ())

    def test_unknown_evidence_freezes(self):
        kwargs = self._good_kwargs()
        kwargs["evidence_requirements"] = [EvidenceValue(TruthState.UNKNOWN, ("missing",))]
        report = evaluate_lo4_release(**kwargs)
        self.assertEqual(report.status, "FREEZE")
        self.assertIn("UPA:UNKNOWN", report.blockers)

    def test_contract_drift_freezes(self):
        kwargs = self._good_kwargs()
        kwargs["after_contract"] = {**BASE, "assumptions": ["provider-is-correct"]}
        report = evaluate_lo4_release(**kwargs)
        self.assertEqual(report.status, "FREEZE")
        self.assertTrue(any(item.startswith("CONTRACT_DRIFT:") for item in report.blockers))


if __name__ == "__main__":
    unittest.main()
