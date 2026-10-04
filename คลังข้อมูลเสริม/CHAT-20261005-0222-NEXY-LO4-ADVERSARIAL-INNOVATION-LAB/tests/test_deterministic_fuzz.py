import random
import unittest
from decimal import Decimal

from lo4lab.aurora import AbstentionCase, AgentAction, evaluate_abstention
from lo4lab.contract_drift import analyze_contract_drift
from lo4lab.margin import Constraint, Operator, evaluate_constraints
from lo4lab.traceweight import InfluenceGraph, InfluenceNode
from lo4lab.upa import EvidenceValue, TruthState


class DeterministicFuzzTests(unittest.TestCase):
    def test_aurora_metrics_always_bounded(self):
        rng = random.Random(20261005022201)
        for batch in range(300):
            cases = []
            for i in range(rng.randint(1, 20)):
                answerable = bool(rng.getrandbits(1))
                answer = bool(rng.getrandbits(1))
                if answer:
                    cases.append(AbstentionCase(
                        f"{batch}-{i}",
                        answerable,
                        AgentAction.ANSWER,
                        correct=bool(rng.getrandbits(1)),
                        confidence=rng.random(),
                        risk_weight=rng.uniform(0.1, 5.0),
                    ))
                else:
                    cases.append(AbstentionCase(
                        f"{batch}-{i}",
                        answerable,
                        AgentAction.ABSTAIN,
                        risk_weight=rng.uniform(0.1, 5.0),
                    ))
            report = evaluate_abstention(cases)
            self.assertGreaterEqual(report.unsafe_answer_rate, 0.0)
            self.assertLessEqual(report.unsafe_answer_rate, 1.0)
            self.assertGreaterEqual(report.brier_score, 0.0)
            self.assertLessEqual(report.brier_score, 1.0)
            self.assertGreaterEqual(report.reliability_score, 0.0)
            self.assertLessEqual(report.reliability_score, 1.0)

    def test_margin_direction_and_status_consistency(self):
        rng = random.Random(20261005022202)
        ops = [Operator.LE, Operator.LT, Operator.GE, Operator.GT]
        for i in range(1000):
            actual = Decimal(rng.randint(-1000, 1000)) / Decimal("10")
            limit = Decimal(rng.randint(-1000, 1000)) / Decimal("10")
            op = rng.choice(ops)
            report = evaluate_constraints([
                Constraint(f"c{i}", actual, op, limit, scale="10", required_margin="0.1")
            ])
            result = report.results[0]
            if result.status == "VIOLATION":
                self.assertEqual(report.release_status, "FREEZE")
            elif result.status == "FRAGILE_PASS":
                self.assertEqual(report.release_status, "REVERIFY")
            else:
                self.assertEqual(report.release_status, "RELEASE")

    def test_upa_closed_and_releaseable_only_true(self):
        rng = random.Random(20261005022203)
        states = list(TruthState)
        for _ in range(2000):
            a = EvidenceValue(rng.choice(states), ("a",))
            b = EvidenceValue(rng.choice(states), ("b",))
            for value in (a.logical_and(b), a.logical_or(b), a.knowledge_join(b)):
                self.assertIsInstance(value.state, TruthState)
                self.assertEqual(value.releaseable, value.state is TruthState.TRUE)

    def test_traceweight_always_normalizes_source_influence(self):
        rng = random.Random(20261005022204)
        for batch in range(300):
            count = rng.randint(2, 8)
            nodes = [
                InfluenceNode(f"s{i}", {}, True, bool(rng.getrandbits(1)))
                for i in range(count)
            ]
            weights = {f"s{i}": rng.uniform(0.001, 10.0) for i in range(count)}
            nodes.append(InfluenceNode("final", weights))
            report = InfluenceGraph(nodes).analyze("final", max_dominance_ratio=1.0, max_unverified_influence=1.0)
            self.assertAlmostEqual(sum(v for _, v in report.source_influence), 1.0, places=12)
            self.assertGreaterEqual(report.effective_source_count, 1.0 - 1e-12)
            self.assertLessEqual(report.effective_source_count, count + 1e-9)

    def test_contract_dangerous_deltas_never_silently_pass(self):
        base = {
            "authorized_scope": ["a"],
            "success_invariants": ["i"],
            "forbidden_actions": ["f"],
            "assumptions": [],
            "required_evidence": ["e"],
        }
        dangerous = [
            {**base, "authorized_scope": ["a", "new"]},
            {**base, "success_invariants": []},
            {**base, "forbidden_actions": []},
            {**base, "assumptions": ["guess"]},
            {**base, "required_evidence": []},
        ]
        for after in dangerous:
            report = analyze_contract_drift(base, after)
            self.assertEqual(report.status, "FREEZE")
            self.assertTrue(report.reasons)


if __name__ == "__main__":
    unittest.main()
