from __future__ import annotations

import unittest

from nexy_pepsa.engine import analyze
from nexy_pepsa.models import ExecutionPlan, Policy, Step, StepKind, Verdict


BASE_POLICY = Policy(
    policy_id="test-policy",
    allowed_boundaries=("AI_CONTEXT", "EXTERNAL"),
    protected_resources=("repo:NEXY.AI/**",),
)


def codes(report) -> set[str]:
    return {item.code for item in report.findings}


class PolicyTests(unittest.TestCase):
    def test_read_only_plan_is_ready(self) -> None:
        plan = ExecutionPlan(
            plan_id="read-only",
            steps=(Step(id="read", kind=StepKind.READ, resource="repo:AI-CONTEXT/README.md", boundary="AI_CONTEXT"),),
        )
        report = analyze(plan, BASE_POLICY)
        self.assertEqual(report.verdict, Verdict.READY)
        self.assertEqual(report.stats["error_findings"], 0)

    def test_reversible_mutation_with_rollback_is_ready(self) -> None:
        plan = ExecutionPlan(
            plan_id="reversible",
            steps=(
                Step(
                    id="write",
                    kind=StepKind.CREATE,
                    resource="repo:AI-CONTEXT/aux/new.json",
                    boundary="AI_CONTEXT",
                    reversible=True,
                    rollback_strategy="delete newly-created file using exact blob identity",
                    postcondition="new file exists with expected content hash",
                    evidence_required=("E0_PRESENCE", "E2_UNIT"),
                ),
            ),
        )
        report = analyze(plan, BASE_POLICY)
        self.assertEqual(report.verdict, Verdict.READY)

    def test_mutating_protected_resource_freezes(self) -> None:
        plan = ExecutionPlan(
            plan_id="protected",
            steps=(
                Step(
                    id="write",
                    kind=StepKind.UPDATE,
                    resource="repo:NEXY.AI/src/core.ts",
                    boundary="AI_CONTEXT",
                    reversible=True,
                    rollback_strategy="restore exact prior blob",
                    postcondition="hash changed",
                    evidence_required=("E1_STATIC",),
                ),
            ),
        )
        report = analyze(plan, BASE_POLICY)
        self.assertEqual(report.verdict, Verdict.FREEZE)
        self.assertIn("PROTECTED_RESOURCE_MUTATION", codes(report))

    def test_forbidden_boundary_freezes(self) -> None:
        plan = ExecutionPlan(
            plan_id="boundary",
            steps=(Step(id="read", kind=StepKind.READ, resource="x", boundary="PRODUCTION"),),
        )
        report = analyze(plan, BASE_POLICY)
        self.assertEqual(report.verdict, Verdict.FREEZE)
        self.assertIn("BOUNDARY_NOT_ALLOWED", codes(report))

    def test_external_effect_requires_idempotency_key(self) -> None:
        plan = ExecutionPlan(
            plan_id="external",
            steps=(
                Step(
                    id="send",
                    kind=StepKind.EXTERNAL_EFFECT,
                    resource="email:recipient@example.invalid",
                    boundary="EXTERNAL",
                    reversible=False,
                    approval_id="approval-1",
                    postcondition="provider accepted exactly one message",
                    evidence_required=("E3_INTEGRATION",),
                ),
            ),
        )
        report = analyze(plan, BASE_POLICY)
        self.assertEqual(report.verdict, Verdict.FREEZE)
        self.assertIn("MISSING_IDEMPOTENCY_KEY", codes(report))

    def test_irreversible_without_approval_freezes(self) -> None:
        plan = ExecutionPlan(
            plan_id="delete",
            steps=(
                Step(
                    id="delete",
                    kind=StepKind.DELETE,
                    resource="repo:AI-CONTEXT/aux/obsolete.txt",
                    boundary="AI_CONTEXT",
                    reversible=False,
                    postcondition="target absent",
                    evidence_required=("E0_PRESENCE",),
                ),
            ),
        )
        report = analyze(plan, BASE_POLICY)
        self.assertIn("IRREVERSIBLE_WITHOUT_APPROVAL", codes(report))
        self.assertEqual(report.verdict, Verdict.FREEZE)

    def test_approved_terminal_irreversible_can_be_ready(self) -> None:
        plan = ExecutionPlan(
            plan_id="terminal-delete",
            steps=(
                Step(id="inspect", kind=StepKind.READ, resource="repo:AI-CONTEXT/aux/obsolete.txt", boundary="AI_CONTEXT"),
                Step(
                    id="delete",
                    kind=StepKind.DELETE,
                    resource="repo:AI-CONTEXT/aux/obsolete.txt",
                    boundary="AI_CONTEXT",
                    depends_on=("inspect",),
                    reversible=False,
                    approval_id="owner-approval-42",
                    postcondition="target absent",
                    evidence_required=("E0_PRESENCE",),
                ),
            ),
        )
        report = analyze(plan, BASE_POLICY)
        self.assertEqual(report.verdict, Verdict.READY)
        self.assertIn("APPROVED_TERMINAL_IRREVERSIBLE", codes(report))

    def test_nonterminal_irreversible_freezes_and_records_partial_state(self) -> None:
        plan = ExecutionPlan(
            plan_id="unsafe-prefix",
            steps=(
                Step(
                    id="a-delete",
                    kind=StepKind.DELETE,
                    resource="repo:AI-CONTEXT/aux/a.txt",
                    boundary="AI_CONTEXT",
                    reversible=False,
                    approval_id="owner-approval-1",
                    postcondition="a absent",
                    evidence_required=("E0_PRESENCE",),
                ),
                Step(
                    id="b-create",
                    kind=StepKind.CREATE,
                    resource="repo:AI-CONTEXT/aux/b.txt",
                    boundary="AI_CONTEXT",
                    depends_on=("a-delete",),
                    reversible=True,
                    rollback_strategy="delete b",
                    postcondition="b present",
                    evidence_required=("E0_PRESENCE",),
                ),
            ),
        )
        report = analyze(plan, BASE_POLICY)
        self.assertEqual(report.verdict, Verdict.FREEZE)
        self.assertIn("NONTERMINAL_IRREVERSIBLE_MUTATION", codes(report))
        self.assertIn("UNSAFE_PARTIAL_STATE", codes(report))
        self.assertEqual(report.partial_states[0].failure_before_step, "b-create")
        self.assertEqual(report.partial_states[0].residual_resources, ("repo:AI-CONTEXT/aux/a.txt",))

    def test_reversible_prefix_does_not_create_partial_state(self) -> None:
        plan = ExecutionPlan(
            plan_id="safe-prefix",
            steps=(
                Step(
                    id="a-create",
                    kind=StepKind.CREATE,
                    resource="repo:AI-CONTEXT/aux/a.txt",
                    boundary="AI_CONTEXT",
                    reversible=True,
                    rollback_strategy="delete exact created blob",
                    postcondition="a present",
                    evidence_required=("E0_PRESENCE",),
                ),
                Step(
                    id="b-create",
                    kind=StepKind.CREATE,
                    resource="repo:AI-CONTEXT/aux/b.txt",
                    boundary="AI_CONTEXT",
                    depends_on=("a-create",),
                    reversible=True,
                    rollback_strategy="delete exact created blob",
                    postcondition="b present",
                    evidence_required=("E0_PRESENCE",),
                ),
            ),
        )
        report = analyze(plan, BASE_POLICY)
        self.assertEqual(report.verdict, Verdict.READY)
        self.assertEqual(report.partial_states, ())

    def test_missing_mutation_postcondition_and_evidence_freeze(self) -> None:
        plan = ExecutionPlan(
            plan_id="underspecified",
            steps=(
                Step(
                    id="write",
                    kind=StepKind.UPDATE,
                    resource="repo:AI-CONTEXT/aux/a.txt",
                    boundary="AI_CONTEXT",
                    reversible=True,
                    rollback_strategy="restore prior blob",
                ),
            ),
        )
        report = analyze(plan, BASE_POLICY)
        self.assertEqual(report.verdict, Verdict.FREEZE)
        self.assertIn("MISSING_POSTCONDITION", codes(report))
        self.assertIn("MISSING_EVIDENCE_REQUIREMENT", codes(report))

    def test_step_limit_freezes(self) -> None:
        policy = Policy(
            policy_id="small",
            allowed_boundaries=("AI_CONTEXT",),
            protected_resources=(),
            max_steps=1,
        )
        plan = ExecutionPlan(
            plan_id="two",
            steps=(
                Step(id="a", kind=StepKind.READ, resource="a", boundary="AI_CONTEXT"),
                Step(id="b", kind=StepKind.READ, resource="b", boundary="AI_CONTEXT"),
            ),
        )
        report = analyze(plan, policy)
        self.assertEqual(report.verdict, Verdict.FREEZE)
        self.assertIn("STEP_LIMIT_EXCEEDED", codes(report))

    def test_report_hash_is_stable_for_equivalent_plan_order(self) -> None:
        a = Step(id="a", kind=StepKind.READ, resource="a", boundary="AI_CONTEXT")
        b = Step(id="b", kind=StepKind.READ, resource="b", boundary="AI_CONTEXT")
        left = analyze(ExecutionPlan(plan_id="p", steps=(b, a)), BASE_POLICY)
        right = analyze(ExecutionPlan(plan_id="p", steps=(a, b)), BASE_POLICY)
        self.assertEqual(left.plan_hash, right.plan_hash)
        self.assertEqual(left.combined_hash, right.combined_hash)
        self.assertEqual(left.ordered_steps, right.ordered_steps)


if __name__ == "__main__":
    unittest.main()
