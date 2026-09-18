from __future__ import annotations
import copy, json, re, unittest
from pathlib import Path
from skills.nexy.runtime.runtime import SkillRuntime, REPOSITORY, BRANCH, UNIVERSAL_REQUIRED, UNIVERSAL_OUTPUT, sha256_hex, stable_id

ROOT=Path(__file__).resolve().parents[4]
REGISTRY=ROOT/"skills/nexy/registry/skills.json"
HEAD="0123456789abcdef0123456789abcdef01234567"
TARGETS={
"GOV-001":{"data":{"sources":[{"source_id":"DOC-CMD-001","source_type":"CURRENT_USER_COMMAND","rank":1,"status":"VERIFIED"}]}},
"GOV-002":{"data":{"request":{"target":"skills/nexy"}}},
"CTX-001":{"data":{}},
"CTX-003":{"data":{"files":[{"path":"projects/NEXY.AI/architecture.md","type":"document","content_hash":"sha256:architecture","dependencies":[],"callers":[],"callees":[],"contracts":[],"tests":[]}]}},
"REQ-001":{"data":{"requirement":{"objective":"Test runtime","in_scope":["runtime"],"out_scope":["unrelated"],"input":["context"],"output":["result"],"constraint":["no guess"],"acceptance":["pass"],"validation":["tests"]}}},
"ARC-001":{"data":{"architecture":{"layers":["authority","execution","vault"],"authority_flow":["user","law","core"],"boundaries":["context","runtime"]}}},
"ARC-004":{"data":{"impact":{"affected_modules":["skills/nexy/runtime"],"affected_contracts":[],"affected_state":[],"affected_tests":["runtime"],"affected_security":["authorization"],"affected_release":["verification"]}}}
}
def env(sid, action="ANALYZE", **kw):
    c={"task":"validate canonical skill runtime","authority":{"source_type":"CURRENT_USER_COMMAND","source_id":"CMD-0001","rank":1},"scope":{"skill_ids":[sid],"allowed_actions":[action],"out_of_scope_skill_ids":[],"allowed_targets":["skills/nexy"]},"repository":kw.get("repo",REPOSITORY),"branch":kw.get("branch",BRANCH),"head":HEAD,"source_of_truth":[{"id":"SPEC-001","path":"skills/nexy/MASTER-SPECIFICATION.md","hash":"a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c"}],"constraints":["NO_GUESS","FAIL_CLOSED"],"expected_output":"universal skill output","validation_requirements":["V0-V9"]}
    x={"execution_id":f"EXE-{sid}-001","action":action,"context":c}
    x.update(copy.deepcopy(TARGETS[sid])); return x

class RuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.rt=SkillRuntime(REGISTRY)

    def test_registry_binding_7_of_7(self):
        self.assertEqual(set(self.rt.registry["skills"]),set(TARGETS))
        for sid,e in self.rt.registry["skills"].items():
            self.assertEqual(sid,e["id"]); self.assertIn("SKILL.md",e["source_path"]); self.assertIn(":",e["runtime_entry"])

    def test_loader_and_resolver(self):
        for sid,e in self.rt.registry["skills"].items():
            mod,fn=e["runtime_entry"].split(":",1)
            loaded=getattr(__import__(mod,fromlist=[fn]),fn); self.assertTrue(callable(loaded))

    def test_all_target_skills_execute(self):
        expected=["LOAD","RESOLVE","AUTHORIZE","EXECUTE","VALIDATE","EVIDENCE","RESULT"]
        for sid in TARGETS:
            with self.subTest(sid=sid):
                r=self.rt.run(sid,env(sid))
                self.assertEqual(r["status"],"SUCCESS"); self.assertEqual(r["chain"],expected)
                self.assertRegex(r["id"],r"^RES-[0-9A-F]{16}$"); self.assertRegex(r["evidence_id"],r"^EVD-[0-9A-F]{16}$")
                self.assertEqual(r["evidence_id"],r["skill_output"]["evidence"][0]["id"])

    def test_authorization_and_permission_enforcement(self):
        self.assertEqual(self.rt.run("GOV-001",env("GOV-001",action="READ"))["status"],"SUCCESS")
        r=self.rt.run("GOV-001",env("GOV-001",action="WRITE")); self.assertEqual(r["failure"]["code"],"UNAUTHORIZED")

    def test_invalid_authority(self):
        p=env("GOV-001"); p["context"]["authority"]={"source_type":"BOGUS","source_id":"X","rank":99}
        r=self.rt.run("GOV-001",p); self.assertEqual(r["failure"]["code"],"UNAUTHORIZED")

    def test_scope_violation(self):
        p=env("GOV-002"); p["context"]["scope"]["out_of_scope_skill_ids"]=["GOV-002"]
        r=self.rt.run("GOV-002",p); self.assertEqual(r["failure"]["code"],"SCOPE_VIOLATION")

    def test_repository_mismatch(self):
        r=self.rt.run("GOV-001",env("GOV-001",repo="other/repo")); self.assertEqual(r["failure"]["code"],"REPOSITORY_MISMATCH")

    def test_branch_mismatch(self):
        r=self.rt.run("GOV-001",env("GOV-001",branch="dev")); self.assertEqual(r["failure"]["code"],"BRANCH_MISMATCH")

    def test_invalid_skill_id(self):
        r=self.rt.run("NO-SUCH-SKILL",env("GOV-001")); self.assertEqual(r["failure"]["code"],"INVALID_SKILL_ID")

    def test_invalid_execution_context(self):
        p=env("ARC-004"); del p["context"]["head"]
        r=self.rt.run("ARC-004",p); self.assertEqual(r["failure"]["code"],"INVALID_INPUT")

    def test_missing_universal_input(self):
        p=env("GOV-001"); del p["context"]["source_of_truth"]
        r=self.rt.run("GOV-001",p); self.assertEqual(r["failure"]["code"],"INVALID_INPUT")

    def test_authority_conflict_freezes(self):
        p=env("GOV-001"); p["data"]["sources"]=[{"source_id":"A","source_type":"CURRENT_USER_COMMAND","rank":1},{"source_id":"B","source_type":"CURRENT_USER_COMMAND","rank":1}]
        r=self.rt.run("GOV-001",p); self.assertEqual(r["status"],"FREEZE"); self.assertEqual(r["failure"]["code"],"AUTHORITY_CONFLICT")

    def test_integrity_mismatch_freezes(self):
        p=env("CTX-003"); p["data"]["files"][0]["content"]="real content"; p["data"]["files"][0]["content_hash"]="sha256:"+"0"*64
        r=self.rt.run("CTX-003",p); self.assertEqual(r["status"],"FREEZE"); self.assertEqual(r["failure"]["code"],"INTEGRITY_MISMATCH")

    def test_failure_evidence_same_execution(self):
        r=self.rt.run("GOV-001",env("GOV-001",repo="other/repo"))
        self.assertEqual(r["evidence"]["execution_id"],r["execution_id"]); self.assertEqual(r["evidence"]["result_id"],r["id"])

    def test_identifier_traceability(self):
        r=self.rt.run("GOV-001",env("GOV-001"))
        self.assertTrue(r["id"].startswith("RES-")); self.assertTrue(r["evidence_id"].startswith("EVD-")); self.assertTrue(r["checkpoint"]["id"].startswith("CHK-"))

    def test_evidence_hash_deterministic(self):
        a=self.rt.run("GOV-001",env("GOV-001")); b=self.rt.run("GOV-001",env("GOV-001"))
        self.assertEqual(a["evidence_id"],b["evidence_id"]); self.assertEqual(a["skill_output"]["evidence"][0]["content_hash"],b["skill_output"]["evidence"][0]["content_hash"])

    def test_output_contract_fields(self):
        r=self.rt.run("REQ-001",env("REQ-001"))
        self.assertTrue(set(UNIVERSAL_OUTPUT).issubset(r["skill_output"]))

    def test_checkpoint_failure_and_freeze(self):
        f=self.rt.run("GOV-001",env("GOV-001",repo="bad/repo")); self.assertEqual(f["checkpoint"]["failed"],1)
        z=self.rt.run("GOV-001",env("GOV-001")); self.assertEqual(z["checkpoint"]["verified"],1)
        p=env("CTX-003"); p["data"]["files"][0]["content"]="x"; p["data"]["files"][0]["content_hash"]="sha256:"+"f"*64
        self.assertEqual(self.rt.run("CTX-003",p)["status"],"FREEZE")

    def test_runtime_source_is_self_contained(self):
        src=Path(__import__("skills.nexy.runtime.runtime",fromlist=["__file__"]).__file__).read_text(encoding="utf-8")
        self.assertIn("class SkillRuntime",src); self.assertIn("def authorize",src); self.assertIn("def evidence_bind",src)

if __name__=="__main__": unittest.main()
