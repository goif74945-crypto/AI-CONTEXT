from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from freeze_bridge import FreezeBridgeError, FreezeEvent, compile_mapping


BASE = {
    "protocol_version": "1.0",
    "event_id": "evt-001",
    "reason_code": "MISSING_REQUIRED_INPUT",
    "status": "FROZEN",
    "blocking_layer": "TASK_CONTRACT",
    "recovery_owner": "USER",
    "disclosure": "PUBLIC",
    "locale": "en",
    "retryable": False,
    "missing_inputs": ["target_branch", "expected_head"],
    "evidence_refs": ["public:task-contract/42"],
    "authorized_actions": ["PROVIDE_MISSING_INPUT", "CHANGE_SCOPE", "CONTACT_OPERATOR"],
}


class FreezeBridgeTests(unittest.TestCase):
    def test_missing_input_card_is_actionable_without_guessing(self) -> None:
        result = compile_mapping(BASE)
        self.assertEqual(result["reason_code"], "MISSING_REQUIRED_INPUT")
        self.assertEqual(result["needed"], ["expected_head", "target_branch"])
        self.assertEqual(
            [action["code"] for action in result["actions"]],
            ["PROVIDE_MISSING_INPUT", "CHANGE_SCOPE"],
        )
        self.assertNotIn("CONTACT_OPERATOR", [action["code"] for action in result["actions"]])

    def test_output_is_deterministic_under_input_order_changes(self) -> None:
        a = copy.deepcopy(BASE)
        b = copy.deepcopy(BASE)
        b["missing_inputs"] = list(reversed(b["missing_inputs"]))
        b["evidence_refs"] = list(reversed(b["evidence_refs"]))
        b["authorized_actions"] = list(reversed(b["authorized_actions"]))
        self.assertEqual(compile_mapping(a), compile_mapping(b))

    def test_unknown_reason_never_infers_specific_cause(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["reason_code"] = "SOMETHING_NEW"
        payload["authorized_actions"] = ["ACKNOWLEDGE", "CONTACT_OPERATOR", "RETRY_AFTER_DEPENDENCY"]
        result = compile_mapping(payload)
        self.assertEqual(result["reason_code"], "UNKNOWN_REASON")
        self.assertIn("cannot safely classify", result["summary"])
        self.assertFalse(result["retryable"])
        self.assertEqual([a["code"] for a in result["actions"]], ["CONTACT_OPERATOR", "ACKNOWLEDGE"])

    def test_security_restricted_hides_nonpublic_evidence_and_retry(self) -> None:
        payload = copy.deepcopy(BASE)
        payload.update(
            {
                "reason_code": "SECURITY_INTEGRITY",
                "disclosure": "RESTRICTED",
                "retryable": True,
                "evidence_refs": ["secret:incident/9", "public:notice/2"],
                "authorized_actions": ["RETRY_AFTER_DEPENDENCY", "CONTACT_OPERATOR", "ACKNOWLEDGE", "OPEN_EVIDENCE"],
            }
        )
        result = compile_mapping(payload)
        self.assertEqual(result["evidence_refs"], [])
        self.assertFalse(result["retryable"])
        self.assertEqual([a["code"] for a in result["actions"]], ["CONTACT_OPERATOR", "ACKNOWLEDGE"])

    def test_restricted_nonsecurity_allows_public_refs_only(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["reason_code"] = "INSUFFICIENT_EVIDENCE"
        payload["disclosure"] = "RESTRICTED"
        payload["evidence_refs"] = ["internal:trace/5", "public:proof/7", "secret:key/1"]
        payload["authorized_actions"] = ["OPEN_EVIDENCE"]
        result = compile_mapping(payload)
        self.assertEqual(result["evidence_refs"], ["public:proof/7"])

    def test_retry_requires_both_policy_and_authorization(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["reason_code"] = "DEPENDENCY_UNAVAILABLE"
        payload["retryable"] = True
        payload["authorized_actions"] = ["WAIT_FOR_SYSTEM"]
        no_retry = compile_mapping(payload)
        self.assertFalse(no_retry["retryable"])

        payload["authorized_actions"] = ["RETRY_AFTER_DEPENDENCY", "WAIT_FOR_SYSTEM"]
        retry = compile_mapping(payload)
        self.assertTrue(retry["retryable"])

    def test_authorized_action_not_allowed_by_reason_is_removed(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["reason_code"] = "PERMISSION_DENIED"
        payload["authorized_actions"] = ["PROVIDE_MISSING_INPUT", "REQUEST_AUTHORITY_REVIEW"]
        result = compile_mapping(payload)
        self.assertEqual([a["code"] for a in result["actions"]], ["REQUEST_AUTHORITY_REVIEW"])

    def test_thai_locale(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["locale"] = "th"
        result = compile_mapping(payload)
        self.assertIn("ข้อมูล", result["title"])
        self.assertIn("เดา", result["summary"])

    def test_control_characters_are_rejected(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["blocking_layer"] = "CORE\nINJECT"
        with self.assertRaises(FreezeBridgeError):
            compile_mapping(payload)

    def test_invalid_action_is_rejected(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["authorized_actions"] = ["FORCE_BYPASS"]
        with self.assertRaises(FreezeBridgeError):
            compile_mapping(payload)

    def test_unsupported_protocol_is_rejected(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["protocol_version"] = "2.0"
        with self.assertRaises(FreezeBridgeError):
            compile_mapping(payload)

    def test_fingerprint_changes_when_authority_changes(self) -> None:
        a = compile_mapping(BASE)
        payload = copy.deepcopy(BASE)
        payload["authorized_actions"] = ["ACKNOWLEDGE"]
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
        self.assertEqual(result["needed"], [])
        self.assertEqual(result["evidence_refs"], [])

        payload = copy.deepcopy(BASE)
        payload["missing_inputs"] = ["alpha", "alpha", "beta"]
        result = compile_mapping(payload)
        self.assertEqual(result["needed"], ["alpha", "beta"])

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
        payload = copy.deepcopy(BASE)
        payload["reason_code"] = 123
        result = compile_mapping(payload)
        self.assertEqual(result["reason_code"], "UNKNOWN_REASON")

        for key, value in [
            ("status", 123),
            ("status", "NOPE"),
            ("recovery_owner", "NOPE"),
            ("disclosure", "NOPE"),
            ("locale", "xx"),
            ("retryable", "true"),
        ]:
            with self.subTest(key=key):
                payload = copy.deepcopy(BASE)
                payload[key] = value
                with self.assertRaises(FreezeBridgeError):
                    compile_mapping(payload)

    def test_authorized_action_collection_validation_paths(self) -> None:
        payload = copy.deepcopy(BASE)
        payload["authorized_actions"] = ["ACKNOWLEDGE", "ACKNOWLEDGE"]
        result = compile_mapping(payload)
        self.assertEqual([a["code"] for a in result["actions"]], ["ACKNOWLEDGE"])

        for value in ["ACKNOWLEDGE", ["ACKNOWLEDGE"] * 10]:
            with self.subTest(value_type=type(value).__name__):
                payload = copy.deepcopy(BASE)
                payload["authorized_actions"] = value
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
