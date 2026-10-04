import hashlib
import unittest
from src import validate_manifest


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class ArtifactReferentialIntegrityGuardTests(unittest.TestCase):
    def test_valid_graph_with_hashes_passes(self):
        manifest = [
            {"id": "REQ-1", "kind": "requirement", "refs": ["TEST-1"]},
            {"id": "TEST-1", "kind": "test", "refs": ["EVID-1"]},
            {"id": "EVID-1", "kind": "evidence", "refs": [], "sha256": sha("pass")},
        ]
        report = validate_manifest(manifest, {"EVID-1": "pass"})
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["errors"], [])

    def test_missing_reference_and_stale_hash_fail(self):
        manifest = [
            {"id": "REQ-1", "kind": "requirement", "refs": ["TEST-MISSING", "EVID-1"]},
            {"id": "EVID-1", "kind": "evidence", "refs": [], "sha256": sha("old")},
        ]
        report = validate_manifest(manifest, {"EVID-1": "new"})
        codes = [e["code"] for e in report["errors"]]
        self.assertIn("MISSING_REF", codes)
        self.assertIn("STALE_HASH", codes)
        self.assertEqual(report["status"], "FAIL")

    def test_duplicate_ids_fail_closed(self):
        manifest = [
            {"id": "X", "kind": "requirement", "refs": []},
            {"id": "X", "kind": "test", "refs": []},
        ]
        report = validate_manifest(manifest, {})
        self.assertEqual(report["errors"][0]["code"], "DUPLICATE_ID")

    def test_orphan_evidence_is_reported(self):
        manifest = [
            {"id": "REQ", "kind": "requirement", "refs": []},
            {"id": "E", "kind": "evidence", "refs": []},
        ]
        report = validate_manifest(manifest, {})
        self.assertEqual(report["orphans"], ["E"])

    def test_empty_manifest_is_not_verified(self):
        report = validate_manifest([], {})
        self.assertEqual(report["status"], "NOT_VERIFIED")


if __name__ == "__main__":
    unittest.main()
