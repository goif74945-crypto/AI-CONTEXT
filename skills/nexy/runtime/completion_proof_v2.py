from __future__ import annotations
import importlib, json, os, re, subprocess
from pathlib import Path
from skills.nexy.runtime.runtime import SkillRuntime, REPOSITORY, BRANCH

ROOT=Path(__file__).resolve().parents[3]
REGISTRY=ROOT/"skills/registry/registry.json"
def current_head():
    value=os.environ.get("GITHUB_SHA")
    if isinstance(value,str) and re.fullmatch(r"[0-9a-f]{40}",value):
        return value
    return subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()

HEAD=current_head()
TARGETS=["GOV-001","GOV-002","CTX-001","CTX-003","REQ-001","ARC-001","ARC-004"]

def env(sid, action="ANALYZE"):
    data={"GOV-001":{"sources":[{"source_id":"CMD-0001","source_type":"CURRENT_USER_COMMAND","rank":1,"status":"VERIFIED"}]},
          "GOV-002":{"request":{"target":"skills/nexy"}},"CTX-001":{},
          "CTX-003":{"files":[{"path":"projects/NEXY.AI/architecture.md","type":"document","content_hash":"sha256:architecture"}]},
          "REQ-001":{"requirement":{"objective":"proof","in_scope":["runtime"],"out_scope":[],"input":["context"],"output":["result"],"constraint":["no guess"],"acceptance":["pass"],"validation":["V0-V9"]}},
          "ARC-001":{"architecture":{"layers":["authority","execution"],"authority_flow":["user","law"],"boundaries":["runtime"]}},
          "ARC-004":{"impact":{"affected_modules":["skills/nexy/runtime"],"affected_contracts":[],"affected_state":[],"affected_tests":["runtime"],"affected_security":["authorization"],"affected_release":["verification"]}}}
    return {"execution_id":f"EXE-{sid}-PROOF","action":action,"context":{"task":"completion proof","authority":{"source_type":"CURRENT_USER_COMMAND","source_id":"CMD-0001","rank":1},"scope":{"skill_ids":[sid],"allowed_actions":[action],"out_of_scope_skill_ids":[],"allowed_targets":["skills/nexy"]},"repository":REPOSITORY,"branch":BRANCH,"head":HEAD,"source_of_truth":[{"id":"SPEC-001","path":"skills/nexy/MASTER-SPECIFICATION.md"}],"constraints":["NO_GUESS","FAIL_CLOSED"],"expected_output":"universal skill output","validation_requirements":["V0-V9"]},"data":data[sid]}

def callable_ref(ref):
    module,fn=ref.split(":",1)
    return callable(getattr(importlib.import_module(module),fn))

def main():
    rt=SkillRuntime(REGISTRY)
    entries={e["id"]:e for e in rt.registry["skills"] if e.get("id") in TARGETS}
    assert set(entries)==set(TARGETS)
    assert len(rt.registry["skills"])==228
    assert len([e for e in rt.registry["skills"] if e.get("id") not in TARGETS])==221
    for sid,e in entries.items():
        assert callable_ref(e["locator"]); assert callable_ref(e["validator"]); assert callable_ref(e["evidence_handler"])
    success=rt.run("GOV-001",env("GOV-001"))
    assert success["status"]=="SUCCESS" and success["chain"]==["LOAD","RESOLVE","AUTHORIZE","EXECUTE","VALIDATE","EVIDENCE","RESULT"]
    failure=rt.run("GOV-001",env("GOV-001",action="WRITE"))
    assert failure["status"]=="FAILURE" and failure["failure"]["code"]=="UNAUTHORIZED"
    frozen=env("CTX-003"); frozen["data"]["files"][0]["content"]="tampered"; frozen["data"]["files"][0]["content_hash"]="sha256:"+"0"*64
    freeze=rt.run("CTX-003",frozen)
    assert freeze["status"]=="FREEZE" and freeze["failure"]["code"]=="INTEGRITY_MISMATCH"
    proof={"proof_id":"PRF-NEXY-RUNTIME-001","status":"PASS","target_count":7,"target_ids":TARGETS,
           "success":{"execution_id":success["execution_id"],"result_id":success["id"],"evidence_id":success["evidence_id"],"chain":success["chain"]},
           "failure":{"execution_id":failure["execution_id"],"result_id":failure["id"],"evidence_id":failure["evidence_id"],"code":failure["failure"]["code"]},
           "freeze":{"execution_id":freeze["execution_id"],"result_id":freeze["id"],"evidence_id":freeze["evidence_id"],"code":freeze["failure"]["code"]}}
    print(json.dumps(proof,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__": main()
