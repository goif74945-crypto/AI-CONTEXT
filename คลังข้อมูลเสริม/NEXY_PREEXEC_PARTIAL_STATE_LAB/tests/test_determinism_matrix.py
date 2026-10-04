from __future__ import annotations

import itertools
import unittest

from nexy_pepsa.engine import analyze
from nexy_pepsa.models import ExecutionPlan, Policy, Step, StepKind, Verdict


class DeterminismMatrixTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = Policy(
            policy_id="determinism-policy",
            allowed_boundaries=("B", "A"),
            protected_resources=("secret:**", "production:**"),
        )

    def test_all_120_permutations_of_five_independent_reads_are_semantically_identical(self) -> None:
        steps = tuple(
            Step(id=letter, kind=StepKind.READ, resource=f"resource:{letter}", boundary="A")
            for letter in ("a", "b", "c", "d", "e")
        )
        baseline = analyze(ExecutionPlan(plan_id="permute", steps=steps), self.policy)
        self.assertEqual(baseline.verdict, Verdict.READY)
        self.assertEqual(baseline.ordered_steps, ("a", "b", "c", "d", "e"))
        checked = 0
        for permutation in itertools.permutations(steps):
            report = analyze(ExecutionPlan(plan_id="permute", steps=permutation), self.policy)
            self.assertEqual(report.plan_hash, baseline.plan_hash)
            self.assertEqual(report.combined_hash, baseline.combined_hash)
            self.assertEqual(report.ordered_steps, baseline.ordered_steps)
            checked += 1
        self.assertEqual(checked, 120)

    def test_dependency_and_evidence_array_order_do_not_change_plan_identity(self) -> None:
        common = dict(
            id="c",
            kind=StepKind.CREATE,
            resource="resource:c",
            boundary="A",
            reversible=True,
            rollback_strategy="restore",
            postcondition="exists",
        )
        left = ExecutionPlan(
            plan_id="sets",
            steps=(
                Step(id="a", kind=StepKind.READ, resource="a", boundary="A"),
                Step(id="b", kind=StepKind.READ, resource="b", boundary="A"),
                Step(depends_on=("a", "b"), evidence_required=("E2_UNIT", "E0_PRESENCE"), **common),
            ),
        )
        right = ExecutionPlan(
            plan_id="sets",
            steps=(
                Step(id="b", kind=StepKind.READ, resource="b", boundary="A"),
                Step(id="a", kind=StepKind.READ, resource="a", boundary="A"),
                Step(depends_on=("b", "a"), evidence_required=("E0_PRESENCE", "E2_UNIT"), **common),
            ),
        )
        left_report = analyze(left, self.policy)
        right_report = analyze(right, self.policy)
        self.assertEqual(left_report.plan_hash, right_report.plan_hash)
        self.assertEqual(left_report.combined_hash, right_report.combined_hash)

    def test_policy_set_order_does_not_change_policy_identity(self) -> None:
        plan = ExecutionPlan(plan_id="read", steps=(Step(id="r", kind=StepKind.READ, resource="x", boundary="A"),))
        left = Policy(
            policy_id="p",
            allowed_boundaries=("A", "B"),
            protected_resources=("secret:**", "production:**"),
        )
        right = Policy(
            policy_id="p",
            allowed_boundaries=("B", "A"),
            protected_resources=("production:**", "secret:**"),
        )
        self.assertEqual(analyze(plan, left).policy_hash, analyze(plan, right).policy_hash)

    def test_maximum_default_sized_read_dag_is_ready(self) -> None:
        steps = tuple(
            Step(
                id=f"s{index:03d}",
                kind=StepKind.READ,
                resource=f"resource:{index}",
                boundary="A",
                depends_on=(() if index == 0 else (f"s{index - 1:03d}",)),
            )
            for index in range(128)
        )
        report = analyze(ExecutionPlan(plan_id="chain-128", steps=steps), self.policy)
        self.assertEqual(report.verdict, Verdict.READY)
        self.assertEqual(report.stats["steps"], 128)


if __name__ == "__main__":
    unittest.main()
