from __future__ import annotations

import unittest

from c1_interpretation_convergence.implementation import (
    DecisionSignature,
    Interpretation,
    evaluate_convergence,
)


class InterpretationConvergenceTests(unittest.TestCase):
    @staticmethod
    def evaluator(item: Interpretation) -> DecisionSignature:
        return DecisionSignature(
            action="read",
            target=item.variables.get("target", "vault"),
            scope=("project:x",),
            effects=("none",),
            authority_epoch="law-v7",
        )

    def test_irrelevant_ambiguity_releases(self) -> None:
        items = [
            Interpretation("a", {"target": "vault", "tone": "short"}),
            Interpretation("b", {"target": "vault", "tone": "formal"}),
        ]
        result = evaluate_convergence(items, self.evaluator)
        self.assertEqual(result.status, "RELEASE")
        self.assertEqual(result.details["interpretation_count"], 2)

    def test_decision_relevant_ambiguity_freezes(self) -> None:
        items = [
            Interpretation("a", {"target": "vault"}),
            Interpretation("b", {"target": "production"}),
        ]
        result = evaluate_convergence(items, self.evaluator)
        self.assertEqual(result.status, "FREEZE")
        self.assertIn("target", result.details["divergent_fields"])

    def test_input_order_does_not_change_witness(self) -> None:
        a = Interpretation("a", {"target": "vault"})
        b = Interpretation("b", {"target": "vault"})
        left = evaluate_convergence([a, b], self.evaluator)
        right = evaluate_convergence([b, a], self.evaluator)
        self.assertEqual(left.details, right.details)

    def test_duplicate_id_freezes(self) -> None:
        result = evaluate_convergence(
            [Interpretation("x", {}), Interpretation("x", {})], self.evaluator
        )
        self.assertEqual(result.reason, "DUPLICATE_INTERPRETATION_ID")

    def test_evaluator_failure_freezes(self) -> None:
        def broken(_: Interpretation) -> DecisionSignature:
            raise RuntimeError("boom")

        result = evaluate_convergence([Interpretation("x", {})], broken)
        self.assertEqual(result.reason, "EVALUATOR_FAILURE")


if __name__ == "__main__":
    unittest.main()
