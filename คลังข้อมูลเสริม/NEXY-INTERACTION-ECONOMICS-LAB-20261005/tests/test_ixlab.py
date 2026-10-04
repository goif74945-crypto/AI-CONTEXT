from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from nexy_ixlab.model import InteractionPlan, ValidationError
from nexy_ixlab.optimizer import optimize_plan
from nexy_ixlab.planner import Action, DecisionContext, Risk, decide_action
from nexy_ixlab.scorer import assess_plan


def make_plan(steps, **budget):
    return InteractionPlan.from_mapping({"name": "test", "budget": budget or {}, "steps": steps})


class ScoringTests(unittest.TestCase):
    def test_high_friction_plan_exceeds_budget(self):
        plan = make_plan([
            {"id": "q1", "kind": "clarification", "blocking": True, "user_effort": 2, "justification": "required"},
            {"id": "q2", "kind": "clarification", "blocking": True, "user_effort": 2, "justification": "required"},
            {"id": "choose", "kind": "selection", "blocking": True, "choice_count": 16, "context_switches": 3, "user_effort": 3, "justification": "required"},
            {"id": "wait", "kind": "wait", "estimated_wait_ms": 10_000},
        ], max_friction_score=35, max_blocking_touches=2, max_choice_bits=3, max_context_switches=2, max_wait_ms=5000)
        a = assess_plan(plan)
        self.assertGreater(a.friction_score, 35)
        self.assertFalse(a.passed_budget)
        codes = {f.code for f in a.findings}
        self.assertIn("IXF-BUDGET-SCORE", codes)
        self.assertIn("IXF-BUDGET-WAIT", codes)

    def test_unguarded_irreversible_action_is_error(self):
        a = assess_plan(make_plan([{
            "id": "delete", "kind": "irreversible_action", "reversible": False, "preauthorized": False
        }], max_friction_score=100))
        self.assertEqual(a.unguarded_irreversible_actions, ("delete",))
        self.assertIn("IXF-UNGUARDED-IRREVERSIBLE", {f.code for f in a.findings})

    def test_guarded_irreversible_action_has_no_guard_error(self):
        a = assess_plan(make_plan([
            {"id": "confirm", "kind": "confirmation", "guards_step_id": "delete", "required_by_law": True, "justification": "law"},
            {"id": "delete", "kind": "irreversible_action", "reversible": False},
        ], max_friction_score=100))
        self.assertEqual(a.unguarded_irreversible_actions, ())
        self.assertNotIn("IXF-STRUCT-GUARD-TARGET", {f.code for f in a.findings})

    def test_invalid_guard_target_is_error(self):
        a = assess_plan(make_plan([
            {"id": "confirm", "kind": "confirmation", "guards_step_id": "missing", "justification": "test"}
        ], max_friction_score=100))
        self.assertIn("IXF-STRUCT-GUARD-TARGET", {f.code for f in a.findings})

    def test_deterministic_assessment(self):
        p = make_plan([{"id": "auto", "kind": "automatic"}], max_friction_score=100)
        self.assertEqual(assess_plan(p).to_mapping(), assess_plan(p).to_mapping())


class OptimizerTests(unittest.TestCase):
    def test_removes_only_redundant_confirmation(self):
        plan = make_plan([
            {"id": "confirm", "kind": "confirmation", "guards_step_id": "save", "justification": "legacy"},
            {"id": "save", "kind": "automatic", "reversible": True},
        ], max_friction_score=100)
        result = optimize_plan(plan)
        self.assertEqual(result.removed_step_ids, ("confirm",))
        self.assertEqual([s.id for s in result.optimized_plan.steps], ["save"])
        self.assertLess(result.optimized.friction_score, result.original.friction_score)

    def test_never_removes_law_required_confirmation(self):
        plan = make_plan([
            {"id": "confirm", "kind": "confirmation", "guards_step_id": "save", "required_by_law": True, "justification": "law"},
            {"id": "save", "kind": "automatic", "reversible": True},
        ], max_friction_score=100)
        result = optimize_plan(plan)
        self.assertEqual(result.removed_step_ids, ())

    def test_never_removes_confirmation_that_other_step_depends_on(self):
        plan = make_plan([
            {"id": "confirm", "kind": "confirmation", "guards_step_id": "save", "justification": "sequence"},
            {"id": "save", "kind": "automatic", "reversible": True},
            {"id": "after", "kind": "automatic", "dependencies": ["confirm"]},
        ], max_friction_score=100)
        result = optimize_plan(plan)
        self.assertEqual(result.removed_step_ids, ())


