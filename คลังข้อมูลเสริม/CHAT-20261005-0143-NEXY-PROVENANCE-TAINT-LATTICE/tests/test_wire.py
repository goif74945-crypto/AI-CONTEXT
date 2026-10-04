from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexy_provenance_taint import (  # noqa: E402
    ProvenanceEngine,
    ReleasePolicy,
    SourceSpec,
    Taint,
    artifact_from_record,
    artifact_to_record,
    decision_to_record,
    receipt_from_record,
    receipt_to_record,
)
from nexy_provenance_taint.core import ProvenanceError  # noqa: E402


class WireContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = ProvenanceEngine()
        self.artifact = self.engine.source(
            "payload",
            SourceSpec(
                origin_id="canonical:1",
                source_kind="canonical",
                authority_rank=80,
                assurance_tags=frozenset({"verified", "schema:valid"}),
                epoch=4,
            ),
            metadata={"kind": "demo"},
        )

    def test_artifact_round_trip_is_lossless(self):
        record = artifact_to_record(self.artifact)
        restored = artifact_from_record(record)
        self.assertEqual(self.artifact, restored)

    def test_artifact_parser_rejects_unknown_schema(self):
        record = artifact_to_record(self.artifact)
        record["schema"] = "unknown/v999"
        with self.assertRaises(ProvenanceError):
            artifact_from_record(record)

    def test_artifact_parser_rejects_extra_fields_fail_closed(self):
        record = artifact_to_record(self.artifact)
        record["surprise"] = True
        with self.assertRaises(ProvenanceError):
            artifact_from_record(record)

    def test_artifact_parser_rejects_missing_fields_fail_closed(self):
        record = artifact_to_record(self.artifact)
        del record["authority_floor"]
        with self.assertRaises(ProvenanceError):
            artifact_from_record(record)

    def test_artifact_parser_rejects_tampered_authority(self):
        record = artifact_to_record(self.artifact)
        record["authority_floor"] = 999
        with self.assertRaises(ProvenanceError):
            artifact_from_record(record)

    def test_artifact_parser_rejects_unknown_taint(self):
        record = artifact_to_record(self.artifact)
        record["taints"] = ["MADE_UP"]
        with self.assertRaises(ProvenanceError):
            artifact_from_record(record)

    def test_artifact_parser_rejects_bool_as_integer(self):
        record = artifact_to_record(self.artifact)
        record["created_epoch"] = True
        with self.assertRaises(ProvenanceError):
            artifact_from_record(record)

    def test_receipt_round_trip_is_lossless(self):
        receipt = self.engine.issue_verification(
            self.artifact,
            verifier_id="judge:1",
            added_assurances={"integration:passed"},
            issued_epoch=4,
            expires_epoch=8,
        )
        record = receipt_to_record(receipt)
        restored = receipt_from_record(record)
        self.assertEqual(receipt, restored)

    def test_receipt_parser_rejects_content_tamper(self):
        receipt = self.engine.issue_verification(
            self.artifact,
            verifier_id="judge:1",
            added_assurances={"integration:passed"},
            issued_epoch=4,
        )
        record = receipt_to_record(receipt)
        record["verifier_id"] = "attacker"
        with self.assertRaises(ProvenanceError):
            receipt_from_record(record)

    def test_receipt_parser_rejects_extra_field(self):
        receipt = self.engine.issue_verification(
            self.artifact, verifier_id="judge:1", issued_epoch=4
        )
        record = receipt_to_record(receipt)
        record["extra"] = "x"
        with self.assertRaises(ProvenanceError):
            receipt_from_record(record)

    def test_allow_decision_serializes(self):
        policy = ReleasePolicy(
            policy_id="p",
            min_authority_rank=50,
            required_assurances=frozenset({"verified"}),
            forbidden_taints=frozenset(Taint),
        )
        decision = self.engine.release_decision(self.artifact, policy, current_epoch=4)
        record = decision_to_record(decision)
        self.assertTrue(record["allowed"])
        self.assertEqual("ALLOW", record["state"])

    def test_freeze_decision_serializes_with_reasons(self):
        policy = ReleasePolicy(
            policy_id="p",
            min_authority_rank=100,
            required_assurances=frozenset({"deployment:passed"}),
            forbidden_taints=frozenset(Taint),
        )
        decision = self.engine.release_decision(self.artifact, policy, current_epoch=4)
        record = decision_to_record(decision)
        self.assertFalse(record["allowed"])
        self.assertTrue(record["reason_codes"])


if __name__ == "__main__":
    unittest.main()
