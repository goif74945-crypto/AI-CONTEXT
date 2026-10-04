import unittest

from nexy_preflight import (
    Decision, EvidenceClass, TaskContract,
    canonical_json, compare_contracts, contains_scope, evaluate_contract,
    minimum_for_claim, sha256_identity,
)


# ===== test_canonical.py =====
import unittest



BASE = {
    "task_id": "T1",
    "objective": "demo",
    "target": "repo",
    "authorized_scope": ["repo/a"],
    "protected_scope": ["repo/protected"],
    "authority_sources": ["user"],
    "preconditions": [],
    "operations": [],
    "claims": [],
    "evidence": [],
    "approvals": [],
}


class CanonicalTests(unittest.TestCase):
    def test_key_order_does_not_change_hash(self):
        a = dict(BASE)
        b = {k: BASE[k] for k in reversed(list(BASE.keys()))}
        ca = TaskContract.from_mapping(a)
        cb = TaskContract.from_mapping(b)
        self.assertEqual(sha256_identity(ca.to_primitive()), sha256_identity(cb.to_primitive()))

    def test_canonical_json_is_compact_and_sorted(self):
        self.assertEqual(canonical_json({"b": 2, "a": 1}), '{"a":1,"b":2}')

    def test_semantic_change_changes_hash(self):
        a = TaskContract.from_mapping(BASE)
        changed = dict(BASE)
        changed["objective"] = "different"
        b = TaskContract.from_mapping(changed)
        self.assertNotEqual(sha256_identity(a.to_primitive()), sha256_identity(b.to_primitive()))



# ===== test_engine.py =====
import unittest



def contract(**changes):
    raw = {
        "task_id": "TASK-001",
        "objective": "Add advisory material",
        "target": "goif74945-crypto/AI-CONTEXT",
        "authorized_scope": ["goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/lab"],
        "protected_scope": ["goif74945-crypto/NEXY.AI-"],
        "authority_sources": ["user-directive", "AI-CONTEXT/rules/GLOBAL.md"],
        "preconditions": ["target-exists"],
        "operations": [
            {
                "kind": "write",
                "resource": "goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/lab/README.md",
                "irreversible": False,
            }
        ],
        "claims": [],
        "evidence": [],
        "approvals": [],
    }
    raw.update(changes)
    return TaskContract.from_mapping(raw)


class PathTests(unittest.TestCase):
    def test_scope_boundary(self):
        self.assertTrue(contains_scope("a/b", "a/b/c"))
        self.assertFalse(contains_scope("a/b", "a/bad/c"))

    def test_windows_slashes_normalize(self):
        self.assertTrue(contains_scope("a\\b", "a/b/c"))


class EngineTests(unittest.TestCase):
    def test_safe_contract_passes(self):
        result = evaluate_contract(contract())
        self.assertEqual(result.decision, Decision.PASS)
        self.assertEqual(result.findings, ())

    def test_missing_target_blocks(self):
        result = evaluate_contract(contract(target=""))
        self.assertEqual(result.decision, Decision.BLOCKED)
        self.assertIn("PFL-TARGET-MISSING", {f.code for f in result.findings})

    def test_missing_scope_blocks(self):
        result = evaluate_contract(contract(authorized_scope=[]))
        self.assertEqual(result.decision, Decision.BLOCKED)
        self.assertIn("PFL-SCOPE-MISSING", {f.code for f in result.findings})

    def test_missing_authority_blocks(self):
        result = evaluate_contract(contract(authority_sources=[]))
        self.assertEqual(result.decision, Decision.BLOCKED)
        self.assertIn("PFL-AUTHORITY-MISSING", {f.code for f in result.findings})

    def test_outside_scope_blocks(self):
        ops = [{"kind": "write", "resource": "somewhere/else", "irreversible": False}]
        result = evaluate_contract(contract(operations=ops))
        self.assertEqual(result.decision, Decision.BLOCKED)
        self.assertIn("PFL-SCOPE-OUTSIDE", {f.code for f in result.findings})

    def test_protected_write_conflicts(self):
        protected = "goif74945-crypto/NEXY.AI-"
        ops = [{"kind": "write", "resource": protected + "/src/x.ts", "irreversible": False}]
        result = evaluate_contract(
            contract(authorized_scope=[protected], operations=ops)
        )
        self.assertEqual(result.decision, Decision.CONFLICT)
        codes = {f.code for f in result.findings}
        self.assertIn("PFL-PROTECTED-WRITE", codes)

    def test_read_in_protected_scope_is_not_write_violation(self):
        protected = "goif74945-crypto/NEXY.AI-"
        ops = [{"kind": "read", "resource": protected + "/README.md", "irreversible": False}]
        result = evaluate_contract(
            contract(authorized_scope=[protected], protected_scope=[protected], operations=ops)
        )
        self.assertEqual(result.decision, Decision.PASS)
        self.assertNotIn("PFL-PROTECTED-WRITE", {f.code for f in result.findings})

    def test_irreversible_requires_explicit_approval(self):
        resource = "goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/lab/old.md"
        ops = [{"kind": "delete", "resource": resource, "irreversible": True}]
        result = evaluate_contract(contract(operations=ops))
        self.assertEqual(result.decision, Decision.BLOCKED)
        self.assertIn("PFL-APPROVAL-MISSING", {f.code for f in result.findings})

    def test_irreversible_with_explicit_approval_can_pass(self):
        resource = "goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/lab/old.md"
        token = f"approve:delete:{resource}"
        ops = [{"kind": "delete", "resource": resource, "irreversible": True}]
        result = evaluate_contract(contract(operations=ops, approvals=[token]))
        self.assertEqual(result.decision, Decision.PASS)

    def test_unknown_claim_kind_blocks(self):
        claims = [{"id": "C1", "kind": "magic", "text": "unknown policy"}]
        result = evaluate_contract(contract(claims=claims))
        self.assertEqual(result.decision, Decision.BLOCKED)
        self.assertIn("PFL-EVIDENCE-POLICY-UNKNOWN", {f.code for f in result.findings})

    def test_missing_evidence_is_not_verified(self):
        claims = [{"id": "C1", "kind": "uni