class PlannerTests(unittest.TestCase):
    def test_authority_conflict_has_highest_precedence(self):
        r = decide_action(DecisionContext(authority_conflict=True, missing_required_information=True))
        self.assertEqual(r.action, Action.FREEZE)
        self.assertEqual(r.reason_code, "IXD-AUTHORITY-CONFLICT")

    def test_missing_required_information_asks(self):
        self.assertEqual(decide_action(DecisionContext(missing_required_information=True)).action, Action.ASK_CLARIFICATION)

    def test_insufficient_required_evidence_freezes(self):
        self.assertEqual(decide_action(DecisionContext(evidence_required=True, evidence_sufficient=False)).action, Action.FREEZE)

    def test_law_confirmation_cannot_be_skipped_by_preauthorization(self):
        ctx = DecisionContext(action_preauthorized=True, confirmation_required_by_law=True)
        self.assertEqual(decide_action(ctx).action, Action.CONFIRM)

    def test_irreversible_high_risk_requires_confirmation(self):
        ctx = DecisionContext(action_reversible=False, action_preauthorized=False, risk=Risk.HIGH)
        self.assertEqual(decide_action(ctx).action, Action.CONFIRM)

    def test_irreversible_low_risk_still_requires_confirmation(self):
        ctx = DecisionContext(action_reversible=False, action_preauthorized=False, risk=Risk.LOW)
        self.assertEqual(decide_action(ctx).action, Action.CONFIRM)

    def test_reversible_authorized_action_executes(self):
        self.assertEqual(decide_action(DecisionContext()).action, Action.EXECUTE)

    def test_decision_context_rejects_string_boolean(self):
        with self.assertRaises(ValidationError):
            DecisionContext.from_mapping({"authority_conflict": "false"})


class ValidationTests(unittest.TestCase):
    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValidationError):
            make_plan([{"id": "x", "kind": "automatic"}, {"id": "x", "kind": "wait"}])

    def test_selection_requires_two_choices(self):
        with self.assertRaises(ValidationError):
            make_plan([{"id": "x", "kind": "selection", "choice_count": 1}])

    def test_unknown_dependency_rejected(self):
        with self.assertRaises(ValidationError):
            make_plan([{"id": "x", "kind": "automatic", "dependencies": ["missing"]}])

    def test_string_boolean_rejected(self):
        with self.assertRaises(ValidationError):
            make_plan([{"id": "x", "kind": "automatic", "required": "false"}])

    def test_dependency_cycle_rejected(self):
        with self.assertRaises(ValidationError):
            make_plan([
                {"id": "a", "kind": "automatic", "dependencies": ["b"]},
                {"id": "b", "kind": "automatic", "dependencies": ["a"]},
            ])

    def test_negative_choice_budget_rejected(self):
        with self.assertRaises(ValidationError):
            make_plan([{"id": "a", "kind": "automatic"}], max_choice_bits=-1)

    def test_self_guard_rejected(self):
        with self.assertRaises(ValidationError):
            make_plan([{"id": "c", "kind": "confirmation", "guards_step_id": "c", "justification": "bad"}])


class CliIntegrationTests(unittest.TestCase):
    def test_analyze_cli_returns_machine_readable_json(self):
        payload = {"name": "cli", "budget": {"max_friction_score": 100}, "steps": [{"id": "auto", "kind": "automatic"}]}
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "plan.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            env = dict(os.environ)
            env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
            proc = subprocess.run(
                [sys.executable, "-m", "nexy_ixlab.cli", "analyze", str(path)],
                check=False, capture_output=True, text=True, env=env
            )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        parsed = json.loads(proc.stdout)
        self.assertEqual(parsed["status"], "OK")
        self.assertEqual(parsed["result"]["friction_score"], 0.0)

    def test_cli_rejects_invalid_input(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "plan.json"
            path.write_text('{"steps": "wrong"}', encoding="utf-8")
            env = dict(os.environ)
            env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
            proc = subprocess.run(
                [sys.executable, "-m", "nexy_ixlab.cli", "analyze", str(path)],
                check=False, capture_output=True, text=True, env=env
            )
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout)["status"], "ERROR")


if __name__ == "__main__":
    unittest.main()
