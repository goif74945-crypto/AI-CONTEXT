from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from freeze_bridge import FreezeBridgeError, FreezeEvent, compile_mapping


BASE = {
    "protocol_version": "1.1",
    "event_id": "evt-001",
    "reason_code": "MISSING_REQUIRED_INPUT",
    "status": "FROZEN",
    "blocking_layer": "TASK_CONTRACT",
    "recovery_owner": "USER",
    "disclosure": "PUBLIC",
    "locale": "en",
    "dependency_recheck_safe": False,
    "missing_inputs": ["target_branch", "expected_head"],
    "evidence_refs": ["public:task-contract/42"],
    "authorized_recovery_intents": [
        "PROVIDE_REQUIRED_INPUT",
        "ADJUST_SCOPE",
        "ESCALATE_OPERATOR",
    ],
}


class FreezeBridgeTests(unittest.TestCase):
    def test_missing_input_explanation_preserves_reason_without_ui_authority(self) -> None:
        result = compile_mapping(BASE)
        self.assertEqual(result["reason_code"], "MISSING_REQUIRED_INPUT")
        self.assertEqual(result["required_inputs"], ["expected_head", "target_branch"])
        self.assertEqual(
            result["eligible_recovery_intents"],
            ["PROVIDE_REQUIRED_INPUT", "ADJUST_SCOPE"],
        )
        self.assertNotIn("ESCALATE_OPERATOR", result["eligible_recovery_intents"])
        self.assertTrue(result["downstream_ui_authority_required"])

    def test_sibling_boundary_excludes_role_display_mode_and_ui_actions(self) -> None:
        result = compile_mapping(BASE)
        forbidden = {
            "role",
            "display_mode",
            "primary_action",
            "secondary_actions",
            "actions",
            "recover",
            "requires_backend_authorization",
            "requires_confirmation",
        }
        self.assertTrue(forbidden.isdisjoint(result.keys()))
        serialized = json.dumps(result, ensure_ascii=False).lower()
        self.assertNotIn('"role"', serialized)
        self.assertNotIn('"display_mode"', serialized)
        self.assertNotIn('"recover"', serialized)

    def test_output_is_deterministic_under_input_order_changes(self) -> None:
        a = copy.deepcopy(BASE)
        b = copy.deepcopy(BASE)
        b["missing_inputs"] = list(reversed(b["missing_inputs"]))
        b["evidence_refs"] = list(reversed(b["evidence_refs"]))
        b["authorized_recovery_intents"] = list(reversed(b["authorized_recovery_intents"]))
        self.assertEqual(compile_mapping(a), compile_mapping(b))

    def test_unknown_reason_never_infers_specific_cause(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["reason_code"] = "SOMETHING_NEW"
        payload["dependency_recheck_safe"] = True
        payload["authorized_recovery_intents"] = [
            "ACKNOWLEDGE_STATE",
            "ESCALATE_OPERATOR",
            "RECHECK_DEPENDENCY",
        ]
        result = compile_mapping(payload)
        self.assertEqual(result["reason_code"], "UNKNOWN_REASON")
        self.assertIn("cannot safely classify", result["summary"])
        self.assertFalse(result["dependency_recheck_safe"])
        self.assertEqual(
            result["eligible_recovery_intents"],
            ["ESCALATE_OPERATOR", "ACKNOWLEDGE_STATE"],
        )

    def test_security_restricted_hides_evidence_and_recheck(self) -> None:
        payload = copy.deepcopy(BASE)
        payload.update(
            {
                "reason_code": "SECURITY_INTEGRITY",
                "disclosure": "RESTRICTED",
                "dependency_recheck_safe": True,
                "evidence_refs": ["secret:incident/9", "public:notice/2"],
                "authorized_recovery_intents": [
                    "RECHECK_DEPENDENCY",
                    "ESCALATE_OPERATOR",
                    "ACKNOWLEDGE_STATE",
                    "REFRESH_EVIDENCE",
                ],
            }
        )
        result = compile_mapping(payload)
        self.assertEqual(result["evidence_refs"], [])
        self.assertFalse(result["dependency_recheck_safe"])
        self.assertEqual(
            result["eligible_recovery_intents"],
            ["ESCALATE_OPERATOR", "ACKNOWLEDGE_STATE"],
        )

    def test_restricted_nonsecurity_allows_public_refs_only(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["reason_code"] = "INSUFFICIENT_EVIDENCE"
        payload["disclosure"] = "RESTRICTED"
        payload["evidence_refs"] = ["internal:trace/5", "public:proof/7", "secret:key/1"]
        payload["authorized_recovery_intents"] = ["REFRESH_EVIDENCE"]
        result = compile_mapping(payload)
        self.assertEqual(result["evidence_refs"], ["public:proof/7"])

    def test_dependency_recheck_requires_flag_policy_and_upstream_intent(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["reason_code"] = "DEPENDENCY_UNAVAILABLE"
        payload["dependency_recheck_safe"] = True
        payload["authorized_recovery_intents"] = ["ACKNOWLEDGE_STATE"]
        no_recheck = compile_mapping(payload)
        self.assertFalse(no_recheck["dependency_recheck_safe"])

        payload["authorized_recovery_intents"] = ["RECHECK_DEPENDENCY", "ACKNOWLEDGE_STATE"]
        recheck = compile_mapping(payload)
        self.assertTrue(recheck["dependency_recheck_safe"])

        payload["dependency_recheck_safe"] = False
        flag_off = compile_mapping(payload)
        self.assertFalse(flag_off["dependency_recheck_safe"])

    def test_upstream_intent_not_allowed_by_reason_is_removed(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["reason_code"] = "PERMISSION_DENIED"
        payload["authorized_recovery_intents"] = [
            "PROVIDE_REQUIRED_INPUT",
            "REQUEST_AUTHORITY_REVIEW",
        ]
        result = compile_mapping(payload)
        self.assertEqual(result["eligible_recovery_intents"], ["REQUEST_AUTHORITY_REVIEW"])

    def test_thai_locale_changes_text_not_machine_semantics(self) -> None:
        english = compile_mapping(BASE)
        payload = copy.deepcopy(BASE)
        payload["locale"] = "th"
        thai = compile_mapping(payload)
        self.assertIn("ข้อมูล", thai["title"])
        self.assertIn("เดา", thai["summary"])
        for key in (
            "event_id",
            "status",
            "reason_code",
            "blocking_layer",
            "recovery_owner",
            "required_inputs",
            "eligible_recovery_intents",
            "evidence_refs",
            "disclosure",
            "dependency_recheck_safe",
            "downstream_ui_authority_required",
        ):
            self.assertEqual(english[key], thai[key])
        self.assertNotEqual(english["fingerprint"], thai["fingerprint"])

    def test_non_missing_reason_does_not_echo_missing_input_ids(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["reason_code"] = "AUTHORITY_CONFLICT"
        payload["authorized_recovery_intents"] = ["RESOLVE_AUTHORITY_CONFLICT"]
        result = compile_mapping(payload)
        self.assertEqual(result["required_inputs"], [])

    def test_control_characters_are_rejected(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["blocking_layer"] = "CORE\nINJECT"
        with self.assertRaises(FreezeBridgeError):
            compile_mapping(payload)

    def test_invalid_recovery_intent_is_rejected(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["authorized_recovery_intents"] = ["FORCE_BYPASS"]
        with self.assertRaises(FreezeBridgeError):
            compile_mapping(payload)

    def test_unsupported_protocol_is_rejected(self) -> None:
        for version in ("1.0", "2.0"):
            with self.subTest(version=version):
                payload = copy.deepcopy(BASE)
                payload["protocol_version"] = version
                with self.assertRaises(FreezeBridgeError):
                    compile_mapping(payload)

    def test_fingerprint_changes_when_authorized_intents_change(self) -> None:
        a = compile_mapping(BASE)
        payload = copy.deepcopy(BASE)
        payload["authorized_recovery_intents"] = ["ACKNOWLEDGE_STATE"]
        b = compile_mapping(payload)
        self.assertNotEqual(a["fingerprint"], b["fingerprint"])

    def test_context_label_is_not_reflected_to_user_output(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["context_label"] = "<script>alert(1)</script>"
        result = compile_mapping(payload)
        serialized = json.dumps(result, ensure_ascii=False)
        self.assertNotIn("<script>", serialized)
        self.assertNotIn("alert(1)", serialized)

    def test_validation_rejects_non_object_event(self) -> None:
        with self.assertRaises(FreezeBridgeError):
            FreezeEvent.from_mapping([])  # type: ignore[arg-type]

    def test_required_text_validation_paths(self) -> None:
        cases = [
            ("event_id", None),
            ("event_id", "   "),
            ("event_id", "x" * 129),
            ("blocking_layer", 42),
            ("blocking_layer", " "),
            ("blocking_layer", "x" * 97),
        ]
        for key, value in cases:
            with self.subTest(key=key, value_type=type(value).__name__):
                payload = copy.deepcopy(BASE)
                payload[key] = value
                with self.assertRaises(FreezeBridgeError):
                    compile_mapping(payload)

    def test_optional_context_label_validation_paths(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["context_label"] = "   "
        self.assertEqual(compile_mapping(payload)["event_id"], "evt-001")

        for value in [42, "bad\nlabel", "x" * 161]:
            with self.subTest(value_type=type(value).__name__):
                payload = copy.deepcopy(BASE)
                payload["context_label"] = value
                with self.assertRaises(FreezeBridgeError):
                    compile_mapping(payload)

    def test_list_validation_and_dedup_paths(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["missing_inputs"] = None
        payload["evidence_refs"] = None
        result = compile_mapping(payload)
        self.assertEqual(result["required_inputs"], [])
        self.assertEqual(result["evidence_refs"], [])

        payload = copy.deepcopy(BASE)
        payload["missing_inputs"] = ["alpha", "alpha", "beta"]
        result = compile_mapping(payload)
        self.assertEqual(result["required_inputs"], ["alpha", "beta"])

        for key, value in [
            ("missing_inputs", "not-a-list"),
            ("missing_inputs", ["x"] * 25),
            ("evidence_refs", 123),
            ("evidence_refs", ["x" * 161]),
        ]:
            with self.subTest(key=key):
                payload = copy.deepcopy(BASE)
                payload[key] = value
                with self.assertRaises(FreezeBridgeError):
                    compile_mapping(payload)

    def test_enum_and_boolean_validation_paths(self) -> None:
        for key, value in [
            ("reason_code", 123),
            ("status", 123),
            ("status", "NOPE"),
            ("recovery_owner", "NOPE"),
            ("disclosure", "NOPE"),
            ("locale", "xx"),
            ("dependency_recheck_safe", "true"),
        ]:
            with self.subTest(key=key):
                payload = copy.deepcopy(BASE)
                payload[key] = value
                with self.assertRaises(FreezeBridgeError):
                    compile_mapping(payload)

    def test_recovery_intent_collection_validation_paths(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["authorized_recovery_intents"] = ["ACKNOWLEDGE_STATE", "ACKNOWLEDGE_STATE"]
        result = compile_mapping(payload)
        self.assertEqual(result["eligible_recovery_intents"], ["ACKNOWLEDGE_STATE"])

        for value in ["ACKNOWLEDGE_STATE", ["ACKNOWLEDGE_STATE"] * 9]:
            with self.subTest(value_type=type(value).__name__):
                payload = copy.deepcopy(BASE)
                payload["authorized_recovery_intents"] = value
                with self.assertRaises(FreezeBridgeError):
                    compile_mapping(payload)

    def test_cli_round_trip(self) -> None:
        root = Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [sys.executable, "-m", "freeze_bridge", "--compact"],
            cwd=root,
            input=json.dumps(BASE),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["event_id"], "evt-001")
        self.assertTrue(result["downstream_ui_authority_required"])

    def test_cli_returns_code_2_on_invalid_json_shape(self) -> None:
        root = Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [sys.executable, "-m", "freeze_bridge"],
            cwd=root,
            input="[]",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        error = json.loads(proc.stderr)
        self.assertEqual(error["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
