import unittest

from lo4lab import (
    Claim,
    Direction,
    ExperimentObservation,
    FactVersion,
    Replica,
    Status,
    TermDefinition,
    TerminologyRegistry,
    ValueContract,
    assess_value,
    join_statuses,
    merge_replicas,
    resolve_at,
)


class TestIntegration(unittest.TestCase):
    def test_five_systems_compose_without_authority_escalation(self):
        terminology = TerminologyRegistry([
            TermDefinition("requirement-count", "NEXY/source", "count of normalized source requirement rows"),
        ])
        term = terminology.resolve("requirement-count", "NEXY/source")
        self.assertEqual(term.status, "PASS")

        fact = FactVersion("matrix-837", "NEXY", "requirement-count", 837, 0, None, 10, "current-matrix", 100)
        temporal = resolve_at([fact], subject="NEXY", attribute="requirement-count", valid_time=10, known_time=10)
        self.assertEqual(temporal.values, (837,))

        merged = merge_replicas([
            Replica((Claim("c1", "NEXY", "requirement-count", "source", 837, 100, "matrix-a"),)),
            Replica((Claim("c2", "NEXY", "requirement-count", "source", 837, 100, "matrix-b"),)),
        ])
        self.assertEqual(merged.status, "PASS")

        contract = ValueContract(
            "lo4-proposal",
            "preserve bitemporal context",
            "reduce stale-context mistakes",
            "verified_task_success",
            Direction.HIGHER_IS_BETTER,
            0.05,
            "median_latency_ms",
            25.0,
            "success fails to improve under controlled evaluation",
        )
        assessment = assess_value(
            contract,
            ExperimentObservation(0.80, 0.87, 100.0, 110.0, 120, "E3"),
        )
        self.assertEqual(assessment.status, "BENEFIT_SUPPORTED")
        self.assertTrue(assessment.advisory_only)

        final = join_statuses([
            Status.PASS,
            Status.PASS,
            Status.PASS,
            Status.PASS,
            Status.PASS,
        ])
        self.assertEqual(final.status, Status.PASS)

    def test_conflict_propagates_to_final_gate(self):
        merged = merge_replicas([
            Replica((Claim("a", "x", "p", "s", 1, 5, "e1"),)),
            Replica((Claim("b", "x", "p", "s", 2, 5, "e2"),)),
        ])
        self.assertEqual(merged.status, "CONFLICT")
        final = join_statuses([Status.PASS, Status.CONFLICT])
        self.assertEqual(final.status, Status.CONFLICT)


if __name__ == "__main__":
    unittest.main()
