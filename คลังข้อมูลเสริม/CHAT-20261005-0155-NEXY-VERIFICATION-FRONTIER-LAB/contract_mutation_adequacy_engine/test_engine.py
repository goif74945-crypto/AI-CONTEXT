import unittest

from contract_mutation_adequacy_engine.engine import evaluate_mutation_adequacy, generate_mutants


class ContractMutationAdequacyEngineTests(unittest.TestCase):
    def setUp(self):
        self.contract = {"min": 1, "max": 3, "enabled": True, "mode": "strict"}

    def test_generates_deterministic_unique_mutants(self):
        a = generate_mutants(self.contract)
        b = generate_mutants(self.contract)
        self.assertEqual(a, b)
        ids = [m.mutant_id for m in a]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreater(len(ids), 0)

    def test_weak_oracle_exposes_surviving_mutants(self):
        def weak(doc):
            return "min" in doc and "max" in doc and doc["min"] <= doc["max"]

        report = evaluate_mutation_adequacy(self.contract, weak)
        self.assertGreater(report.survived, 0)
        self.assertLess(report.score, 1.0)

    def test_strict_oracle_kills_all_generated_mutants(self):
        def strict(doc):
            return doc == self.contract

        report = evaluate_mutation_adequacy(self.contract, strict)
        self.assertGreater(report.total, 0)
        self.assertEqual(report.killed, report.total)
        self.assertEqual(report.score, 1.0)

    def test_baseline_must_pass(self):
        with self.assertRaisesRegex(ValueError, "baseline"):
            evaluate_mutation_adequacy(self.contract, lambda _doc: False)

    def test_non_positive_mutant_budget_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "max_mutants"):
            generate_mutants(self.contract, max_mutants=0)
        with self.assertRaisesRegex(ValueError, "max_mutants"):
            evaluate_mutation_adequacy(self.contract, lambda _doc: True, max_mutants=-1)

    def test_no_generated_mutants_does_not_produce_vacuous_perfect_score(self):
        with self.assertRaisesRegex(ValueError, "no mutants generated"):
            evaluate_mutation_adequacy({}, lambda _doc: True)


if __name__ == "__main__":
    unittest.main()
