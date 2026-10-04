import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from nexy_supply_chain_sentinel.canonical import canonical_json, sha256_json
from nexy_supply_chain_sentinel.cli import main
from nexy_supply_chain_sentinel.diffing import diff_snapshots
from nexy_supply_chain_sentinel.engine import build_snapshot, validate_snapshot, verify_drift
from nexy_supply_chain_sentinel.policy import Policy, PolicyError


HASH_A = "a" * 64
HASH_B = "b" * 64


class SentinelTestCase(unittest.TestCase):
    def write_json(self, root: Path, name: str, value: dict) -> Path:
        path = root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def npm_lock(self, version="1.0.0", integrity="sha512-AAA", host="registry.npmjs.org", include_b=False):
        packages = {
            "": {"name": "demo", "version": "1.0.0"},
            "node_modules/a": {
                "version": version,
                "resolved": f"https://{host}/a/-/a-{version}.tgz",
                "integrity": integrity,
            },
        }
        if include_b:
            packages["node_modules/b"] = {
                "version": "2.0.0",
                "resolved": "https://registry.npmjs.org/b/-/b-2.0.0.tgz",
                "integrity": "sha512-BBB",
            }
        return {"name": "demo", "lockfileVersion": 3, "packages": packages}

    def test_canonical_json_and_hash_ignore_mapping_order(self):
        left = {"z": 1, "a": {"y": 2, "x": 3}}
        right = {"a": {"x": 3, "y": 2}, "z": 1}
        self.assertEqual(canonical_json(left), canonical_json(right))
        self.assertEqual(sha256_json(left), sha256_json(right))

    def test_npm_snapshot_is_allow_and_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write_json(root, "package-lock.json", self.npm_lock())
            first = build_snapshot(path)
            second = build_snapshot(path)
            self.assertEqual(first["decision"], "ALLOW")
            self.assertEqual(first["inventory_sha256"], second["inventory_sha256"])
            self.assertEqual(first["snapshot_sha256"], second["snapshot_sha256"])
            self.assertEqual(first["packages"][0]["name"], "a")

    def test_npm_untrusted_registry_host_freezes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write_json(root, "package-lock.json", self.npm_lock(host="evil.example"))
            snapshot = build_snapshot(path)
            self.assertEqual(snapshot["decision"], "FREEZE")
            self.assertIn("NPM_SOURCE_HOST_NOT_ALLOWED", {v["code"] for v in snapshot["violations"]})

    def test_missing_integrity_freezes_by_default(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            lock = self.npm_lock()
            del lock["packages"]["node_modules/a"]["integrity"]
            path = self.write_json(root, "package-lock.json", lock)
            snapshot = build_snapshot(path)
            self.assertEqual(snapshot["decision"], "FREEZE")
            self.assertIn("MISSING_INTEGRITY", {v["code"] for v in snapshot["violations"]})

    def test_hashed_python_requirement_allows(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "requirements.txt"
            path.write_text(f"Requests==2.32.3 --hash=sha256:{HASH_A}\n", encoding="utf-8")
            snapshot = build_snapshot(path)
            self.assertEqual(snapshot["decision"], "ALLOW")
            self.assertEqual(snapshot["packages"][0]["name"], "requests")
            self.assertEqual(snapshot["packages"][0]["integrity"], f"sha256:{HASH_A}")

    def test_unpinned_python_requirement_freezes(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "requirements.txt"
            path.write_text("requests>=2\n", encoding="utf-8")
            snapshot = build_snapshot(path)
            self.assertEqual(snapshot["decision"], "FREEZE")
            self.assertIn("PYTHON_UNPINNED_OR_UNSUPPORTED_REQUIREMENT", {v["code"] for v in snapshot["violations"]})

    def test_snapshot_tampering_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write_json(root, "package-lock.json", self.npm_lock())
            snapshot = build_snapshot(path)
            snapshot["packages"][0]["version"] = "9.9.9"
            valid, reasons = validate_snapshot(snapshot)
            self.assertFalse(valid)
            self.assertIn("INVENTORY_HASH_MISMATCH", reasons)
            self.assertIn("SNAPSHOT_HASH_MISMATCH", reasons)

    def test_version_change_is_single_semantic_drift_and_freezes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            baseline_path = self.write_json(root, "baseline-lock.json", self.npm_lock(version="1.0.0", integrity="sha512-AAA"))
            candidate_path = self.write_json(root, "candidate-lock.json", self.npm_lock(version="2.0.0", integrity="sha512-BBB"))
            baseline = build_snapshot(baseline_path)
            candidate = build_snapshot(candidate_path)
            events = diff_snapshots(baseline, candidate)
            self.assertEqual([e["type"] for e in events], ["VERSION_CHANGE"])
            result = verify_drift(baseline, candidate)
            self.assertEqual(result["decision"], "FREEZE")
            self.assertIn("DRIFT_VERSION_CHANGE_DENIED", result["reason_codes"])

    def test_integrity_change_freezes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            baseline_path = self.write_json(root, "baseline-lock.json", self.npm_lock(integrity="sha512-AAA"))
            candidate_path = self.write_json(root, "candidate-lock.json", self.npm_lock(integrity="sha512-BBB"))
            result = verify_drift(build_snapshot(baseline_path), build_snapshot(candidate_path))
            self.assertEqual(result["decision"], "FREEZE")
            self.assertEqual(result["events"][0]["type"], "INTEGRITY_CHANGE")

    def test_explicit_policy_can_allow_addition(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            baseline_path = self.write_json(root, "baseline-lock.json", self.npm_lock(include_b=False))
            candidate_path = self.write_json(root, "candidate-lock.json", self.npm_lock(include_b=True))
            policy = Policy(allow_additions=True)
            result = verify_drift(build_snapshot(baseline_path, policy=policy), build_snapshot(candidate_path, policy=policy), policy=policy)
            self.assertEqual(result["decision"], "ALLOW")
            self.assertEqual([e["type"] for e in result["events"]], ["ADDITION"])

    def test_unknown_policy_field_is_rejected(self):
        with self.assertRaises(PolicyError):
            Policy.from_dict({"allow_additions": True, "typo_allow_everything": True})

    def test_cli_snapshot_prints_machine_readable_json(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write_json(root, "package-lock.json", self.npm_lock())
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(["snapshot", "--input", os.fspath(path)])
            self.assertEqual(code, 0)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["decision"], "ALLOW")
            self.assertEqual(payload["schema_version"], "nscs.snapshot.v1")


if __name__ == "__main__":
    unittest.main()

class SentinelAdversarialTestCase(unittest.TestCase):
    def write_json(self, root: Path, name: str, value: dict) -> Path:
        path = root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def npm_lock(self):
        return {
            "name": "demo",
            "lockfileVersion": 3,
            "packages": {
                "": {"name": "demo", "version": "1.0.0"},
                "node_modules/a": {
                    "version": "1.0.0",
                    "resolved": "https://registry.npmjs.org/a/-/a-1.0.0.tgz",
                    "integrity": "sha512-AAA",
                },
            },
        }

    def reseal(self, snapshot: dict) -> None:
        sealable = {k: v for k, v in snapshot.items() if k != "snapshot_sha256"}
        snapshot["snapshot_sha256"] = sha256_json(sealable)

    def test_invalid_utf8_becomes_freeze_snapshot_instead_of_exception(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "requirements.txt"
            path.write_bytes(b"requests==2.0 --hash=sha256:" + b"a" * 64 + b"\xff")
            snapshot = build_snapshot(path)
            self.assertEqual(snapshot["decision"], "FREEZE")
            self.assertIn("INPUT_NOT_UTF8", {v["code"] for v in snapshot["violations"]})

    def test_resealed_unknown_snapshot_field_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = self.write_json(Path(td), "package-lock.json", self.npm_lock())
            snapshot = build_snapshot(path)
            snapshot["unexpected_authority"] = "ALLOW"
            self.reseal(snapshot)
            valid, reasons = validate_snapshot(snapshot)
            self.assertFalse(valid)
            self.assertIn("SNAPSHOT_UNKNOWN_FIELD:unexpected_authority", reasons)

    def test_resealed_decision_cannot_contradict_violations(self):
        with tempfile.TemporaryDirectory() as td:
            lock = self.npm_lock()
            del lock["packages"]["node_modules/a"]["integrity"]
            path = self.write_json(Path(td), "package-lock.json", lock)
            snapshot = build_snapshot(path)
            self.assertEqual(snapshot["decision"], "FREEZE")
            snapshot["decision"] = "ALLOW"
            self.reseal(snapshot)
            valid, reasons = validate_snapshot(snapshot)
            self.assertFalse(valid)
            self.assertIn("SNAPSHOT_DECISION_INCONSISTENT", reasons)

    def test_resealed_package_with_unknown_field_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = self.write_json(Path(td), "package-lock.json", self.npm_lock())
            snapshot = build_snapshot(path)
            snapshot["packages"][0]["authority"] = "trusted"
            snapshot["inventory_sha256"] = sha256_json(snapshot["packages"])
            self.reseal(snapshot)
            valid, reasons = validate_snapshot(snapshot)
            self.assertFalse(valid)
            self.assertIn("PACKAGE_SCHEMA_INVALID", reasons)

class SentinelSecurityLimitsTestCase(unittest.TestCase):
    def test_npm_source_credentials_are_not_persisted(self):
        with tempfile.TemporaryDirectory() as td:
            lock = {
                "name": "demo",
                "lockfileVersion": 3,
                "packages": {
                    "": {"name": "demo", "version": "1.0.0"},
                    "node_modules/a": {
                        "version": "1.0.0",
                        "resolved": "https://user:supersecret@registry.npmjs.org/a/-/a-1.0.0.tgz?token=hidden",
                        "integrity": "sha512-AAA",
                    },
                },
            }
            path = Path(td) / "package-lock.json"
            path.write_text(json.dumps(lock), encoding="utf-8")
            snapshot = build_snapshot(path)
            serialized = canonical_json(snapshot)
            self.assertEqual(snapshot["decision"], "FREEZE")
            self.assertNotIn("supersecret", serialized)
            self.assertNotIn("token=hidden", serialized)
            self.assertIn("NPM_SOURCE_CREDENTIALS_FORBIDDEN", {v["code"] for v in snapshot["violations"]})
            self.assertIn("NPM_SOURCE_QUERY_OR_FRAGMENT_FORBIDDEN", {v["code"] for v in snapshot["violations"]})

    def test_input_size_policy_freezes_before_dependency_parse(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "requirements.txt"
            path.write_text("x" * 32, encoding="utf-8")
            snapshot = build_snapshot(path, policy=Policy(max_input_bytes=16))
            self.assertEqual(snapshot["decision"], "FREEZE")
            self.assertEqual(snapshot["source_kind"], "unparsed")
            self.assertIn("INPUT_SIZE_LIMIT_EXCEEDED", {v["code"] for v in snapshot["violations"]})

class SentinelCrossOriginDriftTestCase(unittest.TestCase):
    def test_version_change_does_not_mask_registry_origin_change(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            baseline_lock = {
                "name": "demo",
                "lockfileVersion": 3,
                "packages": {
                    "": {"name": "demo", "version": "1.0.0"},
                    "node_modules/a": {
                        "version": "1.0.0",
                        "resolved": "https://registry.npmjs.org/a/-/a-1.0.0.tgz",
                        "integrity": "sha512-AAA",
                    },
                },
            }
            candidate_lock = {
                "name": "demo",
                "lockfileVersion": 3,
                "packages": {
                    "": {"name": "demo", "version": "1.0.0"},
                    "node_modules/a": {
                        "version": "2.0.0",
                        "resolved": "https://mirror.example/a/-/a-2.0.0.tgz",
                        "integrity": "sha512-BBB",
                    },
                },
            }
            baseline_path = root / "baseline.json"
            candidate_path = root / "candidate.json"
            baseline_path.write_text(json.dumps(baseline_lock), encoding="utf-8")
            candidate_path.write_text(json.dumps(candidate_lock), encoding="utf-8")
            policy = Policy(
                allowed_npm_hosts=("registry.npmjs.org", "mirror.example"),
                allow_version_changes=True,
                allow_source_changes=False,
            )
            baseline = build_snapshot(baseline_path, policy=policy)
            candidate = build_snapshot(candidate_path, policy=policy)
            result = verify_drift(baseline, candidate, policy=policy)
            self.assertEqual(result["decision"], "FREEZE")
            self.assertEqual([event["type"] for event in result["events"]], ["SOURCE_CHANGE", "VERSION_CHANGE"])
            self.assertIn("DRIFT_SOURCE_CHANGE_DENIED", result["reason_codes"])
            self.assertNotIn("DRIFT_VERSION_CHANGE_DENIED", result["reason_codes"])
