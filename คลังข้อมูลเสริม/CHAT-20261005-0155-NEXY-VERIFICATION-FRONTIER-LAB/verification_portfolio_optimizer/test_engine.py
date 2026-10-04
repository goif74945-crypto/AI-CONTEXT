import unittest

from verification_portfolio_optimizer.engine import (
    Check,
    Claim,
    NoValidPortfolio,
    PortfolioTooLarge,
    optimize_portfolio,
)


class VerificationPortfolioOptimizerTests(unittest.TestCase):
    def test_picks_minimum_cost_exact_portfolio(self):
        claims = [
            Claim("unit-behavior", frozenset({"E2"})),
            Claim("api-db-integration", frozenset({"E3"})),
        ]
        checks = [
            Check("broad-suite", 20, {"unit-behavior": "E2", "api-db-integration": "E3"}),
            Check("unit", 3, {"unit-behavior": "E2"}),
            Check("integration", 4, {"api-db-integration": "E3"}),
            Check("static", 1, {"unit-behavior": "E1"}),
        ]
        result = optimize_portfolio(claims, checks)
        self.assertEqual(result.checks, ("integration", "unit"))
        self.assertEqual(result.total_cost_units, 7)

    def test_does_not_substitute_wrong_evidence_class(self):
        claims = [Claim("behavior", frozenset({"E2"}))]
        checks = [Check("static-only", 1, {"behavior": "E1"})]
        with self.assertRaisesRegex(NoValidPortfolio, "behavior"):
            optimize_portfolio(claims, checks)

    def test_deterministic_tie_break(self):
        claims = [Claim("c", frozenset({"E2"}))]
        checks = [Check("z", 5, {"c": "E2"}), Check("a", 5, {"c": "E2"})]
        self.assertEqual(optimize_portfolio(claims, checks).checks, ("a",))

    def test_zero_claims_needs_no_checks(self):
        result = optimize_portfolio([], [Check("unused", 10, {})])
        self.assertEqual(result.total_cost_units, 0)
        self.assertEqual(result.checks, ())

    def test_limits_state_space_by_claim_count(self):
        claims = [Claim(f"c{i}", frozenset({"E2"})) for i in range(5)]
        checks = [Check("all", 1, {f"c{i}": "E2" for i in range(5)})]
        with self.assertRaises(PortfolioTooLarge):
            optimize_portfolio(claims, checks, max_exact_claims=4)

    def test_rejects_duplicate_ids_and_negative_cost(self):
        with self.assertRaisesRegex(ValueError, "claim_id"):
            optimize_portfolio(
                [Claim("x", frozenset({"E2"})), Claim("x", frozenset({"E2"}))], []
            )
        with self.assertRaisesRegex(ValueError, "negative"):
            optimize_portfolio(
                [Claim("x", frozenset({"E2"}))], [Check("bad", -1, {"x": "E2"})]
            )


if __name__ == "__main__":
    unittest.main()
