from __future__ import annotations

import copy
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from nexy_gate.canonical import sha256_hex
from nexy_gate.gate import evaluate_bundle

ROOT = Path(__file__).resolve().parents[1]
PASS_BUNDLE = json.loads((ROOT / "examples" / "pass_bundle.json").read_text(encoding="utf-8"))


class GateTests(unittest.TestCase):
    def test_valid_bundle_allows(self) -> None:
        decision = evaluate_bundle(copy.deepcopy(PASS_BUNDLE))
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.status, "PASS")
        self.assertEqual(set(decision.verified_requirements), {"REQ-001", "REQ-002"})

    def test_missing_evidence_freezes(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["evidence"] = [e for e in bundle["evidence"] if e["id"] != "EV-UNIT-001"]
        decision = evaluate_bundle(bundle)
        self.assertFalse(decision.allowed)
        self.assertIn("UNKNOWN_EVIDENCE_REF", {f.code for f in decision.findings})

    def test_wrong_evidence_class_freezes(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["evidence"][0]["evidence_class"] = "E1_STATIC"
        decision = evaluate_bundle(bundle)
        self.assertFalse(decision.allowed)
        self.assertIn("EVIDENCE_CLASS_NOT_ACCEPTED", {f.code for f in decision.findings})

    def test_duplicate_evidence_id_freezes(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["evidence"].append(copy.deepcopy(bundle["evidence"][0]))
        decision = evaluate_bundle(bundle)
        self.assertIn("DUPLICATE_EVIDENCE_ID", {f.code for f in decision.findings})
        self.assertFalse(decision.allowed)

    def test_mandatory_requirement_non_pass_freezes(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["requirement_ledger"]["requirements"][0]["status"] = "NOT_VERIFIED"
        decision = evaluate_bundle(bundle)
        self.assertIn("MANDATORY_REQUIREMENT_NOT_PASS", {f.code for f in decision.findings})
        self.assertFalse(decision.allowed)

    def test_execution_non_pass_freezes(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["execution_record"]["final_status"] = "PARTIAL"
        decision = evaluate_bundle(bundle)
        self.assertIn("EXECUTION_NOT_PASS", {f.code for f in decision.findings})
        self.assertFalse(decision.allowed)

    def test_forbidden_repository_mutation_freezes(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["execution_record"]["mutations"].append({
            "target": "goif74945-crypto/NEXY.AI-core/src/index.ts",
            "change": "edit",
        })
        decision = evaluate_bundle(bundle)
        self.assertIn("FORBIDDEN_REPOSITORY_MUTATION", {f.code for f in decision.findings})
        self.assertFalse(decision.allowed)

    def test_protected_target_pattern_freezes(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["policy"]["protected_target_patterns"] = ["goif74945-crypto/AI-CONTEXT/private/**"]
        bundle["execution_record"]["mutations"].append({
            "target": "goif74945-crypto/AI-CONTEXT/private/secret.md",
            "change": "edit",
        })
        decision = evaluate_bundle(bundle)
        self.assertIn("PROTECTED_TARGET_MUTATION", {f.code for f in decision.findings})
        self.assertFalse(decision.allowed)

    def test_expected_commit_rejects_stale_evidence(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["policy"]["expected_commit"] = "abc123"
        for evidence in bundle["evidence"]:
            evidence["commit"] = "old999"
        decision = evaluate_bundle(bundle)
        self.assertIn("STALE_OR_WRONG_COMMIT_EVIDENCE", {f.code for f in decision.findings})
        self.assertFalse(decision.allowed)

    def test_expected_commit_accepts_matching_evidence(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["policy"]["expected_commit"] = "abc123"
        for evidence in bundle["evidence"]:
            evidence["commit"] = "abc123"
        decision = evaluate_bundle(bundle)
        self.assertTrue(decision.allowed)

    def test_hash_is_stable_across_mapping_order(self) -> None:
        a = {"z": 1, "a": {"b": 2, "a": 1}}
        b = {"a": {"a": 1, "b": 2}, "z": 1}
        self.assertEqual(sha256_hex(a), sha256_hex(b))

    def test_hash_changes_when_evidence_changes(self) -> None:
        a = copy.deepcopy(PASS_BUNDLE)
        b = copy.deepcopy(PASS_BUNDLE)
        b["evidence"][0]["observed"] = "different observation"
        self.assertNotEqual(sha256_hex(a), sha256_hex(b))

    def test_duplicate_requirement_id_freezes(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        duplicate = copy.deepcopy(bundle["requirement_ledger"]["requirements"][0])
        bundle["requirement_ledger"]["requirements"].append(duplicate)
        decision = evaluate_bundle(bundle)
        self.assertIn("DUPLICATE_REQUIREMENT_ID", {f.code for f in decision.findings})
        self.assertFalse(decision.allowed)

    def test_no_requirements_freezes(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["requirement_ledger"]["requirements"] = []
        decision = evaluate_bundle(bundle)
        self.assertIn("NO_REQUIREMENTS", {f.code for f in decision.findings})
        self.assertFalse(decision.allowed)

    def test_optional_failure_warns_but_allows(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["requirement_ledger"]["requirements"].append({
            "id": "REQ-OPT",
            "requirement": "Optional future feature",
            "mandatory": False,
            "status": "NOT_VERIFIED",
            "evidence_refs": [],
        })
        decision = evaluate_bundle(bundle)
        self.assertTrue(decision.allowed)
        self.assertIn("OPTIONAL_REQUIREMENT_NOT_PASS", {f.code for f in decision.findings})

    def test_policy_can_disallow_warnings(self) -> None:
        bundle = copy.deepcopy(PASS_BUNDLE)
        bundle["requirement_ledger"]["requirements"].append({
            "id": "REQ-OPT",
            "requirement": "Optional future feature",
            "mandatory": False,
            "status": "UNKNOWN",
            "evidence_refs": [],
        })
        bundle["policy"]["allow_warnings"] = False
        decision = evaluate_bundle(bundle)
        self.assertFalse(decision.allowed)
        self.assertIn("WARNINGS_DISALLOWED", {f.code for f in decision.findings})

    def test_random_json_inputs_never_raise(self) -> None:
        rng = random.Random(20261005)

        def value(depth: int = 0):
            if depth >= 3:
                return rng.choice([None, True, False, rng.randint(-5, 5), rng.random(), "x"])
            kind = rng.randrange(6)
            if kind == 0:
                return None
            if kind == 1:
                return rng.choice([True, False])
            if kind == 2:
                return rng.randint(-100, 100)
            if kind == 3:
                return "s" + str(rng.randint(0, 20))
            if kind == 4:
                return [value(depth + 1) for _ in range(rng.randrange(4))]
            return {"k" + str(i): value(depth + 1) for i in range(rng.randrange(4))}

        for _ in range(500):
            decision = evaluate_bundle(value())
            self.assertIn(decision.decision, {"ALLOW", "FREEZE"})

    def test_non_json_api_input_freezes_instead_of_raising(self) -> None:
        bundle = {"bad": {1, 2, 3}}
        decision = evaluate_bundle(bundle)
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.bundle_sha256, "UNAVAILABLE")
        self.assertIn("BUNDLE_CANONICALIZATION_FAILED", {f.code for f in decision.findings})

    def test_cli_validate_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bundle.json"
            path.write_text(json.dumps(PASS_BUNDLE, ensure_ascii=False), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "nexy_gate", "validate", str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["decision"], "ALLOW")

            frozen = copy.deepcopy(PASS_BUNDLE)
            frozen["execution_record"]["final_status"] = "FAIL"
            path.write_text(json.dumps(frozen, ensure_ascii=False), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "nexy_gate", "validate", str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 2, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["decision"], "FREEZE")


if __name__ == "__main__":
    unittest.main()
