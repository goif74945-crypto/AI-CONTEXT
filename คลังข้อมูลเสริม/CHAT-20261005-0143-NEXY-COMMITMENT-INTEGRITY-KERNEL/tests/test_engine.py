from __future__ import annotations

import itertools
import unittest

from ncik.engine import evaluate_commitment, fingerprint, transition, validate_revision, with_supersedes
from ncik.model import (
    AuthorityState,
    BindingType,
    CapabilityManifest,
    Commitment,
    CommitmentState,
    Decision,
    EffectClass,
    EvidenceBundle,
    EvidenceClass,
    ExecutionBinding,
    TemporalMode,
)


def caps(**overrides):
    data = dict(supported_bindings=frozenset(BindingType),supported_effects=frozenset(EffectClass),evidence_classes=frozenset(EvidenceClass))
    data.update(overrides)
    return CapabilityManifest(**data)


def commitment(**overrides):
    data = dict(commitment_id="C-001",revision=1,issuer="NEXY",beneficiary="user",objective="Deliver verified summary",deliverable="A verified summary artifact",scope=("project:alpha",),protected_scope=("project:omega",),temporal_mode=TemporalMode.IMMEDIATE,effect=EffectClass.READ_ONLY,authority_state=AuthorityState.RESOLVED,authority_refs=("user-directive:1",),required_evidence=(EvidenceClass.E2_UNIT,),binding=ExecutionBinding(BindingType.INLINE_SESSION,"session:1",False,"capability:1"),trigger_spec=None,deadline_spec=None,supersedes_fingerprint=None,metadata={"source":"test"})
    data.update(overrides)
    return Commitment(**data)


