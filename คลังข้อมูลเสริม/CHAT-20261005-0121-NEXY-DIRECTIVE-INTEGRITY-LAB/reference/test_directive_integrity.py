from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from directive_integrity import (
    AmbiguityState,
    AuthorizedDelta,
    DirectiveSnapshot,
    ImpactClass,
    IntegrityStatus,
    MutationClass,
    compare_transition,
    main,
    operator_explanation,
)


def snap(**overrides):
    base = dict(
        stage="CIRL",
        action="ACTION_RUN",
        target="project:alpha",
        constraints=("deterministic_required", "max_tokens=4096"),
        scope_in=("project:alpha",),
        scope_out=("repo:NEXY.AI-",),
        side_effects=(),
        authority_refs=("USER_DIRECTIVE:1",),
        ambiguity=AmbiguityState.RESOLVED,
        mutation_class=MutationClass.READ_ONLY,
        impact_class=ImpactClass.LOW,
    )
    base.update(overrides)
    return DirectiveSnapshot(**base)


class DirectiveIntegrityTests(unittest.TestCase):
    def test_digest_is_order_independent_for_set_like_fields(self):
        a = snap(constraints=("b", "a"), scope_in=("z", "a"), authority_refs=("R2", "R1"))
        b = snap(constraints=("a", "b"), scope_in=("a", "z"), authority_refs=("R1", "R2"))
        self.assertEqual(a.digest(), b.digest())

    def test_identical_transition_passes(self):
        parent = snap()
        child = snap(stage="CLE", parent_digest=parent.digest())
        result = compare_transition(parent, child)
        self.assertEqual(result.status, IntegrityStatus.PASS)
        self.assertEqual(result.violations, ())

    def test_scope_narrowing_passes(self):
        parent = snap(scope_in=("project:alpha", "artifact:x"))
        child = snap(stage="CLE", scope_in=("project:alpha",), parent_digest=parent.digest())
        self.assertEqual(compare_transition(parent, child).status, IntegrityStatus.PASS)

    def test_scope_broadening_freezes(self):
        parent = snap()
        child = snap(stage="CLE", scope_in=("project:alpha", "repo:other"), parent_digest=parent.digest())
        result = compare_transition(parent, child)
        self.assertEqual(result.status, IntegrityStatus.FREEZE)
        self.assertEqual([v.code for v in result.violations], ["SCOPE_BROADENED"])

    def test_scope_broadening_can_be_explicitly_reauthorized(self):
        parent = snap()
        child = snap(stage="CLE", scope_in=("project:alpha", "repo:other"), parent_digest=parent.digest())
        grant = AuthorizedDelta(path="/scope_in", evidence_ref="USER_CLARIFICATION:2", reason="user explicitly added repo:other")
        result = compare_transition(parent, child, authorized_deltas=(grant,))
        self.assertEqual(result.status, IntegrityStatus.PASS)
        self.assertEqual(result.violations, ())
        self.assertEqual(result.authorized_deltas, (grant,))

    def test_constraint_drop_freezes(self):
        parent = snap()
        child = snap(stage="CLE", constraints=("deterministic_required",), parent_digest=parent.digest())
        self.assertIn("CONSTRAINT_DROPPED", [v.code for v in compare_transition(parent, child).violations])

    def test_scope_exclusion_removal_freezes(self):
        parent = snap(scope_out=("repo:NEXY.AI-", "prod"))
        child = snap(stage="CLE", scope_out=("repo:NEXY.AI-",), parent_digest=parent.digest())
        self.assertIn("SCOPE_EXCLUSION_REMOVED", [v.code for v in compare_transition(parent, child).violations])

    def test_new_side_effect_freezes(self):
        parent = snap()
        child = snap(stage="CLE", side_effects=("write:file",), parent_digest=parent.digest())
        self.assertIn("SIDE_EFFECT_ADDED", [v.code for v in compare_transition(parent, child).violations])

    def test_action_change_freezes(self):
        parent = snap()
        child = snap(stage="CLE", action="ACTION_EXPORT", parent_digest=parent.digest())
        self.assertIn("ACTION_CHANGED", [v.code for v in compare_transition(parent, child).violations])

    def test_target_change_freezes(self):
        parent = snap()
        child = snap(stage="CLE", target="project:beta", parent_digest=parent.digest())
        self.assertIn("TARGET_CHANGED", [v.code for v in compare_transition(parent, child).violations])

    def test_mutation_escalation_freezes(self):
        parent = snap(mutation_class=MutationClass.READ_ONLY)
        child = snap(stage="CLE", mutation_class=MutationClass.REVERSIBLE_MUTATION, parent_digest=parent.digest())
        self.assertIn("MUTATION_ESCALATED", [v.code for v in compare_transition(parent, child).violations])

    def test_impact_downgrade_needs_evidence(self):
        parent = snap(impact_class=ImpactClass.HIGH)
        child = snap(stage="CLE", impact_class=ImpactClass.LOW, parent_digest=parent.digest())
        self.assertIn("IMPACT_DOWNGRADED_WITHOUT_EVIDENCE", [v.code for v in compare_transition(parent, child).violations])

    def test_impact_downgrade_with_reassessment_passes(self):
        parent = snap(impact_class=ImpactClass.HIGH)
        child = snap(
            stage="CLE",
            impact_class=ImpactClass.LOW,
            risk_reassessment_refs=("RISK_REVIEW:7",),
            parent_digest=parent.digest(),
        )
        self.assertEqual(compare_transition(parent, child).status, IntegrityStatus.PASS)

    def test_ambiguity_resolution_needs_clarification(self):
        parent = snap(ambiguity=AmbiguityState.OPEN)
        child = snap(stage="CLE", ambiguity=AmbiguityState.RESOLVED, parent_digest=parent.digest())
        self.assertIn("AMBIGUITY_RESOLVED_WITHOUT_CLARIFICATION", [v.code for v in compare_transition(parent, child).violations])

    def test_ambiguity_resolution_with_clarification_passes(self):
        parent = snap(ambiguity=AmbiguityState.OPEN)
        child = snap(
            stage="CLE",
            ambiguity=AmbiguityState.RESOLVED,
            clarification_refs=("USER_CLARIFICATION:9",),
            parent_digest=parent.digest(),
        )
        self.assertEqual(compare_transition(parent, child).status, IntegrityStatus.PASS)

    def test_authority_removal_freezes(self):
        parent = snap(authority_refs=("USER_DIRECTIVE:1", "LAW:SAFE"))
        child = snap(stage="CLE", authority_refs=("USER_DIRECTIVE:1",), parent_digest=parent.digest())
        self.assertIn("AUTHORITY_REF_REMOVED", [v.code for v in compare_transition(parent, child).violations])

    def test_parent_digest_mismatch_freezes(self):
        parent = snap()
        child = snap(stage="CLE", parent_digest="0" * 64)
        self.assertIn("PARENT_DIGEST_MISMATCH", [v.code for v in compare_transition(parent, child).violations])

    def test_duplicate_grant_path_is_rejected(self):
        parent = snap()
        child = snap(stage="CLE", action="ACTION_EXPORT", parent_digest=parent.digest())
        grants = (
            AuthorizedDelta("/action", "USER:1", "first"),
            AuthorizedDelta("/action", "USER:2", "second"),
        )
        with self.assertRaisesRegex(ValueError, "duplicate authorization path"):
            compare_transition(parent, child, authorized_deltas=grants)

    def test_operator_explanation_contains_no_hidden_reasoning(self):
        snapshot = snap()
        view = operator_explanation(snapshot)
        self.assertEqual(view["action"], "ACTION_RUN")
        self.assertEqual(view["contract_digest"], snapshot.digest())
        self.assertNotIn("chain_of_thought", view)

    def test_mapping_round_trip_is_stable(self):
        original = snap()
        restored = DirectiveSnapshot.from_mapping(original.canonical_payload())
        self.assertEqual(restored, original)
        self.assertEqual(restored.digest(), original.digest())

    def test_invalid_blank_set_item_rejected(self):
        with self.assertRaisesRegex(ValueError, "blank"):
            snap(scope_in=("project:alpha", "   "))

    def test_cli_compare_exit_codes_are_machine_useful(self):
        parent = snap()
        child_ok = snap(stage="CLE", parent_digest=parent.digest())
        child_bad = snap(stage="CLE", target="project:beta", parent_digest=parent.digest())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "parent.json").write_text(json.dumps(parent.canonical_payload()), encoding="utf-8")
            (root / "ok.json").write_text(json.dumps(child_ok.canonical_payload()), encoding="utf-8")
            (root / "bad.json").write_text(json.dumps(child_bad.canonical_payload()), encoding="utf-8")
            self.assertEqual(main(["compare", str(root / "parent.json"), str(root / "ok.json")]), 0)
            self.assertEqual(main(["compare", str(root / "parent.json"), str(root / "bad.json")]), 2)


if __name__ == "__main__":
    unittest.main()
