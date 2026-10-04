import unittest

from boundary_payload_pathology_lab.engine import BoundaryPayloadError, Limits, strict_loads
from contract_mutation_adequacy_engine.engine import generate_mutants
from failure_witness_distiller.engine import distill
from negative_space_coverage_analyzer.engine import Evidence, Requirement, analyze_negative_space
from verification_portfolio_optimizer.engine import Check, Claim, optimize_portfolio


class FrontierLabAdversarialTests(unittest.TestCase):
    def test_distiller_preserves_exact_signature_not_just_failure_boolean(self):
        def oracle(doc):
            if doc.get("mode") == "release" and doc.get("authority") == "missing":
                return "FREEZE:AUTHORITY_MISSING"
            if doc.get("mode") == "release":
                return "FREEZE:OTHER"
            return None

        source = {"mode": "release", "authority": "missing", "noise": [1, 2, 3]}
        result = distill(source, oracle)
        self.assertEqual(result.signature, "FREEZE:AUTHORITY_MISSING")
        self.assertEqual(oracle(result.witness), "FREEZE:AUTHORITY_MISSING")

    def test_optimizer_prefers_fewer_checks_after_equal_cost(self):
        claims = [Claim("a", frozenset({"E2"})), Claim("b", frozenset({"E2"}))]
        checks = [
            Check("combined", 0, {"a": "E2", "b": "E2"}),
            Check("a-only", 0, {"a": "E2"}),
            Check("b-only", 0, {"b": "E2"}),
        ]
        self.assertEqual(optimize_portfolio(claims, checks).checks, ("combined",))

    def test_boundary_node_limit_is_fail_closed(self):
        # Root + list + three scalars = five structural nodes.
        self.assertEqual(strict_loads('{"x":[1,2,3]}', limits=Limits(max_nodes=5)), {"x": [1, 2, 3]})
        with self.assertRaisesRegex(BoundaryPayloadError, "max_nodes"):
            strict_loads('{"x":[1,2,3]}', limits=Limits(max_nodes=4))

    def test_mutant_cap_is_exact_and_deterministic(self):
        contract = {"a": 1, "b": 2, "c": True, "d": "strict"}
        one = generate_mutants(contract, max_mutants=3)
        two = generate_mutants(contract, max_mutants=3)
        self.assertEqual(len(one), 3)
        self.assertEqual(one, two)

    def test_one_negative_evidence_can_cover_multiple_linked_obligations(self):
        reqs = [Requirement("R1", "DENY"), Requirement("R2", "FREEZE_ON")]
        evs = [Evidence("T-shared", frozenset({"R1", "R2"}), "negative", "PASS", "E3")]
        report = analyze_negative_space(reqs, evs)
        self.assertEqual(report.negative_requirements, 2)
        self.assertEqual(report.covered, 2)
        self.assertEqual(report.missing, 0)


if __name__ == "__main__":
    unittest.main()
