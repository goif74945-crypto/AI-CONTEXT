from __future__ import annotations
import importlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
REGISTRY=ROOT/"skills/registry/registry.json"
PDF_SHA256="a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c"
TARGETS={
"GOV-001":"nexy-authority","GOV-002":"nexy-scope-guard","CTX-001":"nexy-context",
"CTX-003":"nexy-source-inspector","REQ-001":"nexy-requirement","ARC-001":"nexy-architecture",
"ARC-004":"nexy-architecture-impact"
}
HEADINGS=["Identity","Objective","Authority","Source of Truth","Scope","Inputs","Preconditions","Outputs","Workflow",
"Required Behavior","Forbidden Behavior","Architecture Constraints","Security Constraints","Compatibility Constraints",
"Data Integrity","Failure Handling","Freeze Conditions","Validation","Completion Criteria","Stop Conditions","Checkpoint",
"Resume","Error Reporting","Examples","Non-Goals","Version"]

def main():
    errors=[]
    data=json.loads(REGISTRY.read_text(encoding="utf-8"))
    skills=data.get("skills",[])
    by_id={e.get("id"):e for e in skills if isinstance(e,dict)}
    if data.get("registry_id")!="AI-CONTEXT-SKILL-REGISTRY": errors.append("registry identity mismatch")
    if len(skills)!=228: errors.append(f"canonical registry count mismatch: {len(skills)}")
    if set(k for k in by_id if k.startswith(("GOV-","CTX-","REQ-","ARC-"))) == set(): errors.append("no formal target IDs in canonical registry")
    records=[]
    for sid,name in TARGETS.items():
        e=by_id.get(sid)
        if not e: errors.append(f"{sid}: missing canonical registry entry"); continue
        if e.get("name")!=name: errors.append(f"{sid}: name mismatch")
        p=ROOT/e.get("source_path","")
        if not p.is_file(): errors.append(f"{sid}: missing source file")
        else:
            txt=p.read_text(encoding="utf-8")
            for h in HEADINGS:
                if f"## {h}" not in txt and f"### {h}" not in txt: errors.append(f"{sid}: missing heading {h}")
            if PDF_SHA256 not in txt: errors.append(f"{sid}: source hash missing")
        for key in ("implementation","load_path","locator","permissions","validation","source_basis","validator","evidence_handler","tests"):
            if not e.get(key): errors.append(f"{sid}: missing {key}")
        try:
            mod,fn=e["locator"].split(":",1)
            if not callable(getattr(importlib.import_module(mod),fn)): errors.append(f"{sid}: runtime entry not callable")
            vmod,vfn=e["validator"].split(":",1)
            if not callable(getattr(importlib.import_module(vmod),vfn)): errors.append(f"{sid}: validator not callable")
            emod,efn=e["evidence_handler"].split(":",1)
            if not callable(getattr(importlib.import_module(emod),efn)): errors.append(f"{sid}: evidence handler not callable")
        except Exception as exc:
            errors.append(f"{sid}: callable import failed: {exc}")
        records.append({"id":sid,"name":name,"status":e.get("status"),"implementation":e.get("implementation"),"load_path":e.get("load_path"),"locator":e.get("locator"),"source_path":e.get("source_path")})
    result={"audit_id":"AUD-NEXY-SKILL-RUNTIME-002","registry_id":data.get("registry_id"),"registry_count":len(skills),
            "baseline_preserved":len(skills)-len(TARGETS)==221,"target_count":7,"errors":errors,"status":"PASS" if not errors else "FAIL","records":records}
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
    raise SystemExit(0 if not errors else 1)

if __name__=="__main__": main()
