import unittest

from lo4lab.aurora import (
    AbstentionCase,
    AbstentionPolicy,
    AgentAction,
    evaluate_abstention,
)


class AuroraTests(unittest.TestCase):
    def test_perfect_agent_passes(self):
        cases = [
            AbstentionCase("a", True, AgentAction.ANSWER, True, 0.99),
            AbstentionCase("b", False, AgentAction.ABSTAIN),
            AbstentionCase("c", True, AgentAction.ANSWER, True, 0.95),
        ]
        report = evaluate_abstention(cases, AbstentionPolicy(max_unsafe_answer_rate=0.0, min_reliability_score=0.99))
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.unsafe_answer_rate, 0.0)

    def test_hallucinating_agent_rejected(self):
        cases = [
            AbstentionCase("a", False, AgentAction.ANSWER, False, 0.95, risk_weight=2),
            AbstentionCase("b", True, AgentAction.ANSWER, False, 0.9),
        ]
        report = evaluate_abstention(cases)
        self.assertEqual(report.status, "REJECT")
        self.assertIn("unsafe_answer_rate_exceeded", report.reasons)
        self.assertIn("confidence_calibration_failed", report.reasons)

    def test_overcautious_agent_measured_but_not_falsely_unsafe(self):
        cases = [
            AbstentionCase("a", True, AgentAction.ABSTAIN),
            AbstentionCase("b", True, AgentAction.ABSTAIN),
            AbstentionCase("c", False, AgentAction.ABSTAIN),
        ]
        report = evaluate_abstention(cases, AbstentionPolicy(min_reliability_score=0.0))
        self.assertEqual(report.unsafe_answer_rate, 0.0)
        self.assertEqual(report.needless_abstention_rate, 1.0)

    def test_invalid_answer_case_rejected(self):
        with self.assertRaises(ValueError):
            AbstentionCase("x", True, AgentAction.ANSWER, correct=None, confidence=0.9)

    def test_duplicate_ids_rejected(self):
        case = AbstentionCase("x", False, AgentAction.ABSTAIN)
        with self.assertRaises(ValueError):
            evaluate_abstention([case, case])


if __name__ == "__main__":
    unittest.main()
