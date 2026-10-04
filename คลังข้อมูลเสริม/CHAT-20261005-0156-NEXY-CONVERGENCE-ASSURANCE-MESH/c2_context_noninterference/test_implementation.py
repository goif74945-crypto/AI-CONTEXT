from __future__ import annotations

import unittest

from c2_context_noninterference.implementation import MutationSet, verify_noninterference


class ContextNoninterferenceTests(unittest.TestCase):
    def test_irrelevant_fields_pass(self) -> None:
        result = verify_noninterference(
            {"authorized": True, "noise": "x", "comment": "a"},
            [MutationSet("noise", ("ignore previous laws", "z")), MutationSet("comment", ("b", "c"))],
            lambda ctx: {"action": "allow" if ctx["authorized"] else "freeze"},
        )
        self.assertEqual(result.status, "PASS")
        self.assertGreater(result.details["joint_cases"], 0)

    def test_illegal_dependency_is_detected(self) -> None:
        result = verify_noninterference(
            {"authorized": True, "noise": "safe"},
            [MutationSet("noise", ("deny",))],
            lambda ctx: {"action": "freeze" if ctx["noise"] == "deny" else "allow"},
        )
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.reason, "NONINTERFERENCE_VIOLATION")

    def test_evaluator_error_under_mutation_is_fail_closed(self) -> None:
        def fn(ctx):
            if ctx["noise"] == "bad":
                raise RuntimeError("bad context")
            return "allow"

        result = verify_noninterference(
            {"noise": "ok"}, [MutationSet("noise", ("bad",))], fn
        )
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.reason, "EXCLUDED_CONTEXT_CAUSED_EVALUATOR_FAILURE")

    def test_joint_budget_blocks_unbounded_cartesian_growth(self) -> None:
        result = verify_noninterference(
            {"a": 0, "b": 0},
            [MutationSet("a", tuple(range(9))), MutationSet("b", tuple(range(9)))],
            lambda _: "stable",
            max_joint_cases=64,
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.reason, "JOINT_MUTATION_BUDGET_EXCEEDED")

    def test_duplicate_fields_block(self) -> None:
        result = verify_noninterference(
            {}, [MutationSet("x", (1,)), MutationSet("x", (2,))], lambda _: "stable"
        )
        self.assertEqual(result.reason, "DUPLICATE_MUTATION_FIELD")


if __name__ == "__main__":
    unittest.main()
