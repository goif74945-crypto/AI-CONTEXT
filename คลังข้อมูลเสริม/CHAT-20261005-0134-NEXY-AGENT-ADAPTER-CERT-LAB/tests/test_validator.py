from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from nexy_adapter_cert.validator import validate_manifest

ROOT = Path(__file__).resolve().parents[1]


def fixture(name: str):
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


class ValidatorTests(unittest.TestCase):
    def test_valid_noncritical_passes(self):
        report = validate_manifest(fixture("valid-noncritical.json"))
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.issues, ())

    def test_valid_critical_passes(self):
        report = validate_manifest(fixture("valid-critical.json"))
        self.assertEqual(report.status, "PASS")

    def test_critical_timeout_must_be_30_seconds(self):
        report = validate_manifest(fixture("invalid-critical-timeout.json"))
        self.assertEqual(report.status, "FAIL")
        self.assertIn("DOC-C.CRITICAL_AGENT_TIMEOUT", {issue.code for issue in report.issues})

    def test_authority_escalation_is_rejected(self):
        report = validate_manifest(fixture("invalid-authority-escalation.json"))
        codes = {issue.code for issue in report.issues}
        self.assertEqual(report.status, "FAIL")
        self.assertIn("NEXY.CORE.NO_WORKER_RELEASE", codes)
        self.assertIn("DOC-C.DEPENDENCY.SWARM_TO_VAULT_FORBIDDEN", codes)
        self.assertIn("DOC-C.PIPELINE.NO_AUTOMATIC_RETRY", codes)
        self.assertIn("NEXY.SECURITY.SERVER_SIDE_RUNTIME_SECRETS", codes)

    def test_duplicate_modes_rejected(self):
        manifest = fixture("valid-noncritical.json")
        manifest["adapter"]["supported_modes"] = ["fast", "fast"]
        report = validate_manifest(manifest)
        self.assertIn("LAB.DUPLICATE_MODE", {issue.code for issue in report.issues})

    def test_unknown_mode_rejected(self):
        manifest = fixture("valid-noncritical.json")
        manifest["adapter"]["supported_modes"] = ["fast", "turbo"]
        report = validate_manifest(manifest)
        self.assertIn("DOC-C.AGENT_SUPPORTED_MODES", {issue.code for issue in report.issues})

    def test_missing_operation_rejected(self):
        manifest = fixture("valid-noncritical.json")
        manifest["adapter"]["operations"] = ["execute", "healthcheck"]
        report = validate_manifest(manifest)
        self.assertIn("DOC-C.AGENT_ADAPTER_OPERATIONS", {issue.code for issue in report.issues})

    def test_report_digest_is_deterministic_for_key_order(self):
        manifest = fixture("valid-noncritical.json")
        reordered = {key: copy.deepcopy(manifest[key]) for key in reversed(list(manifest))}
        a = validate_manifest(manifest)
        b = validate_manifest(reordered)
        self.assertEqual(a.manifest_digest, b.manifest_digest)
        self.assertEqual(a.report_digest, b.report_digest)


    def test_timeout_boundaries(self):
        manifest = fixture("valid-noncritical.json")
        for value, expected in [(9999, "FAIL"), (10000, "PASS"), (60000, "PASS"), (60001, "FAIL")]:
            with self.subTest(timeout_ms=value):
                candidate = copy.deepcopy(manifest)
                candidate["adapter"]["timeout_ms"] = value
                self.assertEqual(validate_manifest(candidate).status, expected)

    def test_secret_persistence_rejected(self):
        manifest = fixture("valid-noncritical.json")
        manifest["security"]["persists_secrets"] = True
        report = validate_manifest(manifest)
        self.assertIn("NEXY.SECURITY.NO_SECRET_PERSISTENCE", {issue.code for issue in report.issues})

    def test_wrong_boolean_types_rejected(self):
        manifest = fixture("valid-noncritical.json")
        manifest["adapter"]["critical"] = 1
        manifest["authority"]["direct_release"] = 0
        report = validate_manifest(manifest)
        codes = {issue.code for issue in report.issues}
        self.assertIn("DOC-C.CRITICAL_FLAG_DECLARED", codes)
        self.assertIn("NEXY.CORE.NO_WORKER_RELEASE", codes)

    def test_digest_changes_when_semantics_change(self):
        manifest = fixture("valid-noncritical.json")
        changed = copy.deepcopy(manifest)
        changed["adapter"]["context_capacity"] += 1
        a = validate_manifest(manifest)
        b = validate_manifest(changed)
        self.assertNotEqual(a.manifest_digest, b.manifest_digest)
        self.assertNotEqual(a.report_digest, b.report_digest)

    def test_issue_order_is_deterministic(self):
        report = validate_manifest(fixture("invalid-authority-escalation.json"))
        actual = [(i.code, i.path, i.message) for i in report.issues]
        self.assertEqual(actual, sorted(actual))

    def test_non_object_manifest_fails_without_crash(self):
        report = validate_manifest(["not", "an", "object"])
        self.assertEqual(report.status, "FAIL")
        self.assertTrue(report.issues)


if __name__ == "__main__":
    unittest.main()
