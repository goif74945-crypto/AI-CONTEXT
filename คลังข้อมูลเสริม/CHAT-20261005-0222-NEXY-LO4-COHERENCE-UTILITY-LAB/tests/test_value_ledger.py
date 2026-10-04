import unittest

from lo4lab.value_ledger import Direction, ExperimentObservation, ValueContract, ValueLedgerError, assess_value


class TestValueLedger(unittest.TestCase):
    def contract(self):
        return ValueContract(
            "p1", "reduce ambiguity before execution", "fewer failed tasks", "success_rate",
            Direction.HIGHER_IS_BETTER, 0.05, "latency_ms", 20.0,
            "success_rate does not improve under controlled comparison",
        )

    def test_supported_benefit(self):
        obs = ExperimentObservation(0.80, 0.88, 100, 110, 100, "E3")
        result = assess_value(self.contract(), obs)
        self.assertEqual(result.status, "BENEFIT_SUPPORTED")
        self.assertTrue(result.advisory_only)

    def test_insufficient_evidence_is_not_verified(self):
        obs = ExperimentObservation(0.80, 0.90, 100, 110, 10, "E1")
        result = assess_value(self.contract(), obs)
        self.assertEqual(result.status, "NOT_VERIFIED")

    def test_guard_regression_falsifies(self):
        obs = ExperimentObservation(0.80, 0.90, 100, 150, 100, "E3")
        result = assess_value(self.contract(), obs)
        self.assertEqual(result.status, "FALSIFIED")
        self.assertIn("GUARD_REGRESSION_EXCEEDED", result.reason_codes)

    def test_explicit_falsifier_wins(self):
        obs = ExperimentObservation(0.80, 0.95, 100, 100, 100, "E3", True)
        self.assertEqual(assess_value(self.contract(), obs).status, "FALSIFIED")

    def test_below_threshold_is_no_supported_benefit(self):
        obs = ExperimentObservation(0.80, 0.82, 100, 100, 100, "E3")
        self.assertEqual(assess_value(self.contract(), obs).status, "NO_SUPPORTED_BENEFIT")

    def test_lower_is_better_direction(self):
        contract = ValueContract(
            "p2", "cache verified context", "faster answers", "latency_ms",
            Direction.LOWER_IS_BETTER, 10.0, "error_rate", 0.0, "latency does not drop",
        )
        obs = ExperimentObservation(100, 80, 0.01, 0.01, 100, "E2")
        self.assertEqual(assess_value(contract, obs).status, "BENEFIT_SUPPORTED")


    def test_higher_is_better_guard_detects_downward_regression(self):
        contract = ValueContract(
            "p3", "improve routing", "more successful tasks", "success_rate",
            Direction.HIGHER_IS_BETTER, 0.05, "safety_success_rate", 0.02,
            "safety success drops too far", Direction.HIGHER_IS_BETTER,
        )
        obs = ExperimentObservation(0.80, 0.90, 0.99, 0.95, 100, "E3")
        result = assess_value(contract, obs)
        self.assertEqual(result.status, "FALSIFIED")
        self.assertAlmostEqual(result.guard_regression, 0.04)

    def test_invalid_direction_type_rejected(self):
        with self.assertRaises(ValueLedgerError):
            ValueContract(
                "p4", "m", "o", "primary", "HIGHER_IS_BETTER", 0.1,
                "guard", 0.1, "f",
            )

    def test_same_primary_guard_metric_rejected(self):
        with self.assertRaises(ValueLedgerError):
            ValueContract("p", "m", "o", "x", Direction.HIGHER_IS_BETTER, 1, "x", 1, "f")


if __name__ == "__main__":
    unittest.main()
