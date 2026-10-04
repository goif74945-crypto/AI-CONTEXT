import unittest
from decimal import Decimal

from lo4lab.margin import Constraint, Operator, evaluate_constraints


class MarginTests(unittest.TestCase):
    def test_robust_release(self):
        report = evaluate_constraints([
            Constraint("latency_ms", "80", Operator.LE, "100", scale="100", required_margin="0.1"),
            Constraint("confidence", "0.97", Operator.GE, "0.9", scale="1", required_margin="0.05"),
        ])
        self.assertEqual(report.release_status, "RELEASE")

    def test_fragile_pass_requires_reverify(self):
        report = evaluate_constraints([
            Constraint("risk", "0.099", Operator.LE, "0.1", scale="1", required_margin="0.01"),
        ])
        self.assertEqual(report.release_status, "REVERIFY")
        self.assertEqual(report.results[0].status, "FRAGILE_PASS")

    def test_violation_freezes(self):
        report = evaluate_constraints([
            Constraint("cost", "101", Operator.LE, "100", scale="100"),
        ])
        self.assertEqual(report.release_status, "FREEZE")
        self.assertLess(report.minimum_margin, Decimal("0"))

    def test_strict_boundary_is_violation(self):
        report = evaluate_constraints([
            Constraint("x", "10", Operator.LT, "10"),
        ])
        self.assertEqual(report.release_status, "FREEZE")

    def test_invalid_scale_rejected(self):
        with self.assertRaises(ValueError):
            Constraint("x", 1, Operator.LE, 2, scale=0)


if __name__ == "__main__":
    unittest.main()
