from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conformance" / "truth_surface_checker.py"
SPEC = importlib.util.spec_from_file_location("truth_surface_checker", PATH)
assert SPEC and SPEC.loader
m = importlib.util.module_from_spec(SPEC)
sys.modules["truth_surface_checker"] = m
SPEC.loader.exec_module(m)


def backend(state="READY", status="OK"):
    return {
        "status": status,
        "state": state,
        "request_id": "req-1",
        "trace_id": "trace-1",
        "data": {},
    }


def surface(state="READY", status="OK"):
    return {
        "displayed_status": status,
        "displayed_state": state,
        "headline": "Ready",
        "summary": "System is ready.",
        "result_visible": False,
        "result": None,
        "actions": [],
        "request_id": "req-1",
        "trace_id": "trace-1",
    }


def codes(report):
    return {v.code for v in report.violations}


class TruthSurfaceCheckerTests(unittest.TestCase):
    def test_clean_ready_operator_passes(self):
        self.assertTrue(m.audit_surface(backend(), surface(), "OPERATOR").conformant)

    def test_status_mismatch_detected(self):
        s = surface(); s["displayed_status"] = "DEGRADED"
        self.assertIn("STATUS_MISMATCH", codes(m.audit_surface(backend(), s, "OPERATOR")))

    def test_state_mismatch_detected(self):
        s = surface(); s["displayed_state"] = "STABLE"
        self.assertIn("STATE_MISMATCH", codes(m.audit_surface(backend(), s, "OPERATOR")))

    def test_request_mismatch_detected(self):
        s = surface(); s["request_id"] = "other"
        self.assertIn("REQUEST_ID_MISMATCH", codes(m.audit_surface(backend(), s, "OPERATOR")))

    def test_trace_mismatch_detected(self):
        s = surface(); s["trace_id"] = "other"
        self.assertIn("TRACE_ID_MISMATCH", codes(m.audit_surface(backend(), s, "OPERATOR")))

    def test_visible_result_missing_detected(self):
        s = surface(); s["result_visible"] = True
        self.assertIn("VISIBLE_RESULT_MISSING", codes(m.audit_surface(backend(), s, "OPERATOR")))

    def test_freeze_result_leak_detected(self):
        b = backend("FREEZE", "FREEZE"); b["freeze"] = {"recoverable": True}
        s = surface("FREEZE", "FREEZE"); s["result_visible"] = True; s["result"] = {"stale": True}
        self.assertIn("FREEZE_RESULT_LEAK", codes(m.audit_surface(b, s, "OWNER")))

    def test_freeze_success_copy_detected(self):
        b = backend("FREEZE", "FREEZE"); s = surface("FREEZE", "FREEZE"); s["headline"] = "Successful"
        self.assertIn("FREEZE_SUCCESS_COPY", codes(m.audit_surface(b, s, "OWNER")))

    def test_owner_recover_when_recoverable_passes(self):
        b = backend("FREEZE", "FREEZE"); b["freeze"] = {"recoverable": True}
        s = surface("FREEZE", "FREEZE"); s["actions"] = [{"id":"recover","kind":"MUTATION_REQUEST","requires_backend_authorization":True,"requires_confirmation":True}]
        self.assertTrue(m.audit_surface(b, s, "OWNER").conformant)

    def test_operator_recover_is_violation(self):
        b = backend("FREEZE", "FREEZE"); b["freeze"] = {"recoverable": True}
        s = surface("FREEZE", "FREEZE"); s["actions"] = [{"id":"recover","kind":"MUTATION_REQUEST","requires_backend_authorization":True,"requires_confirmation":True}]
        self.assertIn("RECOVER_VISIBILITY_VIOLATION", codes(m.audit_surface(b, s, "OPERATOR")))

    def test_nonrecoverable_owner_recover_is_violation(self):
        b = backend("FREEZE", "FREEZE"); b["freeze"] = {"recoverable": False}
        s = surface("FREEZE", "FREEZE"); s["actions"] = [{"id":"recover","kind":"MUTATION_REQUEST","requires_backend_authorization":True,"requires_confirmation":True}]
        self.assertIn("RECOVER_VISIBILITY_VIOLATION", codes(m.audit_surface(b, s, "OWNER")))

    def test_freeze_unrelated_mutation_detected(self):
        b = backend("FREEZE", "FREEZE"); s = surface("FREEZE", "FREEZE"); s["actions"] = [{"id":"new_directive","kind":"MUTATION_REQUEST","requires_backend_authorization":True}]
        self.assertIn("FREEZE_ILLEGAL_MUTATION", codes(m.audit_surface(b, s, "OWNER")))

    def test_stop_result_leak_detected(self):
        b = backend("STOP", "STOP"); s = surface("STOP", "STOP"); s["result_visible"] = True; s["result"] = {"x": 1}
        self.assertIn("STOP_RESULT_LEAK", codes(m.audit_surface(b, s, "OWNER")))

    def test_stop_mutation_detected(self):
        b = backend("STOP", "STOP"); s = surface("STOP", "STOP"); s["actions"] = [{"id":"recover","kind":"MUTATION_REQUEST","requires_backend_authorization":True,"requires_confirmation":True}]
        self.assertIn("STOP_MUTATION_ACTION", codes(m.audit_surface(b, s, "OWNER")))

    def test_stop_retry_copy_detected(self):
        b = backend("STOP", "STOP"); s = surface("STOP", "STOP"); s["summary"] = "Try again later"
        self.assertIn("STOP_RETRY_COPY", codes(m.audit_surface(b, s, "OWNER")))

    def test_pending_result_leak_detected_for_each_pending_state(self):
        for state in ["INIT","RUNNING","VERIFYING","CONSENSUS"]:
            with self.subTest(state=state):
                b = backend(state); s = surface(state); s["result_visible"] = True; s["result"] = {"candidate": 1}
                self.assertIn("PENDING_RESULT_LEAK", codes(m.audit_surface(b, s, "OPERATOR")))

    def test_pending_success_copy_detected(self):
        b = backend("VERIFYING"); s = surface("VERIFYING"); s["headline"] = "Verified result"
        self.assertIn("PENDING_SUCCESS_COPY", codes(m.audit_surface(b, s, "OPERATOR")))

    def test_pending_mutation_detected(self):
        b = backend("RUNNING"); s = surface("RUNNING"); s["actions"] = [{"id":"new_directive","kind":"MUTATION_REQUEST","requires_backend_authorization":True}]
        self.assertIn("PENDING_MUTATION_ACTION", codes(m.audit_surface(b, s, "OPERATOR")))

    def test_stable_result_without_release_proof_detected(self):
        b = backend("STABLE"); s = surface("STABLE"); s["result_visible"] = True; s["result"] = {"x":1}
        self.assertIn("RELEASE_PROOF_MISSING", codes(m.audit_surface(b, s, "OPERATOR")))

    def test_stable_result_with_release_proof_passes(self):
        b = backend("STABLE"); b["data"] = {"accepted":True,"releaseable":True,"integrity_hash":"abc"}
        s = surface("STABLE"); s["result_visible"] = True; s["result"] = {"x":1}; s["headline"] = "Verified result"
        self.assertTrue(m.audit_surface(b, s, "OPERATOR").conformant)

    def test_auditor_ready_mutation_detected(self):
        s = surface(); s["actions"] = [{"id":"new_directive","kind":"MUTATION_REQUEST","requires_backend_authorization":True}]
        self.assertIn("ROLE_MUTATION_VISIBILITY", codes(m.audit_surface(backend(), s, "AUDITOR")))

    def test_public_ready_mutation_detected(self):
        s = surface(); s["actions"] = [{"id":"new_directive","kind":"MUTATION_REQUEST","requires_backend_authorization":True}]
        self.assertIn("ROLE_MUTATION_VISIBILITY", codes(m.audit_surface(backend(), s, "PUBLIC_USER")))

    def test_operator_ready_mutation_can_pass_with_auth_flag(self):
        s = surface(); s["actions"] = [{"id":"new_directive","kind":"MUTATION_REQUEST","requires_backend_authorization":True}]
        self.assertTrue(m.audit_surface(backend(), s, "OPERATOR").conformant)

    def test_mutation_without_backend_auth_flag_detected(self):
        s = surface(); s["actions"] = [{"id":"new_directive","kind":"MUTATION_REQUEST"}]
        self.assertIn("BACKEND_AUTH_FLAG_MISSING", codes(m.audit_surface(backend(), s, "OPERATOR")))

    def test_recover_without_confirmation_detected(self):
        b = backend("FREEZE", "FREEZE"); b["freeze"] = {"recoverable": True}
        s = surface("FREEZE", "FREEZE"); s["actions"] = [{"id":"recover","kind":"MUTATION_REQUEST","requires_backend_authorization":True,"requires_confirmation":False}]
        self.assertIn("RECOVER_CONFIRMATION_MISSING", codes(m.audit_surface(b, s, "OWNER")))

    def test_invalid_backend_state_fails_closed(self):
        b = backend(); b["state"] = "MAGIC"
        with self.assertRaises(m.ConformanceInputError): m.audit_surface(b, surface(), "OPERATOR")

    def test_invalid_surface_state_fails_closed(self):
        s = surface(); s["displayed_state"] = "MAGIC"
        with self.assertRaises(m.ConformanceInputError): m.audit_surface(backend(), s, "OPERATOR")

    def test_invalid_role_fails_closed(self):
        with self.assertRaises(m.ConformanceInputError): m.audit_surface(backend(), surface(), "ADMINISH")

    def test_actions_must_be_list(self):
        s = surface(); s["actions"] = "nope"
        with self.assertRaises(m.ConformanceInputError): m.audit_surface(backend(), s, "OPERATOR")

    def test_deterministic_certificate(self):
        a = m.audit_surface(backend(), surface(), "OPERATOR")
        b = m.audit_surface(backend(), surface(), "OPERATOR")
        self.assertEqual(a.to_dict(), b.to_dict())

    def test_certificate_changes_when_violation_set_changes(self):
        a = m.audit_surface(backend(), surface(), "OPERATOR")
        s = surface(); s["trace_id"] = "wrong"
        b = m.audit_surface(backend(), s, "OPERATOR")
        self.assertNotEqual(a.certificate_fingerprint, b.certificate_fingerprint)

    def test_assert_conformant_raises_on_violation(self):
        s = surface(); s["trace_id"] = "wrong"
        with self.assertRaises(AssertionError): m.assert_conformant(backend(), s, "OPERATOR")


if __name__ == "__main__":
    unittest.main(verbosity=2)
