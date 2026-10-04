from __future__ import annotations

import unittest

from nexy_dcr.errors import IntegrityError, SchemaError
from nexy_dcr.model import Capsule
from nexy_dcr.replay import verify_integrity

from helpers import build_pass_capsule


class IntegrityTests(unittest.TestCase):
    def test_round_trip_preserves_identity(self) -> None:
        capsule = build_pass_capsule()
        loaded = Capsule.from_dict(capsule.to_dict())
        self.assertEqual(loaded.capsule_id, capsule.capsule_id)
        verify_integrity(loaded)

    def test_payload_tamper_is_detected(self) -> None:
        raw = build_pass_capsule().to_dict()
        raw["events"][0]["payload"]["objective"] = "tampered"
        raw.pop("capsule_id", None)
        capsule = Capsule.from_dict(raw)
        with self.assertRaisesRegex(IntegrityError, "event hash mismatch"):
            verify_integrity(capsule)

    def test_prev_hash_tamper_is_detected(self) -> None:
        raw = build_pass_capsule().to_dict()
        raw["events"][1]["prev_hash"] = "0" * 64
        raw.pop("capsule_id", None)
        capsule = Capsule.from_dict(raw)
        with self.assertRaisesRegex(IntegrityError, "hash-chain mismatch"):
            verify_integrity(capsule)

    def test_authority_ref_tamper_is_detected(self) -> None:
        raw = build_pass_capsule().to_dict()
        raw["authority_refs"][0]["role"] = "PROMOTED_WITHOUT_AUTHORITY"
        raw.pop("capsule_id", None)
        capsule = Capsule.from_dict(raw)
        with self.assertRaisesRegex(IntegrityError, "authority fingerprint mismatch"):
            verify_integrity(capsule)

    def test_capsule_id_tamper_is_rejected_on_load(self) -> None:
        raw = build_pass_capsule().to_dict()
        raw["capsule_id"] = "f" * 64
        with self.assertRaisesRegex(SchemaError, "capsule_id"):
            Capsule.from_dict(raw)

    def test_proposal_status_cannot_be_promoted(self) -> None:
        raw = build_pass_capsule().to_dict()
        raw["proposal_status"] = "CANONICAL_NEXY_REQUIREMENT"
        raw.pop("capsule_id", None)
        with self.assertRaisesRegex(SchemaError, "proposal_status"):
            Capsule.from_dict(raw)


if __name__ == "__main__":
    unittest.main()
