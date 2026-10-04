from __future__ import annotations

import json
import unittest

from nxts import ValidationError, compile_payload, validate_output_digest


def claim(i: int, **overrides):
    base = {
        "id": f"c{i:03d}",
        "text": f"claim {i}",
        "status": "SOURCE_FACT",
        "materiality": "MATERIAL",
        "visibility": "PUBLIC",
        "evidence_refs": [f"spec:{i}"],
    }
    base.update(overrides)
    return base


class AdversarialTests(unittest.TestCase):
    def test_sensitive_evidence_refs_are_not_public(self):
        payload = {
            "request_id": "r",
            "objective": "o",
            "claims": [
                claim(1),
                claim(2, visibility="SENSITIVE", evidence_refs=["secret:provider-key-location"]),
                claim(3, visibility="INTERNAL", evidence_refs=["trace:worker-7"]),
            ],
        }
        rendered = json.dumps(compile_payload(payload), ensure_ascii=False)
        self.assertNotIn("secret:provider-key-location", rendered)
        self.assertNotIn("trace:worker-7", rendered)

    def test_sensitive_material_unknown_still_blocks_without_exposing_identity(self):
        payload = {"request_id": "r", "objective": "o", "claims": [claim(1, id="secret-project-codename", visibility="SENSITIVE", status="UNKNOWN", evidence_refs=[])]}
        result = compile_payload(payload)
        self.assertEqual(result["decision"], "FREEZE")
        self.assertEqual(result["facts"], [])
        rendered = json.dumps(result, ensure_ascii=False)
        self.assertNotIn("secret-project-codename", rendered)
        self.assertEqual(result["freeze_reasons"][0]["claim_id"], "[WITHHELD]")

    def test_public_evidence_refs_are_redacted(self):
        payload = {"request_id": "r", "objective": "o", "claims": [claim(1, evidence_refs=["log: sk-abcdefghijklmnopqrstuvwxyz012345"])]}
        rendered = json.dumps(compile_payload(payload), ensure_ascii=False)
        self.assertNotIn("sk-abcdefghijklmnopqrstuvwxyz012345", rendered)
        self.assertIn("REDACTED_API_KEY", rendered)

    def test_objective_and_request_id_are_redacted(self):
        token = "sk-abcdefghijklmnopqrstuvwxyz012345"
        payload = {"request_id": f"r-{token}", "objective": f"do not expose {token}", "claims": [claim(1)]}
        rendered = json.dumps(compile_payload(payload), ensure_ascii=False)
        self.assertNotIn(token, rendered)

    def test_large_claim_count_is_rejected(self):
        payload = {"request_id": "r", "objective": "o", "claims": [claim(i) for i in range(257)]}
        with self.assertRaises(ValidationError):
            compile_payload(payload)

    def test_long_claim_text_is_rejected(self):
        payload = {"request_id": "r", "objective": "o", "claims": [claim(1, text="x" * 8193)]}
        with self.assertRaises(ValidationError):
            compile_payload(payload)

    def test_all_blocking_truth_statuses_freeze_when_material(self):
        for status in ("UNKNOWN", "CONFLICT", "NOT_VERIFIED"):
            with self.subTest(status=status):
                payload = {"request_id": "r", "objective": "o", "claims": [claim(1, status=status, evidence_refs=[])]}
                self.assertEqual(compile_payload(payload)["decision"], "FREEZE")

    def test_non_material_unknown_does_not_block_but_remains_uncertain(self):
        payload = {"request_id": "r", "objective": "o", "claims": [claim(1, status="UNKNOWN", materiality="NON_MATERIAL", evidence_refs=[])]}
        result = compile_payload(payload)
        self.assertEqual(result["decision"], "RELEASE")
        self.assertEqual(result["uncertainties"][0]["status"], "UNKNOWN")

    def test_digest_survives_unicode(self):
        payload = {"request_id": "คำขอ-1", "objective": "แสดงผลที่ตรวจสอบแล้ว 🔒", "claims": [claim(1, text="ผลลัพธ์ผ่าน ✅")]}
        result = compile_payload(payload)
        self.assertTrue(validate_output_digest(result))

    def test_duplicate_evidence_refs_are_deduplicated(self):
        payload = {"request_id": "r", "objective": "o", "claims": [claim(1, evidence_refs=["spec:1", "spec:1", "run:1"])]}
        result = compile_payload(payload)
        self.assertEqual(result["evidence_refs"], ["run:1", "spec:1"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
