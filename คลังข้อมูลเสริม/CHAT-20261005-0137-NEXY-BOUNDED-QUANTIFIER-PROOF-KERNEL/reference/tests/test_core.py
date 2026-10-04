import copy
import unittest


class CoreContractTests(unittest.TestCase):
    def setUp(self):
        from bqpk.core import evaluate_claim
        self.evaluate_claim = evaluate_claim

    def claim(self, *, quantifier="ALL", population=None, evidence=None, complete=True, threshold=None):
        population = ["A", "B"] if population is None else population
        evidence = (
            [
                {"member_id": member, "outcome": "MATCH", "evidence_ref": f"ev:{member}", "target_revision": "rev-1"}
                for member in population
            ]
            if evidence is None
            else evidence
        )
        doc = {
            "claim_id": "claim-1",
            "predicate": "member satisfies required proof",
            "quantifier": quantifier,
            "target_revision": "rev-1",
            "domain": {
                "population": population,
                "enumeration": {
                    "complete": complete,
                    "method": "fixture",
                    "evidence_ref": "enum:fixture",
                },
            },
            "evidence": evidence,
        }
        if threshold is not None:
            doc["threshold"] = threshold
        return doc

    def assertReleased(self, result):
        self.assertEqual("PASS", result["status"])
        self.assertEqual("RELEASE", result["action"])
        self.assertEqual("PROVEN", result["decision"])

    def assertFrozen(self, result):
        self.assertEqual("FREEZE", result["action"])
        self.assertNotEqual("PASS", result["status"])

    def test_all_passes_when_every_member_matches_in_closed_domain(self):
        result = self.evaluate_claim(self.claim())
        self.assertReleased(result)
        self.assertEqual(2, result["metrics"]["lower_bound_matches"])
        self.assertEqual(2, result["metrics"]["upper_bound_matches"])

    def test_all_is_refuted_by_known_counterexample_even_if_enumeration_is_incomplete(self):
        doc = self.claim(
            complete=False,
            evidence=[
                {"member_id": "A", "outcome": "MATCH", "evidence_ref": "ev:A", "target_revision": "rev-1"},
                {"member_id": "B", "outcome": "NO_MATCH", "evidence_ref": "ev:B", "target_revision": "rev-1"},
            ],
        )
        result = self.evaluate_claim(doc)
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("REFUTED", result["decision"])
        self.assertFrozen(result)
        self.assertEqual(["B"], result["counterexample_members"])

    def test_all_is_not_verified_when_member_evidence_is_missing(self):
        doc = self.claim(evidence=[
            {"member_id": "A", "outcome": "MATCH", "evidence_ref": "ev:A", "target_revision": "rev-1"}
        ])
        result = self.evaluate_claim(doc)
        self.assertEqual("NOT_VERIFIED", result["status"])
        self.assertEqual(["B"], result["missing_members"])
        self.assertFrozen(result)

    def test_none_passes_when_closed_domain_has_zero_matches(self):
        evidence = [
            {"member_id": "A", "outcome": "NO_MATCH", "evidence_ref": "ev:A", "target_revision": "rev-1"},
            {"member_id": "B", "outcome": "NO_MATCH", "evidence_ref": "ev:B", "target_revision": "rev-1"},
        ]
        result = self.evaluate_claim(self.claim(quantifier="NONE", evidence=evidence))
        self.assertReleased(result)

    def test_none_is_refuted_by_one_match(self):
        evidence = [
            {"member_id": "A", "outcome": "MATCH", "evidence_ref": "ev:A", "target_revision": "rev-1"},
            {"member_id": "B", "outcome": "NO_MATCH", "evidence_ref": "ev:B", "target_revision": "rev-1"},
        ]
        result = self.evaluate_claim(self.claim(quantifier="NONE", evidence=evidence))
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("REFUTED", result["decision"])
        self.assertEqual(["A"], result["counterexample_members"])

    def test_exactly_passes_only_when_lower_and_upper_equal_threshold(self):
        evidence = [
            {"member_id": "A", "outcome": "MATCH", "evidence_ref": "ev:A", "target_revision": "rev-1"},
            {"member_id": "B", "outcome": "NO_MATCH", "evidence_ref": "ev:B", "target_revision": "rev-1"},
        ]
        result = self.evaluate_claim(self.claim(quantifier="EXACTLY", threshold=1, evidence=evidence))
        self.assertReleased(result)

    def test_exactly_is_refuted_when_lower_bound_exceeds_threshold(self):
        result = self.evaluate_claim(self.claim(quantifier="EXACTLY", threshold=1))
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("REFUTED", result["decision"])
        self.assertFrozen(result)

    def test_exactly_is_not_verified_when_domain_is_incomplete(self):
        evidence = [
            {"member_id": "A", "outcome": "MATCH", "evidence_ref": "ev:A", "target_revision": "rev-1"},
            {"member_id": "B", "outcome": "NO_MATCH", "evidence_ref": "ev:B", "target_revision": "rev-1"},
        ]
        result = self.evaluate_claim(self.claim(quantifier="EXACTLY", threshold=1, complete=False, evidence=evidence))
        self.assertEqual("NOT_VERIFIED", result["status"])
        self.assertIsNone(result["metrics"]["upper_bound_matches"])
        self.assertEqual("UNBOUNDED", result["metrics"]["upper_bound_kind"])

    def test_at_least_can_be_proven_from_lower_bound_even_with_incomplete_enumeration(self):
        result = self.evaluate_claim(self.claim(quantifier="AT_LEAST", threshold=2, complete=False))
        self.assertReleased(result)
        self.assertIn("LOWER_BOUND_MEETS_THRESHOLD", result["reason_codes"])

    def test_at_least_is_refuted_when_finite_upper_bound_is_below_threshold(self):
        evidence = [
            {"member_id": "A", "outcome": "MATCH", "evidence_ref": "ev:A", "target_revision": "rev-1"},
            {"member_id": "B", "outcome": "NO_MATCH", "evidence_ref": "ev:B", "target_revision": "rev-1"},
        ]
        result = self.evaluate_claim(self.claim(quantifier="AT_LEAST", threshold=2, evidence=evidence))
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("REFUTED", result["decision"])

    def test_at_most_can_pass_from_finite_upper_bound_with_unresolved_members(self):
        evidence = [
            {"member_id": "A", "outcome": "UNKNOWN", "evidence_ref": "ev:A", "target_revision": "rev-1"}
        ]
        result = self.evaluate_claim(self.claim(quantifier="AT_MOST", threshold=2, evidence=evidence))
        self.assertReleased(result)
        self.assertEqual(2, result["metrics"]["upper_bound_matches"])

    def test_at_most_is_not_verified_when_upper_bound_is_unbounded(self):
        result = self.evaluate_claim(self.claim(quantifier="AT_MOST", threshold=2, complete=False))
        self.assertEqual("NOT_VERIFIED", result["status"])
        self.assertFrozen(result)

    def test_stale_evidence_is_unresolved_and_blocks_all_pass(self):
        evidence = [
            {"member_id": "A", "outcome": "MATCH", "evidence_ref": "ev:A", "target_revision": "old-rev"},
            {"member_id": "B", "outcome": "MATCH", "evidence_ref": "ev:B", "target_revision": "rev-1"},
        ]
        result = self.evaluate_claim(self.claim(evidence=evidence))
        self.assertEqual("NOT_VERIFIED", result["status"])
        self.assertEqual(["A"], result["stale_members"])
        self.assertIn("STALE_EVIDENCE", result["reason_codes"])

    def test_duplicate_population_member_is_invalid(self):
        result = self.evaluate_claim(self.claim(population=["A", "A"]))
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("DUPLICATE_POPULATION_MEMBER", result["reason_codes"])
        self.assertFrozen(result)

    def test_duplicate_evidence_member_is_invalid(self):
        evidence = [
            {"member_id": "A", "outcome": "MATCH", "evidence_ref": "ev:1", "target_revision": "rev-1"},
            {"member_id": "A", "outcome": "MATCH", "evidence_ref": "ev:2", "target_revision": "rev-1"},
        ]
        result = self.evaluate_claim(self.claim(evidence=evidence))
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("DUPLICATE_EVIDENCE_MEMBER", result["reason_codes"])

    def test_evidence_for_member_outside_domain_is_invalid(self):
        evidence = [
            {"member_id": "A", "outcome": "MATCH", "evidence_ref": "ev:A", "target_revision": "rev-1"},
            {"member_id": "C", "outcome": "MATCH", "evidence_ref": "ev:C", "target_revision": "rev-1"},
        ]
        result = self.evaluate_claim(self.claim(evidence=evidence))
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("EVIDENCE_MEMBER_OUTSIDE_DOMAIN", result["reason_codes"])

    def test_empty_population_is_rejected_to_prevent_vacuous_truth(self):
        result = self.evaluate_claim(self.claim(population=[], evidence=[]))
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("EMPTY_DOMAIN_FORBIDDEN", result["reason_codes"])

    def test_threshold_is_required_for_count_quantifiers(self):
        result = self.evaluate_claim(self.claim(quantifier="EXACTLY"))
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("INVALID_THRESHOLD", result["reason_codes"])

    def test_boolean_threshold_is_rejected_even_though_python_bool_is_int(self):
        doc = self.claim(quantifier="AT_LEAST")
        doc["threshold"] = True
        result = self.evaluate_claim(doc)
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("INVALID_THRESHOLD", result["reason_codes"])

    def test_blank_evidence_reference_is_invalid(self):
        evidence = [
            {"member_id": "A", "outcome": "MATCH", "evidence_ref": "", "target_revision": "rev-1"},
            {"member_id": "B", "outcome": "MATCH", "evidence_ref": "ev:B", "target_revision": "rev-1"},
        ]
        result = self.evaluate_claim(self.claim(evidence=evidence))
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("INVALID_EVIDENCE_REF", result["reason_codes"])

    def test_unknown_quantifier_is_invalid(self):
        result = self.evaluate_claim(self.claim(quantifier="SOME"))
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("INVALID_QUANTIFIER", result["reason_codes"])

    def test_same_input_produces_identical_output_and_fingerprint(self):
        doc = self.claim()
        first = self.evaluate_claim(copy.deepcopy(doc))
        second = self.evaluate_claim(copy.deepcopy(doc))
        self.assertEqual(first, second)
        self.assertTrue(first["input_fingerprint"].startswith("sha256:"))

    def test_population_limit_fails_closed(self):
        population = [f"M{i}" for i in range(10001)]
        result = self.evaluate_claim(self.claim(population=population, evidence=[]))
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("DOMAIN_TOO_LARGE", result["reason_codes"])

    def test_unhashable_quantifier_fails_closed_instead_of_raising(self):
        doc = self.claim()
        doc["quantifier"] = []
        result = self.evaluate_claim(doc)
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("INVALID_QUANTIFIER", result["reason_codes"])

    def test_unhashable_population_member_fails_closed_instead_of_raising(self):
        doc = self.claim(population=["A"], evidence=[])
        doc["domain"]["population"] = [[]]
        result = self.evaluate_claim(doc)
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("INVALID_POPULATION_MEMBER", result["reason_codes"])

    def test_unhashable_evidence_outcome_fails_closed_instead_of_raising(self):
        evidence = [
            {"member_id": "A", "outcome": {}, "evidence_ref": "ev:A", "target_revision": "rev-1"},
            {"member_id": "B", "outcome": "MATCH", "evidence_ref": "ev:B", "target_revision": "rev-1"},
        ]
        result = self.evaluate_claim(self.claim(evidence=evidence))
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("INVALID_EVIDENCE_OUTCOME", result["reason_codes"])

    def test_noncanonical_json_value_fails_closed(self):
        doc = self.claim()
        doc["extra"] = float("nan")
        result = self.evaluate_claim(doc)
        self.assertEqual("INVALID", result["decision"])
        self.assertIn("DOCUMENT_NOT_CANONICAL_JSON", result["reason_codes"])


if __name__ == "__main__":
    unittest.main()
