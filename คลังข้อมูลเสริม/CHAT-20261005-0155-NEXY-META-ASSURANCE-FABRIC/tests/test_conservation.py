import unittest

from nexy_meta_assurance.conservation import (
    ConservationError,
    ConservationRule,
    verify_sequence,
    verify_transition,
)


class ConservationTests(unittest.TestCase):
    def setUp(self):
        self.rule = ConservationRule("token balance", ("alice", "bob", "escrow"))

    def test_transfer_preserves_total(self):
        result = verify_transition(
            {"alice": 7, "bob": 3, "escrow": 0},
            {"alice": 5, "bob": 5, "escrow": 0},
            self.rule,
        )
        self.assertTrue(result.passed)
        self.assertEqual(result.residual, 0)

    def test_silent_mint_is_detected(self):
        result = verify_transition(
            {"alice": 7, "bob": 3, "escrow": 0},
            {"alice": 7, "bob": 4, "escrow": 0},
            self.rule,
        )
        self.assertFalse(result.passed)
        self.assertEqual(result.residual, 1)

    def test_declared_external_delta_is_accounted_for(self):
        result = verify_transition(
            {"alice": 7, "bob": 3, "escrow": 0},
            {"alice": 7, "bob": 3, "escrow": 5},
            self.rule,
            declared_external_delta=5,
        )
        self.assertTrue(result.passed)

    def test_missing_required_key_fails_closed(self):
        with self.assertRaises(ConservationError):
            verify_transition({"alice": 1, "bob": 2}, {"alice": 1, "bob": 2}, self.rule)

    def test_sequence_reports_each_transition(self):
        results = verify_sequence(
            [
                {"alice": 5, "bob": 5, "escrow": 0},
                {"alice": 4, "bob": 6, "escrow": 0},
                {"alice": 4, "bob": 5, "escrow": 1},
            ],
            self.rule,
        )
        self.assertEqual([item.passed for item in results], [True, True])


if __name__ == "__main__":
    unittest.main()
