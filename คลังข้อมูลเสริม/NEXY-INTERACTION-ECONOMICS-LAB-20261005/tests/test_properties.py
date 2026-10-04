from __future__ import annotations

import itertools
import unittest

from nexy_ixlab.model import InteractionPlan
from nexy_ixlab.optimizer import optimize_plan
from nexy_ixlab.planner import Action, DecisionContext, Risk, decide_action


class ExhaustivePlannerPropertyTests(unittest.TestCase):
    def test_all_boolean_states_are_deterministic_and_obey_precedence(self):
        fields = [
            "authority_conflict",
            "missing_required_information",
            "evidence_required",
            "evidence_sufficient",
            "action_reversible",
            "action_preauthorized",
            "confirmation_required_by_law",
        ]
        checked = 0
        for bits in itertools.product([False, True], repeat=len(fields)):
            values = dict(zip(fields, bits, strict=True))
            for risk in Risk:
                ctx = DecisionContext(risk=risk, **values)
                first = decide_action(ctx)
                second = decide_action(ctx)
                self.assertEqual(first, second)

                if ctx.authority_conflict:
                    self.assertEqual(first.action, Action.FREEZE)
                elif ctx.missing_required_information:
                    self.assertEqual(first.action, Action.ASK_CLARIFICATION)
                elif ctx.evidence_required and not ctx.evidence_sufficient:
                    self.assertEqual(first.action, Action.FREEZE)
                elif ctx.confirmation_required_by_law:
                    self.assertEqual(first.action, Action.CONFIRM)
                elif not ctx.action_reversible and not ctx.action_preauthorized:
                    self.assertEqual(first.action, Action.CONFIRM)
                else:
                    self.assertEqual(first.action, Action.EXECUTE)
                checked += 1
        self.assertEqual(checked, 512)


class ExhaustiveOptimizerPropertyTests(unittest.TestCase):
    def test_confirmation_removal_requires_all_safety_preconditions(self):
        checked = 0
        for reversible, preauthorized, required_by_law, depended_on in itertools.product([False, True], repeat=4):
            steps = [
                {
                    "id": "confirm",
                    "kind": "confirmation",
                    "guards_step_id": "target",
                    "required_by_law": required_by_law,
                    "justification": "property-test",
                },
                {
                    "id": "target",
                    "kind": "automatic",
                    "reversible": reversible,
                    "preauthorized": preauthorized,
                },
            ]
            if depended_on:
                steps.append({"id": "consumer", "kind": "automatic", "dependencies": ["confirm"]})
            plan = InteractionPlan.from_mapping({
                "name": "property",
                "budget": {"max_friction_score": 100},
                "steps": steps,
            })
            result = optimize_plan(plan)
            expected_remove = (reversible or preauthorized) and not required_by_law and not depended_on
            self.assertEqual("confirm" in result.removed_step_ids, expected_remove)
            checked += 1
        self.assertEqual(checked, 16)


if __name__ == "__main__":
    unittest.main()
