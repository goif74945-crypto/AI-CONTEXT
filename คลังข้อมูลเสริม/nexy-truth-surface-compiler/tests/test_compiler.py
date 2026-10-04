from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from nxts import ValidationError, compile_payload, validate_output_digest


def base_payload() -> dict:
    return {
        "request_id": "req-001",
        "objective": "Return the verified deployment state",
        "claims": [
            {
                "id": "c1",
                "text": "The exact-head verification suite passed.",
                "status": "RUNTIME_FACT",
                "materiality": "MATERIAL",
                "visibility": "PUBLIC",
                "evidence_refs": ["run:123"],
            }
        ],
    }


class CompilerTests(unittest.TestCase):
    def test_releases_material_fact_with_evidence(self) -> None:
        result = compile_payload(base_payload())
        self.assertEqual(result["decision"], "RELEASE")
        self.assertEqual(result["facts"][0]["claim_id"], "c1")
        self.assertTrue(validate_output_digest(result))

    def test_freezes_material_unknown(self) -> None:
        payload = base_payload()
        payload["claims"][0]["status"] = "UNKNOWN"
        result = compile_payload(payload)
        self.assertEqual(result["decision"], "FREEZE")
        self.assertEqual(result["freeze_reasons"][0]["code"], "MATERIAL_UNKNOWN")

    def test_freezes_material_conflict(self) -> None:
        payload = base_payload()
        payload["claims"][0]["status"] = "CONFLICT"
        result = compile_payload(payload)
        self.assertEqual(result["decision"], "FREEZE")
        self.assertIn("MATERIAL_CONFLICT", {x["code"] for x in result["freeze_reasons"]})

    def test_freezes_not_verified(self) -> None:
        payload = base_payload()
        payload["claims"][0]["status"] = "NOT_VERIFIED"
        result = compile_payload(payload)
        self.assertEqual(result["decision"], "FREEZE")

    def test_non_material_assumption_is_visible_but_not_blocking(self) -> None:
        payload = base_payload()
        payload["claims"].append({
            "id": "c2",
            "text": "Latency may improve after caching.",
            "status": "ASSUMPTION",
            "materiality": "NON_MATERIAL",
            "visibility": "PUBLIC",
            "evidence_refs": [],
        })
        result = compile_payload(payload)
        self.assertEqual(result["decision"], "RELEASE")
        self.assertEqual(result["uncertainties"][0]["status"], "ASSUMPTION")

    def test_material_fact_without_evidence_freezes(self) -> None:
        payload = base_payload()
        payload["claims"][0]["evidence_refs"] = []
        result = compile_payload(payload)
        self.assertEqual(result["decision"], "FREEZE")
        self.assertEqual(result["freeze_reasons"][0]["code"], "MATERIAL_FACT_WITHOUT_EVIDENCE")

    def test_claim_order_is_semantically_invariant(self) -> None:
        p1 = base_payload()
        p1["claims"].append({
            "id": "a0",
            "text": "A secondary fact.",
            "status": "SOURCE_FACT",
            "materiality": "NON_MATERIAL",
            "visibility": "PUBLIC",
            "evidence_refs": ["spec:x"],
        })
        p2 = json.loads(json.dumps(p1))
        p2["claims"].reverse()
        r1 = compile_payload(p1)
        r2 = compile_payload(p2)
        self.assertEqual(r1, r2)

    def test_internal_and_sensitive_claims_are_not_exposed(self) -> None:
        payload = base_payload()
        payload["claims"].extend([
            {
                "id": "c2",
                "text": "Internal worker routing detail",
                "status": "SOURCE_FACT",
                "materiality": "NON_MATERIAL",
                "visibility": "INTERNAL",
                "evidence_refs": ["internal:1"],
            },
            {
                "id": "c3",
                "text": "Secret provider credential detail",
                "status": "SOURCE_FACT",
                "materiality": "NON_MATERIAL",
                "visibility": "SENSITIVE",
                "evidence_refs": ["secret:1"],
            },
        ])
        result = compile_payload(payload)
        rendered = json.dumps(result, ensure_ascii=False)
        self.assertNotIn("worker routing", rendered)
        self.assertNotIn("provider credential", rendered)

    def test_token_patterns_are_redacted_from_public_text(self) -> None:
        payload = base_payload()
        payload["claims"][0]["text"] = "Observed token sk-abcdefghijklmnopqrstuvwxyz012345 in debug text."
        result = compile_payload(payload)
        rendered = json.dumps(result, ensure_ascii=False)
        self.assertNotIn("sk-abcdefghijklmnopqrstuvwxyz012345", rendered)
        self.assertIn("REDACTED_API_KEY", rendered)

    def test_unknown_status_fails_closed(self) -> None:
        payload = base_payload()
        payload["claims"][0]["status"] = "MAGIC_TRUE"
        result = compile_payload(payload)
        self.assertEqual(result["decision"], "FREEZE")
        self.assertEqual(result["freeze_reasons"][0]["code"], "UNKNOWN_STATUS")

    def test_duplicate_claim_ids_are_rejected(self) -> None:
        payload = base_payload()
        payload["claims"].append(dict(payload["claims"][0]))
        with self.assertRaises(ValidationError):
            compile_payload(payload)

    def test_output_digest_detects_tampering(self) -> None:
        result = compile_payload(base_payload())
        self.assertTrue(validate_output_digest(result))
        result["summary"] = "tampered"
        self.assertFalse(validate_output_digest(result))

    def test_repeat_runs_are_byte_stable_when_serialized_canonically(self) -> None:
        r1 = compile_payload(base_payload())
        r2 = compile_payload(base_payload())
        b1 = json.dumps(r1, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        b2 = json.dumps(r2, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(b1, b2)

    def test_cli_exit_codes_release_and_freeze(self) -> None:
        root = Path(__file__).resolve().parents[1]
        env = dict(os.environ)
        env["PYTHONPATH"] = str(root / "src")

        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "input.json"
            p.write_text(json.dumps(base_payload()), encoding="utf-8")
            released = subprocess.run([sys.executable, "-m", "nxts.cli", str(p)], env=env, capture_output=True, text=True, check=False)
            self.assertEqual(released.returncode, 0, released.stderr)

            frozen_payload = base_payload()
            frozen_payload["claims"][0]["status"] = "UNKNOWN"
            p.write_text(json.dumps(frozen_payload), encoding="utf-8")
            frozen = subprocess.run([sys.executable, "-m", "nxts.cli", str(p)], env=env, capture_output=True, text=True, check=False)
            self.assertEqual(frozen.returncode, 2, frozen.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
