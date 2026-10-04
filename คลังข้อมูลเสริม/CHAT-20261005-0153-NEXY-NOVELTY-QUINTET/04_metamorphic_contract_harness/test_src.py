import unittest
from src import Relation, evaluate


class MetamorphicContractHarnessTests(unittest.TestCase):
    def test_detects_broken_idempotency(self):
        relation = Relation(
            name="idempotent",
            mutate=lambda x: x,
            holds=lambda fn, seed, mutated: fn(fn(seed)) == fn(seed),
        )
        def bad(x):
            return x + "!"
        report = evaluate(bad, ["a"], [relation])
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["violations"][0]["relation"], "idempotent")

    def test_mapping_order_invariance_passes_for_canonicalizer(self):
        relation = Relation(
            name="mapping-order-invariant",
            mutate=lambda d: dict(reversed(list(d.items()))),
            holds=lambda fn, seed, mutated: fn(seed) == fn(mutated),
        )
        def canonicalize(d):
            return tuple(sorted(d.items()))
        report = evaluate(canonicalize, [{"b": 2, "a": 1}], [relation])
        self.assertEqual(report["status"], "PASS")

    def test_mutation_exception_is_recorded_not_hidden(self):
        relation = Relation(
            name="bad-mutation",
            mutate=lambda _: (_ for _ in ()).throw(RuntimeError("boom")),
            holds=lambda fn, seed, mutated: True,
        )
        report = evaluate(lambda x: x, [1], [relation])
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["violations"][0]["reason"], "MUTATION_ERROR")

    def test_zero_checks_is_not_verified(self):
        report = evaluate(lambda x: x, [], [])
        self.assertEqual(report["status"], "NOT_VERIFIED")


if __name__ == "__main__":
    unittest.main()