class EvaluationTests(unittest.TestCase):
    def test_immediate_commitment_allowed(self): self.assertEqual(evaluate_commitment(commitment(),caps()).decision,Decision.ALLOW_COMMITMENT)
    def test_authority_conflict_freezes(self):
        r=evaluate_commitment(commitment(authority_state=AuthorityState.CONFLICT),caps()); self.assertEqual(r.decision,Decision.FREEZE); self.assertIn("AUTHORITY_CONFLICT",r.reason_codes)
    def test_unresolved_authority_asks(self): self.assertEqual(evaluate_commitment(commitment(authority_state=AuthorityState.UNRESOLVED),caps()).decision,Decision.ASK_AUTHORITY)
    def test_scheduled_requires_scheduled_binding(self):
        r=evaluate_commitment(commitment(temporal_mode=TemporalMode.SCHEDULED,deadline_spec="2026-10-06T09:00+07:00"),caps()); self.assertEqual(r.decision,Decision.FREEZE); self.assertIn("TEMPORAL_BINDING_MISMATCH",r.reason_codes)
    def test_scheduled_requires_durable_binding(self):
        c=commitment(temporal_mode=TemporalMode.SCHEDULED,deadline_spec="2026-10-06T09:00+07:00",binding=ExecutionBinding(BindingType.SCHEDULED_TASK,"task:1",False,"scheduler-proof:1")); r=evaluate_commitment(c,caps()); self.assertIn("FUTURE_COMMITMENT_NOT_DURABLE",r.reason_codes)
    def test_scheduled_with_durable_binding_allowed(self):
        c=commitment(temporal_mode=TemporalMode.SCHEDULED,deadline_spec="2026-10-06T09:00+07:00",binding=ExecutionBinding(BindingType.SCHEDULED_TASK,"task:1",True,"scheduler-proof:1")); self.assertEqual(evaluate_commitment(c,caps()).decision,Decision.ALLOW_COMMITMENT)
    def test_conditional_requires_trigger(self):
        c=commitment(temporal_mode=TemporalMode.CONDITIONAL,binding=ExecutionBinding(BindingType.CONDITION_WATCH,"watch:1",True,"watch-proof:1")); self.assertIn("MISSING_TRIGGER_SPEC",evaluate_commitment(c,caps()).reason_codes)
    def test_recurring_requires_trigger(self):
        c=commitment(temporal_mode=TemporalMode.RECURRING,binding=ExecutionBinding(BindingType.RECURRING_TASK,"recurring:1",True,"recurring-proof:1")); self.assertIn("MISSING_TRIGGER_SPEC",evaluate_commitment(c,caps()).reason_codes)
    def test_missing_scheduler_capability_freezes(self):
        c=commitment(temporal_mode=TemporalMode.SCHEDULED,deadline_spec="tomorrow 09:00",binding=ExecutionBinding(BindingType.SCHEDULED_TASK,"task:1",True,"proof:1")); self.assertIn("EXECUTION_CAPABILITY_UNAVAILABLE",evaluate_commitment(c,caps(supported_bindings=frozenset({BindingType.INLINE_SESSION}))).reason_codes)
    def test_missing_effect_capability_freezes(self): self.assertIn("EFFECT_CAPABILITY_UNAVAILABLE",evaluate_commitment(commitment(effect=EffectClass.EXTERNAL_SIDE_EFFECT),caps(supported_effects=frozenset({EffectClass.READ_ONLY}))).reason_codes)
    def test_missing_evidence_capability_freezes(self): self.assertTrue(any(x.startswith("EVIDENCE_CAPABILITY_MISSING:") for x in evaluate_commitment(commitment(),caps(evidence_classes=frozenset({EvidenceClass.E0_PRESENCE}))).reason_codes))
    def test_protected_scope_collision_freezes(self): self.assertIn("PROTECTED_SCOPE_COLLISION",evaluate_commitment(commitment(scope=("project:alpha","project:omega")),caps()).reason_codes)
    def test_empty_scope_freezes(self): self.assertIn("EMPTY_SCOPE",evaluate_commitment(commitment(scope=()),caps()).reason_codes)
    def test_missing_authority_provenance_freezes(self): self.assertIn("MISSING_AUTHORITY_PROVENANCE",evaluate_commitment(commitment(authority_refs=()),caps()).reason_codes)
    def test_missing_binding_proof_freezes(self): self.assertIn("MISSING_EXECUTION_BINDING_PROOF",evaluate_commitment(commitment(binding=ExecutionBinding(BindingType.INLINE_SESSION,"",False,"")),caps()).reason_codes)
    def test_fingerprint_stable_across_scope_order(self):
        base=commitment(scope=("project:a","project:b","project:c"),authority_refs=("r2","r1")); expected=fingerprint(base)
        for perm in itertools.permutations(base.scope): self.assertEqual(fingerprint(commitment(scope=perm,authority_refs=("r1","r2"))),expected)
    def test_fingerprint_whitespace_normalization(self): self.assertEqual(fingerprint(commitment(objective="Deliver   verified\n summary")),fingerprint(commitment(objective="Deliver verified summary")))


class RevisionTests(unittest.TestCase):
    def test_valid_revision(self):
        old=commitment(); self.assertTrue(validate_revision(old,with_supersedes(old,commitment(revision=2,deliverable="New deliverable"))).allowed)
    def test_revision_must_increment_by_one(self):
        old=commitment(); r=validate_revision(old,with_supersedes(old,commitment(revision=3))); self.assertIn("REVISION_NOT_MONOTONIC",r.reason_codes)
    def test_revision_cannot_change_issuer(self):
        old=commitment(); self.assertIn("ISSUER_CHANGED",validate_revision(old,with_supersedes(old,commitment(revision=2,issuer="other"))).reason_codes)
    def test_revision_cannot_change_beneficiary(self):
        old=commitment(); self.assertIn("BENEFICIARY_CHANGED",validate_revision(old,with_supersedes(old,commitment(revision=2,beneficiary="other"))).reason_codes)
    def test_revision_requires_exact_supersedes_fingerprint(self): self.assertIn("SUPERSEDES_FINGERPRINT_MISMATCH",validate_revision(commitment(),commitment(revision=2,supersedes_fingerprint="deadbeef")).reason_codes)
    def test_revision_requires_resolved_authority(self):
        old=commitment(); self.assertIn("REVISED_AUTHORITY_NOT_RESOLVED",validate_revision(old,with_supersedes(old,commitment(revision=2,authority_state=AuthorityState.UNRESOLVED))).reason_codes)


