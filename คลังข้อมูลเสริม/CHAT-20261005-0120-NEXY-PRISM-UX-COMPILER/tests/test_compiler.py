from __future__ import annotations

import unittest

from nexy_prism import (
    Action, Confirmation, DetailLevel, EvidenceStatus, RiskLevel, Role,
    SurfaceInput, SystemState, TrustLabel, assert_plan_valid, compile_surface,
)


def make_input(**overrides) -> SurfaceInput:
    base = dict(
        system_state=SystemState.STABLE,
        role=Role.OWNER,
        evidence_status=EvidenceStatus.PASS,
        requested_action=Action.VIEW_RESULT,
        risk=RiskLevel.LOW,
        preferred_detail=DetailLevel.COMPACT,
        backend_authorized=True,
        release_authorized=True,
        recoverable=False,
        irreversible=False,
        incident_code=None,
        blocking_layer=None,
        backend_reason_code=None,
    )
    base.update(overrides)
    return SurfaceInput(**base)


class PrismCompilerTests(unittest.TestCase):
    def test_verified_stable_result_is_viewable(self):
        inp = make_input()
        plan = compile_surface(inp)
        self.assertTrue(plan.action.enabled)
        self.assertEqual(plan.trust_label, TrustLabel.VERIFIED_FINAL)
        self.assertEqual(plan.detail_level, DetailLevel.COMPACT)
        self.assertIn("OUTPUT_RELEASE:AUTHORIZED", plan.mandatory_disclosures)
        assert_plan_valid(inp, plan)

    def test_backend_deny_can_never_be_widened(self):
        inp = make_input(backend_authorized=False, backend_reason_code="FORBIDDEN")
        plan = compile_surface(inp)
        self.assertFalse(plan.action.enabled)
        self.assertEqual(plan.action.reason_code, "FORBIDDEN")
        assert_plan_valid(inp, plan)

    def test_freeze_operator_cannot_submit(self):
        inp = make_input(
            system_state=SystemState.FREEZE, role=Role.OPERATOR,
            requested_action=Action.SUBMIT_DIRECTIVE, release_authorized=False,
            recoverable=True, incident_code="FRZ-001", blocking_layer="LAW",
        )
        plan = compile_surface(inp)
        self.assertFalse(plan.action.enabled)
        self.assertEqual(plan.banner, "FREEZE")
        self.assertEqual(plan.trust_label, TrustLabel.FROZEN)
        self.assertEqual(plan.detail_level, DetailLevel.FORENSIC)
        assert_plan_valid(inp, plan)

    def test_owner_can_recover_only_when_backend_allows_and_recoverable(self):
        inp = make_input(
            system_state=SystemState.FREEZE,
            requested_action=Action.RECOVER_FREEZE,
            release_authorized=False, recoverable=True,
            incident_code="FRZ-002", blocking_layer="CORE",
        )
        plan = compile_surface(inp)
        self.assertTrue(plan.action.enabled)
        self.assertEqual(plan.action.confirmation, Confirmation.CONFIRM)
        assert_plan_valid(inp, plan)

        denied = make_input(
            system_state=SystemState.FREEZE,
            requested_action=Action.RECOVER_FREEZE,
            release_authorized=False, recoverable=False,
            incident_code="FRZ-003", blocking_layer="CORE",
        )
        denied_plan = compile_surface(denied)
        self.assertFalse(denied_plan.action.enabled)
        assert_plan_valid(denied, denied_plan)

    def test_auditor_never_gets_config_surface(self):
        inp = make_input(role=Role.AUDITOR, requested_action=Action.CONFIG_CHANGE)
        plan = compile_surface(inp)
        self.assertFalse(plan.action.enabled)
        self.assertEqual(plan.action.reason_code, "ROLE_SURFACE_DENY")
        assert_plan_valid(inp, plan)

    def test_irreversible_action_forces_typed_confirmation_and_forensic_detail(self):
        inp = make_input(
            requested_action=Action.HARD_DELETE,
            risk=RiskLevel.HIGH,
            irreversible=True,
        )
        plan = compile_surface(inp)
        self.assertEqual(plan.action.confirmation, Confirmation.TYPE_TO_CONFIRM)
        self.assertEqual(plan.detail_level, DetailLevel.FORENSIC)
        assert_plan_valid(inp, plan)

    def test_user_compact_preference_cannot_hide_high_risk_truth(self):
        inp = make_input(
            requested_action=Action.SUBMIT_DIRECTIVE,
            risk=RiskLevel.CRITICAL,
            preferred_detail=DetailLevel.COMPACT,
        )
        plan = compile_surface(inp)
        self.assertEqual(plan.detail_level, DetailLevel.FORENSIC)
        self.assertIn("DETAIL_RAISED_TO_TRUTH_FLOOR", plan.reasons)
        assert_plan_valid(inp, plan)

    def test_unverified_state_never_looks_final(self):
        inp = make_input(
            evidence_status=EvidenceStatus.NOT_VERIFIED,
            release_authorized=False,
        )
        plan = compile_surface(inp)
        self.assertFalse(plan.action.enabled)
        self.assertNotEqual(plan.trust_label, TrustLabel.VERIFIED_FINAL)
        assert_plan_valid(inp, plan)

    def test_inconsistent_release_flags_fail_closed(self):
        inp = make_input(
            system_state=SystemState.RUNNING,
            evidence_status=EvidenceStatus.NOT_VERIFIED,
            release_authorized=True,
            requested_action=Action.VIEW_RESULT,
        )
        plan = compile_surface(inp)
        self.assertFalse(plan.action.enabled)
        self.assertEqual(plan.trust_label, TrustLabel.CONTRACT_CONFLICT)
        self.assertEqual(plan.banner, "CONTRACT_CONFLICT")
        assert_plan_valid(inp, plan)

    def test_stop_only_allows_diagnostic_read(self):
        trace_inp = make_input(
            system_state=SystemState.STOP,
            requested_action=Action.OPEN_TRACE,
            evidence_status=EvidenceStatus.FAIL,
            release_authorized=False,
        )
        trace_plan = compile_surface(trace_inp)
        self.assertTrue(trace_plan.action.enabled)
        assert_plan_valid(trace_inp, trace_plan)

        mutate_inp = make_input(
            system_state=SystemState.STOP,
            requested_action=Action.CONFIG_CHANGE,
            evidence_status=EvidenceStatus.FAIL,
            release_authorized=False,
        )
        mutate_plan = compile_surface(mutate_inp)
        self.assertFalse(mutate_plan.action.enabled)
        assert_plan_valid(mutate_inp, mutate_plan)

    def test_fingerprint_is_deterministic(self):
        inp = make_input(
            preferred_detail=DetailLevel.FORENSIC,
            requested_action=Action.EXPORT_ARTIFACT,
        )
        a = compile_surface(inp)
        b = compile_surface(inp)
        self.assertEqual(a.fingerprint, b.fingerprint)
        self.assertEqual(a.to_primitive(), b.to_primitive())
        assert_plan_valid(inp, a)


if __name__ == "__main__":
    unittest.main()
