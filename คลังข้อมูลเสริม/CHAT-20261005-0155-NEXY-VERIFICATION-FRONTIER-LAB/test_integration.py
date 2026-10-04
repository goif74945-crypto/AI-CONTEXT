import unittest

from boundary_payload_pathology_lab.engine import canonical_json, strict_loads
from failure_witness_distiller.engine import distill
from negative_space_coverage_analyzer.engine import Evidence, Requirement, analyze_negative_space
from verification_portfolio_optimizer.engine import Check, Claim, optimize_portfolio


class FrontierLabIntegrationTests(unittest.TestCase):
    def test_strict_boundary_to_failure_witness_flow(self):
        raw = '{"action":"release","authority":"missing","noise":{"a":1,"b":2}}'
        payload = strict_loads(raw)

        def oracle(candidate):
            if candidate.get("action") == "release" and candidate.get("authority") != "approved":
                return "FREEZE:AUTHORITY_MISSING"
            return None

        result = distill(payload, oracle)
        self.assertEqual(oracle(result.witness), "FREEZE:AUTHORITY_MISSING")
        # The minimized witness remains serializable through the strict canonical boundary.
        canonical = canonical_json(result.witness)
        reparsed = strict_loads(canonical)
        self.assertEqual(reparsed, result.witness)

    def test_negative_space_gap_drives_correct_evidence_portfolio(self):
        reqs = [Requirement("R-NO-UNVERIFIED", "MUST_NOT")]
        current_evidence = [
            Evidence("T-happy", frozenset({"R-NO-UNVERIFIED"}), "positive", "PASS", "E2")
        ]
        gap = analyze_negative_space(reqs, current_evidence)
        self.assertEqual(gap.missing, 1)

        claims = [Claim("R-NO-UNVERIFIED-negative", frozenset({"E2"}))]
        checks = [
            Check("static-rule", 1, {"R-NO-UNVERIFIED-negative": "E1"}),
            Check("deny-unit", 3, {"R-NO-UNVERIFIED-negative": "E2"}),
            Check("full-e2", 9, {"R-NO-UNVERIFIED-negative": "E2"}),
        ]
        portfolio = optimize_portfolio(claims, checks)
        self.assertEqual(portfolio.checks, ("deny-unit",))
        self.assertEqual(portfolio.total_cost_units, 3)


if __name__ == "__main__":
    unittest.main()