class StateMachineTests(unittest.TestCase):
    def test_happy_path_fulfills_with_evidence(self):
        c=commitment(); s=transition(c,CommitmentState.DRAFT,"ACCEPT").current; s=transition(c,s,"ACTIVATE").current; e=EvidenceBundle(fingerprint(c),1,frozenset({EvidenceClass.E2_UNIT}),("test:1",),"PASS"); self.assertEqual(transition(c,s,"COMPLETE",e).current,CommitmentState.FULFILLED)
    def test_complete_requires_evidence(self):
        with self.assertRaisesRegex(ValueError,"COMPLETION_EVIDENCE_REQUIRED"): transition(commitment(),CommitmentState.ACTIVE,"COMPLETE")
    def test_complete_requires_pass(self):
        c=commitment(); e=EvidenceBundle(fingerprint(c),1,frozenset({EvidenceClass.E2_UNIT}),("test:1",),"FAIL")
        with self.assertRaisesRegex(ValueError,"COMPLETION_EVIDENCE_NOT_PASS"): transition(c,CommitmentState.ACTIVE,"COMPLETE",e)
    def test_complete_rejects_stale_target(self):
        c=commitment(); e=EvidenceBundle("0"*64,1,frozenset({EvidenceClass.E2_UNIT}),("test:1",),"PASS")
        with self.assertRaisesRegex(ValueError,"TARGET_MISMATCH"): transition(c,CommitmentState.ACTIVE,"COMPLETE",e)
    def test_complete_rejects_wrong_revision(self):
        c=commitment(); e=EvidenceBundle(fingerprint(c),2,frozenset({EvidenceClass.E2_UNIT}),("test:1",),"PASS")
        with self.assertRaisesRegex(ValueError,"REVISION_MISMATCH"): transition(c,CommitmentState.ACTIVE,"COMPLETE",e)
    def test_complete_requires_refs(self):
        c=commitment(); e=EvidenceBundle(fingerprint(c),1,frozenset({EvidenceClass.E2_UNIT}),(),"PASS")
        with self.assertRaisesRegex(ValueError,"REFS_REQUIRED"): transition(c,CommitmentState.ACTIVE,"COMPLETE",e)
    def test_complete_requires_all_declared_evidence_classes(self):
        c=commitment(required_evidence=(EvidenceClass.E1_STATIC,EvidenceClass.E2_UNIT)); e=EvidenceBundle(fingerprint(c),1,frozenset({EvidenceClass.E2_UNIT}),("test:1",),"PASS")
        with self.assertRaisesRegex(ValueError,"CLASS_MISSING"): transition(c,CommitmentState.ACTIVE,"COMPLETE",e)
    def test_block_and_resume(self):
        c=commitment(); b=transition(c,CommitmentState.ACTIVE,"BLOCK").current; self.assertEqual(transition(c,b,"RESUME").current,CommitmentState.ACTIVE)
    def test_cancel_is_terminal(self):
        c=commitment(); cancelled=transition(c,CommitmentState.ACTIVE,"CANCEL").current
        with self.assertRaisesRegex(ValueError,"TERMINAL_STATE_IMMUTABLE"): transition(c,cancelled,"ACTIVATE")
    def test_failed_is_terminal(self):
        c=commitment(); failed=transition(c,CommitmentState.ACTIVE,"FAIL").current
        with self.assertRaisesRegex(ValueError,"TERMINAL_STATE_IMMUTABLE"): transition(c,failed,"RESUME")
    def test_illegal_transition_rejected(self):
        with self.assertRaisesRegex(ValueError,"ILLEGAL_TRANSITION"): transition(commitment(),CommitmentState.DRAFT,"COMPLETE")
    def test_supersede_from_accepted(self): self.assertEqual(transition(commitment(),CommitmentState.ACCEPTED,"SUPERSEDE").current,CommitmentState.SUPERSEDED)


if __name__ == "__main__":
    unittest.main()
