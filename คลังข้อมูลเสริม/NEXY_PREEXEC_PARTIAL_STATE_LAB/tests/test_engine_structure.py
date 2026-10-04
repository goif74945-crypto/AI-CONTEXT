from __future__ import annotations

import unittest

from nexy_pepsa.engine import PlanStructureError, deterministic_topological_order
from nexy_pepsa.models import ExecutionPlan, Step, StepKind


class StructureTests(unittest.TestCase):
    def test_topological_order_is_lexically_deterministic(self) -> None:
        plan = ExecutionPlan(
            plan_id="order",
            steps=(
                Step(id="z", kind=StepKind.READ, resource="z", boundary="B"),
                Step(id="a", kind=StepKind.READ, resource="a", boundary="B"),
                Step(id="m", kind=StepKind.READ, resource="m", boundary="B", depends_on=("a", "z")),
            ),
        )
        order = deterministic_topological_order(plan)
        self.assertEqual(tuple(step.id for step in order), ("a", "z", "m"))

    def test_duplicate_step_id_is_rejected(self) -> None:
        plan = ExecutionPlan(
            plan_id="dup",
            steps=(
                Step(id="x", kind=StepKind.READ, resource="a", boundary="B"),
                Step(id="x", kind=StepKind.READ, resource="b", boundary="B"),
            ),
        )
        with self.assertRaisesRegex(PlanStructureError, "duplicate step id"):
            deterministic_topological_order(plan)

    def test_missing_dependency_is_rejected(self) -> None:
        plan = ExecutionPlan(
            plan_id="missing",
            steps=(Step(id="x", kind=StepKind.READ, resource="a", boundary="B", depends_on=("nope",)),),
        )
        with self.assertRaisesRegex(PlanStructureError, "missing step"):
            deterministic_topological_order(plan)

    def test_cycle_is_rejected(self) -> None:
        plan = ExecutionPlan(
            plan_id="cycle",
            steps=(
                Step(id="a", kind=StepKind.READ, resource="a", boundary="B", depends_on=("b",)),
                Step(id="b", kind=StepKind.READ, resource="b", boundary="B", depends_on=("a",)),
            ),
        )
        with self.assertRaisesRegex(PlanStructureError, "dependency cycle"):
            deterministic_topological_order(plan)


if __name__ == "__main__":
    unittest.main()
