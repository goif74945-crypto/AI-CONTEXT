from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "reference_impl" / "trustux.py"
SPEC = importlib.util.spec_from_file_location("trustux", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
trustux = importlib.util.module_from_spec(SPEC)
sys.modules["trustux"] = trustux
SPEC.loader.exec_module(trustux)


def fixture(name: str) -> dict:
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


class TrustUxCompilerTests(unittest.TestCase):
    def test_stable_release_is_visible_only_with_proof(self) -> None:
        card = trustux.compile_and_validate(fixture("stable_release.json"), "OPERATOR")
        self.assertEqual(card.display_mode, "RESULT")
        self.assertTrue(card.result_visible)
        self.assertFalse(card.blocked)
        self.assertEqual(card.primary_action.id, "view_result")
        self.assertIn("RESULT_VISIBLE_ONLY_WITH_RELEASE_PROOF", card.truth_flags)

    def test_stable_without_integrity_hash_is_withheld(self) -> None:
        envelope = fixture("stable_release.json")
        envelope["data"]["integrity_hash"] = ""
        card = trustux.compile_and_validate(envelope, "OPERATOR")
        self.assertEqual(card.display_mode, "HOLD")
        self.assertFalse(card.result_visible)
        self.assertTrue(card.blocked)
        self.assertIsNone(card.result)

    def test_stable_releaseable_false_is_withheld(self) -> None:
        envelope = fixture("stable_release.json")
        envelope["data"]["releaseable"] = False
        card = trustux.compile_and_validate(envelope, "OPERATOR")
        self.assertEqual(card.display_mode, "HOLD")
        self.assertFalse(card.result_visible)

    def test_freeze_is_always_visible_and_hides_result(self) -> None:
        card = trustux.compile_and_validate(fixture("freeze_owner.json"), "OWNER")
        self.assertEqual(card.display_mode, "FREEZE")
        self.assertEqual(card.headline, "System frozen")
        self.assertTrue(card.blocked)
        self.assertFalse(card.result_visible)
        self.assertIsNone(card.result)
        self.assertIn("FREEZE_ALWAYS_VISIBLE", card.truth_flags)

    def test_owner_recover_action_requires_recoverable_true(self) -> None:
        card = trustux.compile_and_validate(fixture("freeze_owner.json"), "OWNER")
        self.assertEqual(card.primary_action.id, "recover")
        self.assertTrue(card.primary_action.requires_confirmation)
        self.assertEqual(card.secondary_actions[0].id, "view_trace")

    def test_operator_never_receives_recover_action_from_presentation(self) -> None:
        card = trustux.compile_and_validate(fixture("freeze_operator.json"), "OPERATOR")
        ids = {card.primary_action.id} if card.primary_action else set()
        ids.update(action.id for action in card.secondary_actions)
        self.assertNotIn("recover", ids)
        self.assertEqual(card.primary_action.id, "view_trace")

    def test_nonrecoverable_freeze_has_no_recover_even_for_owner(self) -> None:
        envelope = fixture("freeze_owner.json")
        envelope["freeze"]["recoverable"] = False
        card = trustux.compile_and_validate(envelope, "OWNER")
        ids = {card.primary_action.id} if card.primary_action else set()
        ids.update(action.id for action in card.secondary_actions)
        self.assertNotIn("recover", ids)

    def test_stop_never_exposes_recover(self) -> None:
        card = trustux.compile_and_validate(fixture("stop.json"), "OWNER")
        self.assertEqual(card.display_mode, "STOP")
        ids = {card.primary_action.id} if card.primary_action else set()
        ids.update(action.id for action in card.secondary_actions)
        self.assertNotIn("recover", ids)

    def test_verifying_is_pending_not_success(self) -> None:
        card = trustux.compile_and_validate(fixture("verifying.json"), "OPERATOR")
        self.assertEqual(card.display_mode, "PENDING")
        self.assertFalse(card.result_visible)
        self.assertIn("PENDING_NEVER_RENDERED_AS_SUCCESS", card.truth_flags)

    def test_ready_operator_can_request_new_directive(self) -> None:
        envelope = {
            "status": "OK",
            "state": "READY",
            "request_id": "req-ready-1",
            "trace_id": "trace-ready-1",
            "data": {},
        }
        card = trustux.compile_and_validate(envelope, "OPERATOR")
        self.assertEqual(card.display_mode, "READY")
        self.assertEqual(card.primary_action.id, "new_directive")

    def test_ready_auditor_gets_read_only_primary(self) -> None:
        envelope = {
            "status": "OK",
            "state": "READY",
            "request_id": "req-ready-2",
            "trace_id": "trace-ready-2",
            "data": {},
        }
        card = trustux.compile_and_validate(envelope, "AUDITOR")
        self.assertEqual(card.primary_action.kind, "READ")
        self.assertEqual(card.primary_action.id, "view_system")

    def test_degraded_status_is_exposed(self) -> None:
        envelope = fixture("verifying.json")
        envelope["status"] = "DEGRADED"
        card = trustux.compile_and_validate(envelope, "OPERATOR")
        self.assertIn("DEGRADED_STATUS_EXPOSED", card.truth_flags)
        self.assertTrue(card.summary.startswith("Degraded system status."))

    def test_unknown_error_code_is_not_interpreted(self) -> None:
        envelope = fixture("freeze_operator.json")
        envelope["error"] = {"code": "NEW_UNKNOWN_CODE"}
        envelope["freeze"].pop("incident_code", None)
        card = trustux.compile_and_validate(envelope, "OPERATOR")
        self.assertEqual(card.incident_code, "NEW_UNKNOWN_CODE")
        self.assertEqual(card.summary, "Execution blocked. Incident code: NEW_UNKNOWN_CODE.")

    def test_invalid_state_fails_closed(self) -> None:
        envelope = fixture("verifying.json")
        envelope["state"] = "MAGIC_SUCCESS"
        with self.assertRaises(trustux.ContractError):
            trustux.compile_and_validate(envelope, "OPERATOR")

    def test_missing_trace_id_fails_closed(self) -> None:
        envelope = fixture("verifying.json")
        envelope.pop("trace_id")
        with self.assertRaises(trustux.ContractError):
            trustux.compile_and_validate(envelope, "OPERATOR")

    def test_invalid_recoverable_type_fails_closed(self) -> None:
        envelope = fixture("freeze_owner.json")
        envelope["freeze"]["recoverable"] = "yes"
        with self.assertRaises(trustux.ContractError):
            trustux.compile_and_validate(envelope, "OWNER")

    def test_deterministic_same_input_same_output(self) -> None:
        envelope = fixture("stable_release.json")
        first = trustux.compile_and_validate(envelope, "OPERATOR").to_dict()
        second = trustux.compile_and_validate(envelope, "OPERATOR").to_dict()
        self.assertEqual(first, second)
        self.assertEqual(first["deterministic_fingerprint"], second["deterministic_fingerprint"])

    def test_role_is_part_of_deterministic_presentation_contract(self) -> None:
        envelope = fixture("freeze_owner.json")
        owner = trustux.compile_and_validate(envelope, "OWNER")
        operator = trustux.compile_and_validate(envelope, "OPERATOR")
        self.assertNotEqual(owner.deterministic_fingerprint, operator.deterministic_fingerprint)
        self.assertEqual(owner.system_state, operator.system_state)

    def test_result_payload_not_visible_while_freeze_even_if_data_contains_output(self) -> None:
        envelope = fixture("freeze_owner.json")
        envelope["data"] = {
            "accepted": True,
            "releaseable": True,
            "integrity_hash": "abc",
            "output": {"danger": "must stay hidden"},
        }
        card = trustux.compile_and_validate(envelope, "OWNER")
        self.assertIsNone(card.result)
        self.assertFalse(card.result_visible)

    def test_public_user_never_gets_mutation_action_on_ready(self) -> None:
        envelope = {
            "status": "OK",
            "state": "READY",
            "request_id": "req-public-1",
            "trace_id": "trace-public-1",
            "data": {},
        }
        card = trustux.compile_and_validate(envelope, "PUBLIC_USER")
        self.assertEqual(card.primary_action.kind, "READ")


if __name__ == "__main__":
    unittest.main(verbosity=2)
