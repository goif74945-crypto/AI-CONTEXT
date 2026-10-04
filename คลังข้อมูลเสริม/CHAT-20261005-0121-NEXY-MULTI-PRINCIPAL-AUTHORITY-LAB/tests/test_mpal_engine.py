from __future__ import annotations

import copy
import itertools
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mpal_engine import (  # noqa: E402
    approval_for,
    evaluate,
    policy_sha256,
    request_sha256,
    validate_policy,
    validate_request,
)


def load(name: str):
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


class MPALTests(unittest.TestCase):
    def setUp(self):
        self.policy = load("policy.example.json")
        self.request = load("request.example.json")

    def a(self, principal, decision="APPROVE", group="operations", vf=0, vu=100):
        return approval_for(self.policy, self.request, principal, decision, group, valid_from_tick=vf, valid_until_tick=vu)

    def allow_set(self):
        return [self.a("bob", group="security"), self.a("alice"), self.a("dave")]

    def test_example_policy_valid(self):
        self.assertTrue(validate_policy(self.policy).ok)

    def test_example_request_valid(self):
        self.assertTrue(validate_request(self.request).ok)

    def test_full_quorum_allows(self):
        d = evaluate(self.policy, self.request, self.allow_set(), evaluation_tick=50)
        self.assertEqual("ALLOW", d.state)
        self.assertEqual(("ALL_AUTHORITY_GATES_SATISFIED",), d.reason_codes)

    def test_missing_security_is_pending(self):
        d = evaluate(self.policy, self.request, [self.a("alice"), self.a("dave")], evaluation_tick=50)
        self.assertEqual("PENDING", d.state)
        self.assertTrue(any(x.startswith("GROUP_QUORUM_MISSING:security") for x in d.reason_codes))

    def test_missing_second_operations_is_pending(self):
        d = evaluate(self.policy, self.request, [self.a("bob", group="security"), self.a("alice")], evaluation_tick=50)
        self.assertEqual("PENDING", d.state)
        self.assertTrue(any(x.startswith("GROUP_QUORUM_MISSING:operations") for x in d.reason_codes))

    def test_security_veto_denies(self):
        approvals = [self.a("bob", decision="DENY", group=None), self.a("alice"), self.a("dave")]
        d = evaluate(self.policy, self.request, approvals, evaluation_tick=50)
        self.assertEqual("DENY", d.state)
        self.assertIn("AUTHORIZED_VETO", d.reason_codes)

    def test_owner_veto_denies(self):
        approvals = [self.a("alice", decision="DENY", group=None), self.a("bob", group="security"), self.a("dave")]
        d = evaluate(self.policy, self.request, approvals, evaluation_tick=50)
        self.assertEqual("DENY", d.state)

    def test_non_veto_operator_deny_does_not_veto(self):
        approvals = [self.a("bob", group="security"), self.a("alice"), self.a("dave", decision="DENY", group=None)]
        d = evaluate(self.policy, self.request, approvals, evaluation_tick=50)
        self.assertEqual("PENDING", d.state)
        self.assertIn(("dave", "DENY_WITHOUT_POLICY_VETO_POWER"), d.ignored_approvals)

    def test_duplicate_identical_approval_not_double_counted(self):
        alice = self.a("alice")
        approvals = [self.a("bob", group="security"), alice, copy.deepcopy(alice)]
        d = evaluate(self.policy, self.request, approvals, evaluation_tick=50)
        self.assertEqual("PENDING", d.state)
        counted = dict(d.counted_approvals)
        self.assertEqual(("alice",), counted["operations"])

    def test_contradictory_same_principal_freezes(self):
        a1 = self.a("alice")
        a2 = self.a("alice", decision="DENY", group=None)
        d = evaluate(self.policy, self.request, [a1, a2], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("CONTRADICTORY_APPROVALS", d.reason_codes)

    def test_unknown_approver_freezes(self):
        a = self.a("alice")
        a["principal_id"] = "mallory"
        d = evaluate(self.policy, self.request, [a], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("UNKNOWN_APPROVER", d.reason_codes)

    def test_wrong_request_hash_freezes(self):
        a = self.a("alice")
        a["request_sha256"] = "0" * 64
        d = evaluate(self.policy, self.request, [a], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("APPROVAL_REQUEST_HASH_MISMATCH", d.reason_codes)

    def test_wrong_policy_version_freezes(self):
        a = self.a("alice")
        a["policy_version"] = 99
        d = evaluate(self.policy, self.request, [a], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("APPROVAL_POLICY_VERSION_MISMATCH", d.reason_codes)

    def test_request_policy_version_mismatch_freezes(self):
        r = copy.deepcopy(self.request)
        r["policy_version"] = 2
        d = evaluate(self.policy, r, [], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("REQUEST_POLICY_VERSION_MISMATCH", d.reason_codes)

    def test_expired_approval_is_ignored(self):
        approvals = [self.a("bob", group="security"), self.a("alice", vu=10), self.a("dave")]
        d = evaluate(self.policy, self.request, approvals, evaluation_tick=50)
        self.assertEqual("PENDING", d.state)
        self.assertIn(("alice", "APPROVAL_EXPIRED"), d.ignored_approvals)

    def test_future_approval_is_ignored(self):
        approvals = [self.a("bob", group="security"), self.a("alice", vf=60), self.a("dave")]
        d = evaluate(self.policy, self.request, approvals, evaluation_tick=50)
        self.assertEqual("PENDING", d.state)
        self.assertIn(("alice", "APPROVAL_NOT_YET_VALID"), d.ignored_approvals)

    def test_requester_self_approval_is_ignored(self):
        approvals = [self.a("bob", group="security"), self.a("alice"), self.a("carol")]
        d = evaluate(self.policy, self.request, approvals, evaluation_tick=50)
        self.assertEqual("PENDING", d.state)
        self.assertIn(("carol", "REQUESTER_SELF_APPROVAL_FORBIDDEN"), d.ignored_approvals)

    def test_inactive_approver_is_ignored(self):
        p = copy.deepcopy(self.policy)
        for principal in p["principals"]:
            if principal["principal_id"] == "dave":
                principal["active"] = False
        d = evaluate(p, self.request, [], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("QUORUM_UNSATISFIABLE_FOR_REQUESTER", d.reason_codes)

    def test_requester_inactive_denied(self):
        p = copy.deepcopy(self.policy)
        for principal in p["principals"]:
            if principal["principal_id"] == "carol":
                principal["active"] = False
        d = evaluate(p, self.request, [], evaluation_tick=50)
        self.assertEqual("DENY", d.state)
        self.assertIn("REQUESTER_INACTIVE", d.reason_codes)

    def test_requester_wrong_domain_denied(self):
        r = copy.deepcopy(self.request)
        r["requester_id"] = "erin"
        d = evaluate(self.policy, r, [], evaluation_tick=50)
        self.assertEqual("DENY", d.state)
        self.assertIn("REQUESTER_DOMAIN_DENIED", d.reason_codes)

    def test_requester_wrong_role_denied(self):
        p = copy.deepcopy(self.policy)
        p["principals"].append({"principal_id": "viewer", "roles": ["AUDITOR"], "domains": ["DEPLOY"], "active": True})
        r = copy.deepcopy(self.request)
        r["requester_id"] = "viewer"
        d = evaluate(p, r, [], evaluation_tick=50)
        self.assertEqual("DENY", d.state)
        self.assertIn("REQUESTER_ROLE_DENIED", d.reason_codes)

    def test_unknown_action_denied_not_guessed(self):
        r = copy.deepcopy(self.request)
        r["action"] = "DELETE_WORLD"
        d = evaluate(self.policy, r, [], evaluation_tick=50)
        self.assertEqual("DENY", d.state)
        self.assertIn("NO_AUTHORIZATION_RULE", d.reason_codes)

    def test_wrong_group_freezes(self):
        a = self.a("alice")
        a["group_id"] = "ghost"
        d = evaluate(self.policy, self.request, [a], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("UNKNOWN_APPROVAL_GROUP", d.reason_codes)

    def test_ineligible_role_for_group_freezes(self):
        a = self.a("alice", group="security")
        d = evaluate(self.policy, self.request, [a], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("APPROVER_ROLE_NOT_ELIGIBLE", d.reason_codes)

    def test_policy_rejects_duplicate_principal(self):
        p = copy.deepcopy(self.policy)
        p["principals"].append(copy.deepcopy(p["principals"][0]))
        report = validate_policy(p)
        self.assertFalse(report.ok)
        self.assertIn("DUPLICATE_PRINCIPAL_ID", {x.code for x in report.findings})

    def test_policy_rejects_ambiguous_selector(self):
        p = copy.deepcopy(self.policy)
        duplicate = copy.deepcopy(p["rules"][0])
        duplicate["rule_id"] = "deploy-production-copy"
        p["rules"].append(duplicate)
        report = validate_policy(p)
        self.assertFalse(report.ok)
        self.assertIn("AMBIGUOUS_RULE_SELECTOR", {x.code for x in report.findings})

    def test_policy_rejects_unsatisfiable_group(self):
        p = copy.deepcopy(self.policy)
        p["rules"][0]["approval_groups"][0]["threshold"] = 2
        report = validate_policy(p)
        self.assertFalse(report.ok)
        self.assertIn("UNSATISFIABLE_GROUP", {x.code for x in report.findings})

    def test_policy_fingerprint_stable_under_ordering(self):
        a = copy.deepcopy(self.policy)
        b = copy.deepcopy(self.policy)
        b["principals"] = list(reversed(b["principals"]))
        b["rules"] = list(reversed(b["rules"]))
        for rule in b["rules"]:
            rule["approval_groups"] = list(reversed(rule["approval_groups"]))
            rule["requester_roles"] = list(reversed(rule["requester_roles"]))
            rule["veto_roles"] = list(reversed(rule["veto_roles"]))
        self.assertEqual(policy_sha256(a), policy_sha256(b))

    def test_request_hash_changes_when_payload_changes(self):
        r = copy.deepcopy(self.request)
        self.assertEqual(request_sha256(r), request_sha256(copy.deepcopy(r)))
        r["payload_sha256"] = "b" * 64
        self.assertNotEqual(request_sha256(self.request), request_sha256(r))

    def test_approval_input_order_never_changes_allow_decision(self):
        approvals = self.allow_set()
        baseline = evaluate(self.policy, self.request, approvals, evaluation_tick=50).to_dict()
        for perm in itertools.permutations(approvals):
            with self.subTest(order=[x["principal_id"] for x in perm]):
                self.assertEqual(baseline, evaluate(self.policy, self.request, list(perm), evaluation_tick=50).to_dict())

    def test_finance_rule_requires_owner_and_finance(self):
        r = {
            "request_id": "req-fin-1",
            "requester_id": "alice",
            "domain": "FINANCE",
            "action": "PAYOUT",
            "target_id": "invoice-42",
            "payload_sha256": "c" * 64,
            "policy_version": 1,
        }
        owner = approval_for(self.policy, r, "alice", "APPROVE", "owner")
        finance = approval_for(self.policy, r, "erin", "APPROVE", "finance")
        d = evaluate(self.policy, r, [owner, finance], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("QUORUM_UNSATISFIABLE_FOR_REQUESTER", d.reason_codes)

    def test_finance_request_by_finance_is_satisfiable_with_owner_and_distinct_finance_if_added(self):
        p = copy.deepcopy(self.policy)
        p["principals"].append({"principal_id": "frank", "roles": ["FINANCE"], "domains": ["FINANCE"], "active": True})
        r = {
            "request_id": "req-fin-2",
            "requester_id": "erin",
            "domain": "FINANCE",
            "action": "PAYOUT",
            "target_id": "invoice-43",
            "payload_sha256": "d" * 64,
            "policy_version": 1,
        }
        approvals = [
            approval_for(p, r, "alice", "APPROVE", "owner"),
            approval_for(p, r, "frank", "APPROVE", "finance"),
        ]
        d = evaluate(p, r, approvals, evaluation_tick=50)
        self.assertEqual("ALLOW", d.state)

    def test_any_eligible_deny_mode_denies_finance(self):
        p = copy.deepcopy(self.policy)
        p["principals"].append({"principal_id": "frank", "roles": ["FINANCE"], "domains": ["FINANCE"], "active": True})
        r = {
            "request_id": "req-fin-3",
            "requester_id": "erin",
            "domain": "FINANCE",
            "action": "PAYOUT",
            "target_id": "invoice-44",
            "payload_sha256": "e" * 64,
            "policy_version": 1,
        }
        approvals = [approval_for(p, r, "frank", "DENY", None)]
        d = evaluate(p, r, approvals, evaluation_tick=50)
        self.assertEqual("DENY", d.state)
        self.assertIn("AUTHORIZED_DENY", d.reason_codes)

    def test_policy_not_object_is_rejected(self):
        report = validate_policy([])
        self.assertFalse(report.ok)
        self.assertEqual("POLICY_NOT_OBJECT", report.findings[0].code)

    def test_policy_missing_top_level_fields_is_rejected(self):
        report = validate_policy({})
        self.assertFalse(report.ok)
        self.assertEqual({"MISSING_FIELD"}, {x.code for x in report.findings})

    def test_policy_rejects_malformed_principal_fields(self):
        p = copy.deepcopy(self.policy)
        p["principals"][0] = {
            "principal_id": "!bad",
            "roles": ["OWNER", "OWNER"],
            "domains": ["DEPLOY", "DEPLOY"],
            "active": "yes",
        }
        codes = {x.code for x in validate_policy(p).findings}
        self.assertTrue({"INVALID_PRINCIPAL_ID", "DUPLICATE_ROLE", "DUPLICATE_DOMAIN", "INVALID_ACTIVE"} <= codes)

    def test_policy_rejects_non_object_principal_and_empty_lists(self):
        p = copy.deepcopy(self.policy)
        p["principals"] = ["alice"]
        p["rules"] = []
        codes = {x.code for x in validate_policy(p).findings}
        self.assertIn("PRINCIPAL_NOT_OBJECT", codes)
        self.assertIn("RULES_REQUIRED", codes)

    def test_policy_rejects_malformed_rule_fields(self):
        p = copy.deepcopy(self.policy)
        p["rules"][0] = {
            "rule_id": "!",
            "domain": "!",
            "action": "!",
            "requester_roles": [],
            "approval_groups": [],
            "veto_roles": "OWNER",
            "deny_mode": "MAGIC",
            "requester_may_approve": "no",
            "min_distinct_approvers": -1,
        }
        codes = {x.code for x in validate_policy(p).findings}
        expected = {
            "INVALID_RULE_ID", "INVALID_RULE_DOMAIN", "INVALID_RULE_ACTION",
            "INVALID_REQUESTER_ROLES", "INVALID_VETO_ROLES", "INVALID_DENY_MODE",
            "INVALID_REQUESTER_APPROVAL_FLAG", "INVALID_MIN_DISTINCT", "APPROVAL_GROUPS_REQUIRED",
        }
        self.assertTrue(expected <= codes)

    def test_policy_rejects_non_object_rule(self):
        p = copy.deepcopy(self.policy)
        p["rules"] = ["rule"]
        codes = {x.code for x in validate_policy(p).findings}
        self.assertIn("RULE_NOT_OBJECT", codes)

    def test_policy_rejects_malformed_group(self):
        p = copy.deepcopy(self.policy)
        p["rules"][0]["approval_groups"] = [
            "group",
            {"group_id": "!", "eligible_roles": [], "threshold": 0},
        ]
        codes = {x.code for x in validate_policy(p).findings}
        self.assertTrue({"GROUP_NOT_OBJECT", "INVALID_GROUP_ID", "INVALID_ELIGIBLE_ROLES", "INVALID_THRESHOLD"} <= codes)

    def test_policy_rejects_duplicate_group_and_rule_ids_and_min_distinct(self):
        p = copy.deepcopy(self.policy)
        g = copy.deepcopy(p["rules"][0]["approval_groups"][0])
        p["rules"][0]["approval_groups"].append(g)
        p["rules"][0]["min_distinct_approvers"] = 99
        duplicate_rule = copy.deepcopy(p["rules"][1])
        p["rules"].append(duplicate_rule)
        codes = {x.code for x in validate_policy(p).findings}
        self.assertIn("DUPLICATE_GROUP_ID", codes)
        self.assertIn("UNSATISFIABLE_MIN_DISTINCT", codes)
        self.assertIn("DUPLICATE_RULE_ID", codes)
        self.assertIn("AMBIGUOUS_RULE_SELECTOR", codes)

    def test_request_not_object_and_malformed_request_rejected(self):
        self.assertIn("REQUEST_NOT_OBJECT", {x.code for x in validate_request([]).findings})
        bad = {
            "request_id": "!",
            "requester_id": "!",
            "domain": "!",
            "action": "!",
            "target_id": "!",
            "payload_sha256": "XYZ",
            "policy_version": 0,
        }
        codes = {x.code for x in validate_request(bad).findings}
        self.assertTrue({"INVALID_ID", "INVALID_PAYLOAD_HASH", "INVALID_POLICY_VERSION"} <= codes)
        self.assertIn("MISSING_FIELD", {x.code for x in validate_request({}).findings})

    def test_evaluate_invalid_policy_and_request_freeze(self):
        bad_policy = copy.deepcopy(self.policy)
        bad_policy["version"] = 0
        d = evaluate(bad_policy, self.request, [], evaluation_tick=1)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("POLICY_INVALID", d.reason_codes)
        bad_request = copy.deepcopy(self.request)
        bad_request["payload_sha256"] = "bad"
        d = evaluate(self.policy, bad_request, [], evaluation_tick=1)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("REQUEST_INVALID", d.reason_codes)

    def test_unknown_requester_freezes(self):
        r = copy.deepcopy(self.request)
        r["requester_id"] = "ghost"
        d = evaluate(self.policy, r, [], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("UNKNOWN_REQUESTER", d.reason_codes)

    def test_malformed_approvals_freeze(self):
        cases = [
            ["not-an-object"],
            [{"principal_id": "alice"}],
        ]
        malformed = self.a("alice")
        malformed["decision"] = "ABSTAIN"
        cases.append([malformed])
        invalid_validity = self.a("alice")
        invalid_validity["valid_from_tick"] = 99
        invalid_validity["valid_until_tick"] = 1
        cases.append([invalid_validity])
        for approvals in cases:
            with self.subTest(approvals=approvals):
                d = evaluate(self.policy, self.request, approvals, evaluation_tick=50)
                self.assertEqual("FREEZE", d.state)

    def test_approver_domain_violation_freezes(self):
        a = approval_for(self.policy, self.request, "erin", "DENY", None)
        d = evaluate(self.policy, self.request, [a], evaluation_tick=50)
        self.assertEqual("FREEZE", d.state)
        self.assertIn("APPROVER_DOMAIN_VIOLATION", d.reason_codes)

    def test_inactive_approver_is_ignored_when_runtime_still_satisfiable(self):
        p = copy.deepcopy(self.policy)
        p["principals"].append({"principal_id": "frank", "roles": ["OPERATOR"], "domains": ["DEPLOY"], "active": True})
        for principal in p["principals"]:
            if principal["principal_id"] == "dave":
                principal["active"] = False
        approvals = [
            approval_for(p, self.request, "bob", "APPROVE", "security"),
            approval_for(p, self.request, "alice", "APPROVE", "operations"),
            approval_for(p, self.request, "dave", "APPROVE", "operations"),
            approval_for(p, self.request, "frank", "APPROVE", "operations"),
        ]
        d = evaluate(p, self.request, approvals, evaluation_tick=50)
        self.assertEqual("ALLOW", d.state)
        self.assertIn(("dave", "APPROVER_INACTIVE"), d.ignored_approvals)

    def test_requester_can_approve_when_policy_allows(self):
        p = copy.deepcopy(self.policy)
        p["rules"][0]["requester_may_approve"] = True
        approvals = [
            approval_for(p, self.request, "bob", "APPROVE", "security"),
            approval_for(p, self.request, "alice", "APPROVE", "operations"),
            approval_for(p, self.request, "carol", "APPROVE", "operations"),
        ]
        d = evaluate(p, self.request, approvals, evaluation_tick=50)
        self.assertEqual("ALLOW", d.state)
        self.assertIn("carol", dict(d.counted_approvals)["operations"])

    def test_invalid_evaluation_tick_raises(self):
        with self.assertRaises(ValueError):
            evaluate(self.policy, self.request, [], evaluation_tick=-1)


if __name__ == "__main__":
    unittest.main()
