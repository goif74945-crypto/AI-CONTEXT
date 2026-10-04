import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
from ncmde import DEFAULT_POLICY, ValidationError, evaluate

NOW = "2026-10-05T01:30:00+07:00"
START = "2026-10-05T01:00:00+07:00"
END = "2026-10-05T05:00:00+07:00"

def m(mid="candidate", **changes):
    data = {
        "schema_version": "1.0",
        "mission_id": mid,
        "objective": "Build deterministic cache coherence research",
        "domains": ["cache-coherence", "verification"],
        "capabilities": ["invalidation", "evidence-binding"],
        "deliverables": ["architecture", "python-engine", "tests"],
        "write_claims": [{"path": "work/" + mid, "kind": "TREE"}],
        "protected_claims": [{"path": "projects/NEXY.AI", "kind": "TREE"}],
        "exclusive_resources": [],
        "exclusive_authorities": [],
        "started_at": START,
        "lease_expires_at": END,
        "status": "DRAFT" if mid == "candidate" else "ACTIVE",
    }
    data.update(changes)
    return data

class NCMDETests(unittest.TestCase):
    def test_empty_registry(self):
        self.assertEqual(evaluate(m(), [], now=NOW)["decision"], "PROCEED")

    def test_same_file_freezes(self):
        c=m(write_claims=[{"path":"x/a.txt","kind":"FILE"}])
        i=m("i",write_claims=[{"path":"x/a.txt","kind":"FILE"}])
        self.assertEqual(evaluate(c,[i],now=NOW)["decision"],"FREEZE")

    def test_tree_contains_file_freezes(self):
        c=m(write_claims=[{"path":"x","kind":"TREE"}])
        i=m("i",write_claims=[{"path":"x/a.txt","kind":"FILE"}])
        self.assertEqual(evaluate(c,[i],now=NOW)["decision"],"FREEZE")

    def test_sibling_files_proceed(self):
        c=m(write_claims=[{"path":"x/a.txt","kind":"FILE"}],domains=["a"],capabilities=["a"],deliverables=["a"],objective="A")
        i=m("i",write_claims=[{"path":"x/b.txt","kind":"FILE"}],domains=["b"],capabilities=["b"],deliverables=["b"],objective="B")
        self.assertEqual(evaluate(c,[i],now=NOW)["decision"],"PROCEED")

    def test_protected_scope_freezes(self):
        c=m(write_claims=[{"path":"protected/child","kind":"TREE"}])
        i=m("i",protected_claims=[{"path":"protected","kind":"TREE"}],domains=["b"],capabilities=["b"],deliverables=["b"],objective="B")
        out=evaluate(c,[i],now=NOW)
        self.assertEqual(out["decision"],"FREEZE")
        self.assertIn("CANDIDATE_WRITE_HITS_INCUMBENT_PROTECTED_SCOPE",out["reason_codes"])

    def test_exclusive_resource_freezes(self):
        c=m(exclusive_resources=["gpu:0"])
        i=m("i",exclusive_resources=["GPU:0"],domains=["b"],capabilities=["b"],deliverables=["b"],objective="B")
        self.assertEqual(evaluate(c,[i],now=NOW)["decision"],"FREEZE")

    def test_exclusive_authority_freezes(self):
        c=m(exclusive_authorities=["release:alpha"])
        i=m("i",exclusive_authorities=["RELEASE:ALPHA"],domains=["b"],capabilities=["b"],deliverables=["b"],objective="B")
        self.assertEqual(evaluate(c,[i],now=NOW)["decision"],"FREEZE")

    def test_high_overlap_deconflicts(self):
        i=m("i",write_claims=[{"path":"other/i","kind":"TREE"}])
        out=evaluate(m(),[i],now=NOW)
        self.assertEqual(out["decision"],"DECONFLICT")
        self.assertGreaterEqual(out["comparisons"][0]["overlap_bps"],7600)

    def test_moderate_overlap_coexists(self):
        c=m(domains=["privacy","context"],capabilities=["filter","receipt"],deliverables=["architecture","tests"],objective="Privacy context filter")
        i=m("i",write_claims=[{"path":"other/i","kind":"TREE"}],domains=["privacy","context","egress"],capabilities=["filter","receipt","retention"],deliverables=["architecture","tests","python-engine"],objective="Privacy context egress firewall")
        self.assertEqual(evaluate(c,[i],now=NOW)["decision"],"COEXIST")

    def test_low_overlap_proceeds(self):
        i=m("i",write_claims=[{"path":"other/i","kind":"TREE"}],domains=["privacy"],capabilities=["redaction"],deliverables=["policy"],objective="Privacy firewall")
        self.assertEqual(evaluate(m(),[i],now=NOW)["decision"],"PROCEED")

    def test_expired_incumbent_ignored(self):
        i=m("i",lease_expires_at="2026-10-05T01:10:00+07:00",write_claims=m()["write_claims"])
        out=evaluate(m(),[i],now=NOW)
        self.assertEqual(out["decision"],"PROCEED")
        self.assertFalse(out["comparisons"][0]["active"])

    def test_completed_incumbent_ignored(self):
        i=m("i",status="COMPLETED",write_claims=m()["write_claims"])
        self.assertEqual(evaluate(m(),[i],now=NOW)["decision"],"PROCEED")

    def test_missing_domains_rejected(self):
        c=m(); c["domains"]=[]
        with self.assertRaisesRegex(ValidationError,"domains:EMPTY_SET"):
            evaluate(c,[],now=NOW)

    def test_glob_rejected(self):
        with self.assertRaisesRegex(ValidationError,"PATH_GLOB_FORBIDDEN"):
            evaluate(m(write_claims=[{"path":"x/*","kind":"TREE"}]),[],now=NOW)

    def test_traversal_rejected(self):
        with self.assertRaisesRegex(ValidationError,"PATH_AMBIGUOUS_SEGMENT"):
            evaluate(m(write_claims=[{"path":"x/../y","kind":"TREE"}]),[],now=NOW)

    def test_naive_time_rejected(self):
        with self.assertRaisesRegex(ValidationError,"TIMESTAMP_REQUIRES_TIMEZONE"):
            evaluate(m(),[],now="2026-10-05T01:30:00")

    def test_oversized_lease_rejected(self):
        with self.assertRaisesRegex(ValidationError,"LEASE_EXCEEDS_POLICY_MAX"):
            evaluate(m(lease_expires_at="2026-10-07T01:00:00+07:00"),[],now=NOW)

    def test_registry_order_hash_stable(self):
        a=m("a",write_claims=[{"path":"a","kind":"TREE"}],domains=["a"],capabilities=["a"],deliverables=["a"],objective="A")
        b=m("b",write_claims=[{"path":"b","kind":"TREE"}],domains=["b"],capabilities=["b"],deliverables=["b"],objective="B")
        self.assertEqual(evaluate(m(),[a,b],now=NOW)["decision_hash"],evaluate(m(),[b,a],now=NOW)["decision_hash"])

    def test_set_order_hash_stable(self):
        a=m(domains=["a","b"],capabilities=["c","d"],deliverables=["e","f"])
        b=m(domains=["b","a"],capabilities=["d","c"],deliverables=["f","e"])
        self.assertEqual(evaluate(a,[],now=NOW)["decision_hash"],evaluate(b,[],now=NOW)["decision_hash"])

    def test_timezone_equivalent_hash_stable(self):
        self.assertEqual(evaluate(m(),[],now="2026-10-04T18:30:00Z")["decision_hash"],evaluate(m(),[],now=NOW)["decision_hash"])

    def test_policy_change_changes_hash(self):
        p=dict(DEFAULT_POLICY); p["coexist_threshold_bps"]=4100
        self.assertNotEqual(evaluate(m(),[],now=NOW)["decision_hash"],evaluate(m(),[],now=NOW,policy=p)["decision_hash"])

    def test_id_collision_freezes(self):
        c=m("same",status="DRAFT")
        i=m("same",write_claims=[{"path":"other","kind":"TREE"}],objective="Different",domains=["different"],capabilities=["different"],deliverables=["different"])
        out=evaluate(c,[i],now=NOW)
        self.assertEqual(out["decision"],"FREEZE")
        self.assertIn("MISSION_ID_COLLISION",out["reason_codes"])

    def test_unicode_tags_normalize(self):
        a=m(domains=["ＡＩ"],capabilities=["Verify"],deliverables=["Code"])
        b=m(domains=["ai"],capabilities=["verify"],deliverables=["code"])
        self.assertEqual(evaluate(a,[],now=NOW)["decision_hash"],evaluate(b,[],now=NOW)["decision_hash"])

    def test_unknown_status_rejected(self):
        with self.assertRaisesRegex(ValidationError,"UNKNOWN_MISSION_STATUS"):
            evaluate(m(status="MAYBE"),[],now=NOW)

    def test_duplicate_registry_id_rejected(self):
        a=m("duplicate",write_claims=[{"path":"registry/a","kind":"TREE"}],domains=["a"],capabilities=["a"],deliverables=["a"],objective="A")
        b=m("duplicate",write_claims=[{"path":"registry/b","kind":"TREE"}],domains=["b"],capabilities=["b"],deliverables=["b"],objective="B")
        with self.assertRaisesRegex(ValidationError,"DUPLICATE_REGISTRY_MISSION_ID"):
            evaluate(m(),[a,b],now=NOW)

    def test_fixture_corpus(self):
        with open(os.path.join(ROOT,"fixtures","scenarios.json"), encoding="utf-8") as handle:
            corpus=json.load(handle)
        for case in corpus["scenarios"]:
            with self.subTest(case=case["id"]):
                first=evaluate(case["candidate"],case["incumbents"],now=case["now"])
                second=evaluate(case["candidate"],list(reversed(case["incumbents"])),now=case["now"])
                self.assertEqual(first,second)
                self.assertEqual(first["decision"],case["expected"])

if __name__=="__main__":
    unittest.main()
