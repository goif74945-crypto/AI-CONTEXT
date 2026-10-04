from __future__ import annotations
from dataclasses import dataclass, asdict
from fnmatch import fnmatch
from hashlib import sha256
import json


def _canon(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)

@dataclass(frozen=True)
class Lease:
    issuer:str; subject:str; capability:str; resources:tuple[str,...]; actions:tuple[str,...]
    not_before:int; expires_at:int; max_uses:int; parent_id:str|None=None
    def lease_id(self)->str:
        return sha256(_canon(asdict(self)).encode()).hexdigest()


def validate_child(parent:Lease, child:Lease)->dict:
    errors=[]
    if child.issuer != parent.subject: errors.append("issuer_not_parent_subject")
    if child.capability != parent.capability: errors.append("capability_escalation")
    if not set(child.actions).issubset(parent.actions): errors.append("action_escalation")
    if child.not_before < parent.not_before or child.expires_at > parent.expires_at: errors.append("time_escalation")
    if child.max_uses > parent.max_uses: errors.append("usage_escalation")
    for cr in child.resources:
        if not any(_pattern_subset(cr,pr) for pr in parent.resources): errors.append(f"resource_escalation:{cr}")
    if child.parent_id != parent.lease_id(): errors.append("parent_lineage_mismatch")
    return {"status":"FREEZE" if errors else "PASS","errors":errors}


def _pattern_subset(child:str,parent:str)->bool:
    if parent=="*": return True
    if child==parent: return True
    if parent.endswith("*"):
        prefix=parent[:-1]
        return child.startswith(prefix) and "*" not in child[len(prefix):]
    return False


def authorize(lease:Lease, *, now:int, subject:str, capability:str, resource:str, action:str, uses:int, revoked_ids:set[str]|None=None)->dict:
    revoked_ids=revoked_ids or set(); lid=lease.lease_id()
    checks=[
      (lid not in revoked_ids,"revoked"),
      (lease.not_before<=now<lease.expires_at,"outside_time_window"),
      (subject==lease.subject,"subject_mismatch"),
      (capability==lease.capability,"capability_mismatch"),
      (action in lease.actions,"action_not_allowed"),
      (any(fnmatch(resource,p) for p in lease.resources),"resource_not_allowed"),
      (uses < lease.max_uses,"usage_exhausted"),
    ]
    failed=[reason for ok,reason in checks if not ok]
    return {"status":"FREEZE" if failed else "PASS","lease_id":lid,"reasons":failed}
