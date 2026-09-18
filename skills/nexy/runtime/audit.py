from __future__ import annotations
import importlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
REGISTRY=ROOT/"skills/nexy/registry/skills.json"
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
    skills=data.get("skills",{})
    if data.get("registry_id")!="REG-NEXY-SKILL-001": errors.append("registry identity mismatch")
    if set(skills)!=set(TARGETS): errors.append("target ID set mismatch")
    records=[]
    for sid,name in TARGETS.items():
        e=skills.get(sid)
        if not e: errors.append(f"{sid}: missing registry entry"); continue
        if e.get("name")!=name: errors.append(f"{sid}: name mismatch")
        p=ROOT/e.get("source_path","")
        if not p.is_file(): errors.append(f"{sid}: missing source file")
        else:
            txt=p.read_text(encoding="utf-8")
            for h in HEADINGS:
                if f"## {h}" not in txt and f"### {h}" not in txt: errors.append(f"{sid}: missing heading {h}")
            if PDF_SHA256 not in txt: errors.append(f"{sid}: source hash missing")
        try:
            mod,fn=e["runtime_entry"].split(":",1)
            obj=getattr(importlib.import_module(mod),fn)
            if not callable(obj): errors.append(f"{sid}: runtime entry not callable")
        except Exception as exc:
            errors.append(f"{sid}: runtime entry import failed: {exc}")
        for key in ("permissions","validator","evidence_handler","tests"):
            if not e.get(key): errors.append(f"{sid}: missing {key}")
        records.append({"id":sid,"name":name,"runtime_entry":e.get("runtime_entry"),"source_path":e.get("source_path")})
    result={"audit_id":"AUD-NEXY-SKILL-RUNTIME-001","registry_id":data.get("registry_id"),"registry_count":len(skills),"target_count":7,
            "errors":errors,"status":"PASS" if not errors else "FAIL","records":records}
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
    raise SystemExit(0 if not errors else 1)

if __name__=="__main__":
    main()
