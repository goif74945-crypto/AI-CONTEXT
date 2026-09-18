from __future__ import annotations
import hashlib, importlib, json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

REPOSITORY = "goif74945-crypto/AI-CONTEXT"
BRANCH = "main"
RUNTIME_ROOT = "skills/nexy/runtime"
RUNTIME_VERSION = "1.0.0"
PDF_SHA256 = "a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c"
UNIVERSAL_REQUIRED = ("task","authority","scope","repository","branch","head","source_of_truth","constraints","expected_output","validation_requirements")
UNIVERSAL_OUTPUT = ("status","objective","scope","inputs","actions","changed_files","unchanged_files","validation","evidence","errors","unknowns","remaining","next_action")
AUTHORITY_ORDER = {"CURRENT_USER_COMMAND":1,"PROJECT_INSTRUCTIONS":2,"MASTER_SPECIFICATION":3,"PDF":4,"REPOSITORY":5,"VALIDATION_EVIDENCE":6}

class RuntimeFault(Exception):
    def __init__(self,message:str,code:str,critical:bool=False):
        super().__init__(message); self.code=code; self.critical=critical
class InvalidInput(RuntimeFault):
    def __init__(self,m): super().__init__(m,"INVALID_INPUT")
class Unauthorized(RuntimeFault):
    def __init__(self,m): super().__init__(m,"UNAUTHORIZED")
class SkillNotFound(RuntimeFault):
    def __init__(self,m): super().__init__(m,"INVALID_SKILL_ID")
class ScopeViolation(RuntimeFault):
    def __init__(self,m): super().__init__(m,"SCOPE_VIOLATION")
class RepositoryMismatch(RuntimeFault):
    def __init__(self,m): super().__init__(m,"REPOSITORY_MISMATCH")
class BranchMismatch(RuntimeFault):
    def __init__(self,m): super().__init__(m,"BRANCH_MISMATCH")
class IntegrityFailure(RuntimeFault):
    def __init__(self,m): super().__init__(m,"INTEGRITY_MISMATCH",True)
class AuthorityConflict(RuntimeFault):
    def __init__(self,m): super().__init__(m,"AUTHORITY_CONFLICT",True)
class ValidationFailure(RuntimeFault):
    def __init__(self,m,critical:bool=False): super().__init__(m,"VALIDATION_FAILURE",critical)

@dataclass(frozen=True)
class RegistryEntry:
    id:str; name:str; source_path:str; runtime_entry:str; permissions:tuple[str,...]; validator:str; evidence_handler:str; tests:tuple[str,...]
@dataclass(frozen=True)
class AuthorizationToken:
    token_id:str; execution_id:str; skill_id:str; action:str; repository:str; branch:str; head:str; scope_hash:str

def canonical_json(v:Any)->str: return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def sha256_hex(v:Any)->str:
    b=v if isinstance(v,bytes) else canonical_json(v).encode("utf-8")
    return hashlib.sha256(b).hexdigest()
def stable_id(prefix:str,v:Any)->str: return f"{prefix}-{sha256_hex(v)[:16].upper()}"
def valid_head(h:Any)->bool:
    if not isinstance(h,str) or len(h)!=40: return False
    try: int(h,16); return True
    except ValueError: return False

def load_registry(path:str|Path)->dict[str,Any]:
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    validate_registry(data); return data

def validate_registry(data:dict[str,Any])->None:
    if data.get("registry_id")!="REG-NEXY-SKILL-001": raise ValidationFailure("Registry identity mismatch",True)
    skills=data.get("skills")
    if not isinstance(skills,dict) or len(skills)!=7: raise ValidationFailure("Registry must contain exactly 7 target Skills",True)
    seen=set()
    for sid,item in skills.items():
        req={"id","name","source_path","runtime_entry","permissions","validator","evidence_handler","tests"}
        if not req.issubset(item): raise ValidationFailure(f"Registry entry {sid} missing required fields",True)
        if sid!=item["id"] or item["name"] in seen: raise ValidationFailure(f"Registry identity/name error for {sid}",True)
        seen.add(item["name"])
    if set(skills)!={"GOV-001","GOV-002","CTX-001","CTX-003","REQ-001","ARC-001","ARC-004"}: raise ValidationFailure("Unexpected target Skill set",True)

def resolve_entry(registry:dict[str,Any],sid:str)->RegistryEntry:
    item=registry["skills"].get(sid)
    if item is None: raise SkillNotFound(f"Unknown Skill ID: {sid}")
    return RegistryEntry(item["id"],item["name"],item["source_path"],item["runtime_entry"],tuple(item["permissions"]),item["validator"],item["evidence_handler"],tuple(item["tests"]))

def load_skill(entry:RegistryEntry)->Callable[[dict[str,Any]],dict[str,Any]]:
    if ":" not in entry.runtime_entry: raise ValidationFailure(f"Invalid runtime entry: {entry.runtime_entry}",True)
    module,fn=entry.runtime_entry.split(":",1)
    obj=getattr(importlib.import_module(module),fn,None)
    if not callable(obj): raise ValidationFailure(f"Runtime entry not callable: {entry.runtime_entry}",True)
    return obj

def validate_input_contract(envelope:dict[str,Any])->None:
    if not isinstance(envelope,dict): raise InvalidInput("Execution envelope must be an object")
    ctx=envelope.get("context")
    if not isinstance(ctx,dict): raise InvalidInput("context is required")
    missing=[k for k in UNIVERSAL_REQUIRED if k not in ctx]
    if missing: raise InvalidInput("Missing required input fields: "+", ".join(missing))
    if not isinstance(ctx["scope"],dict): raise InvalidInput("scope must be an object")
    if not isinstance(ctx["source_of_truth"],list) or not ctx["source_of_truth"]: raise InvalidInput("source_of_truth must be non-empty")
    if not isinstance(ctx["constraints"],list): raise InvalidInput("constraints must be a list")
    if not envelope.get("execution_id") or not envelope.get("action"): raise InvalidInput("execution_id and action are required")

def validate_output_contract(out:dict[str,Any])->None:
    if not isinstance(out,dict): raise ValidationFailure("Skill output must be an object",True)
    missing=[k for k in UNIVERSAL_OUTPUT if k not in out]
    if missing: raise ValidationFailure("Missing output fields: "+", ".join(missing),True)

def validate_trace(trace:list[str])->None:
    expected=["LOAD","RESOLVE","AUTHORIZE","EXECUTE","VALIDATE","EVIDENCE","RESULT"]
    if trace!=expected: raise ValidationFailure(f"Execution chain mismatch: {trace}",True)

def authorize(entry:RegistryEntry,envelope:dict[str,Any])->AuthorizationToken:
    ctx=envelope["context"]; action=envelope["action"]; execution_id=envelope["execution_id"]
    if action not in entry.permissions: raise Unauthorized(f"Permission {action} is not allowed for {entry.id}")
    auth=ctx.get("authority",{})
    if not isinstance(auth,dict) or auth.get("source_type") not in AUTHORITY_ORDER or not auth.get("source_id"): raise Unauthorized("Invalid authority source")
    if auth.get("rank")!=AUTHORITY_ORDER[auth["source_type"]]: raise Unauthorized("Authority rank mismatch")
    if ctx.get("repository")!=REPOSITORY: raise RepositoryMismatch(f"Execution repository must be {REPOSITORY}")
    if ctx.get("branch")!=BRANCH: raise BranchMismatch(f"Execution branch must be {BRANCH}")
    if not valid_head(ctx.get("head")): raise InvalidInput("HEAD must be a 40-character hexadecimal commit")
    if ctx.get("expected_head") is not None and ctx["head"]!=ctx["expected_head"]: raise InvalidInput("HEAD does not match expected_head")
    scope=ctx.get("scope",{})
    if entry.id in set(scope.get("out_of_scope_skill_ids",[])) or entry.id not in scope.get("skill_ids",[]) or action not in scope.get("allowed_actions",[]): raise ScopeViolation(f"{entry.id}/{action} is outside authorized scope")
    sh=sha256_hex({"skill_id":entry.id,"action":action,"scope":scope})
    return AuthorizationToken(stable_id("AUT",{"execution_id":execution_id,"skill_id":entry.id,"scope_hash":sh}),execution_id,entry.id,action,REPOSITORY,BRANCH,ctx["head"],sh)

def evidence_bind(execution_id:str,skill_id:str,head:str,trace:list[str],input_envelope:dict[str,Any],output:dict[str,Any],result_id:str,status:str="VERIFIED")->dict[str,Any]:
    payload={"execution_id":execution_id,"skill_id":skill_id,"head":head,"trace":trace,"input":input_envelope,"output":output,"result_id":result_id}
    return {"id":stable_id("EVD",payload),"type":"EVIDENCE","execution_id":execution_id,"skill_id":skill_id,"result_id":result_id,"handler_id":"EVIDENCE-HANDLER-NEXY-001","source_head":head,"content_hash":sha256_hex(payload),"trace":trace,"status":status}

def execute_with_token(token:AuthorizationToken,fn:Callable[[dict[str,Any]],dict[str,Any]],envelope:dict[str,Any])->dict[str,Any]:
    if token.execution_id!=envelope.get("execution_id") or token.skill_id!=envelope.get("skill_id"): raise Unauthorized("Authorization token does not match execution envelope")
    return fn(envelope)

def base(envelope:dict[str,Any],objective:str)->dict[str,Any]:
    return {"status":"SUCCESS","objective":objective,"scope":envelope["context"]["scope"],"inputs":envelope["context"],"actions":[],"changed_files":[],"unchanged_files":[],"validation":{"status":"PASS"},"evidence":[],"errors":[],"unknowns":[],"remaining":[],"next_action":"NONE"}

def execute_gov_001(e:dict[str,Any])->dict[str,Any]:
    sources=e.get("data",{}).get("sources")
    if not isinstance(sources,list) or not sources: raise InvalidInput("GOV-001 requires non-empty sources")
    candidates=[s for s in sources if isinstance(s,dict) and s.get("status","VERIFIED")!="UNKNOWN" and s.get("source_type") in AUTHORITY_ORDER]
    if not candidates: return {**base(e,"Identify which Source has authority over a decision."),"status":"BLOCKED","authority_result":"UNKNOWN","source":None,"confidence":0.0,"conflicts":[],"decision":"BLOCKED","unknowns":["No verified authority source"],"next_action":"ACQUIRE_AUTHORITY_SOURCE"}
    if any(not isinstance(s.get("rank"),int) for s in candidates): raise InvalidInput("GOV-001 source rank is required")
    mr=max(s["rank"] for s in candidates); top=[s for s in candidates if s["rank"]==mr]
    if len({s["source_id"] for s in top})>1: raise AuthorityConflict("Multiple sources share the highest authority rank")
    out=base(e,"Identify which Source has authority over a decision."); out.update({"authority_result":"AUTHORITATIVE","source":top[0]["source_id"],"confidence":1.0,"conflicts":[],"decision":"CONTINUE","actions":["CLASSIFY_AUTHORITY"]}); return out

def execute_gov_002(e:dict[str,Any])->dict[str,Any]:
    req=e.get("data",{}).get("request")
    if not isinstance(req,dict): raise InvalidInput("GOV-002 requires request")
    scope=e["context"]["scope"]
    if e["skill_id"] in set(scope.get("out_of_scope_skill_ids",[])) or req.get("target") not in scope.get("allowed_targets",[req.get("target")]): raise ScopeViolation("Requested work is outside authorized scope")
    out=base(e,"Prevent work outside authorized scope."); out.update({"scope_result":"IN_SCOPE","decision":"CONTINUE","actions":["CHECK_SCOPE"]}); return out

def execute_ctx_001(e:dict[str,Any])->dict[str,Any]:
    c=e["context"]; out=base(e,"Load required current context.")
    missing=[k for k in UNIVERSAL_REQUIRED if not c.get(k)]
    if missing: out.update({"status":"UNKNOWN","context_result":"INCOMPLETE","unknowns":missing,"next_action":"ACQUIRE_MISSING_CONTEXT"}); return out
    out.update({"context_result":"CURRENT_CONTEXT_LOADED","actions":["LOAD_CURRENT_STATE"]}); return out

def execute_ctx_003(e:dict[str,Any])->dict[str,Any]:
    files=e.get("data",{}).get("files")
    if not isinstance(files,list) or not files: raise InvalidInput("CTX-003 requires files")
    inspected=[]
    for f in files:
        if not isinstance(f,dict) or not f.get("path") or not f.get("type") or not f.get("content_hash"): raise InvalidInput("CTX-003 file entries require path, type and content_hash")
        if "content" in f:
            if not isinstance(f["content"],str): raise InvalidInput("CTX-003 content must be text")
            expected=str(f["content_hash"]).split(":",1)[-1]
            if sha256_hex(f["content"].encode("utf-8"))!=expected: raise IntegrityFailure(f"Content hash mismatch for {f['path']}")
        inspected.append({"id":stable_id("FILE",{"path":f["path"],"content_hash":f["content_hash"]}),"path":f["path"],"type":f["type"],"content_hash":f["content_hash"],"dependencies":f.get("dependencies",[]),"callers":f.get("callers",[]),"callees":f.get("callees",[]),"contracts":f.get("contracts",[]),"tests":f.get("tests",[])})
    out=base(e,"Inspect actual source before deciding."); out.update({"inspected_files":inspected,"actions":["INSPECT_SOURCE"]}); return out

def execute_req_001(e:dict[str,Any])->dict[str,Any]:
    req=e.get("data",{}).get("requirement")
    if not isinstance(req,dict): raise InvalidInput("REQ-001 requires requirement object")
    need=["objective","in_scope","out_scope","input","output","constraint","acceptance","validation"]
    missing=[k for k in need if k not in req]
    out=base(e,"Translate a command into an explicit requirement contract.")
    if missing: out.update({"status":"UNKNOWN","requirement_result":"INCOMPLETE","unknowns":missing,"next_action":"ACQUIRE_AUTHORITATIVE_DETAIL"}); return out
    out.update({"requirement_result":"COMPLETE","requirement":req,"actions":["TRANSLATE_COMMAND"]}); return out

def execute_arc_001(e:dict[str,Any])->dict[str,Any]:
    a=e.get("data",{}).get("architecture")
    if not isinstance(a,dict): raise InvalidInput("ARC-001 requires architecture facts")
    missing=[k for k in ("layers","authority_flow","boundaries") if k not in a]
    out=base(e,"Understand actual NEXY architecture before changes.")
    if missing: out.update({"status":"UNKNOWN","architecture_result":"INCOMPLETE","unknowns":missing,"next_action":"INSPECT_MISSING_ARCHITECTURE"}); return out
    out.update({"architecture_result":"INSPECTED","architecture":a,"actions":["INSPECT_ARCHITECTURE"]}); return out

def execute_arc_004(e:dict[str,Any])->dict[str,Any]:
    i=e.get("data",{}).get("impact")
    if not isinstance(i,dict): raise InvalidInput("ARC-004 requires impact facts")
    need=["affected_modules","affected_contracts","affected_state","affected_tests","affected_security","affected_release"]
    missing=[k for k in need if k not in i]
    out=base(e,"Determine what an architectural change affects.")
    if missing: out.update({"status":"BLOCKED","unknowns":missing,"next_action":"INSPECT_CRITICAL_IMPACT"}); return out
    out.update({"AFFECTED_MODULES":i["affected_modules"],"AFFECTED_CONTRACTS":i["affected_contracts"],"AFFECTED_STATE":i["affected_state"],"AFFECTED_TESTS":i["affected_tests"],"AFFECTED_SECURITY":i["affected_security"],"AFFECTED_RELEASE":i["affected_release"],"actions":["ANALYZE_ARCHITECTURE_IMPACT"]}); return out

class SkillRuntime:
    def __init__(self,registry_path:str|Path):
        self.registry_path=Path(registry_path); self.registry=load_registry(self.registry_path)

    def run(self,skill_id:str,envelope:dict[str,Any])->dict[str,Any]:
        trace=[]; execution_id=envelope.get("execution_id","UNKNOWN-EXECUTION"); head=envelope.get("context",{}).get("head","UNKNOWN")
        try:
            trace.append("LOAD"); entry=resolve_entry(self.registry,skill_id); envelope={**envelope,"skill_id":skill_id}
            trace.append("RESOLVE"); fn=load_skill(entry); validate_input_contract(envelope)
            trace.append("AUTHORIZE"); token=authorize(entry,envelope)
            trace.append("EXECUTE"); out=execute_with_token(token,fn,envelope)
            trace.append("VALIDATE"); validate_output_contract(out); validate_trace(trace+["EVIDENCE","RESULT"])
            status=out.get("status","SUCCESS")
            if status not in {"SUCCESS","UNKNOWN","BLOCKED","FAILURE","FREEZE"}: raise ValidationFailure(f"Unsupported skill status: {status}",True)
            result_id=stable_id("RES",{"execution_id":execution_id,"skill_id":skill_id,"head":head,"output":out})
            trace.append("EVIDENCE"); ev=evidence_bind(execution_id,skill_id,head,trace+["RESULT"],envelope,out,result_id,"VERIFIED"); out={**out,"evidence":[ev]}
            trace.append("RESULT"); validate_trace(trace)
            return self._success(skill_id,execution_id,head,status,out,trace,result_id,ev)
        except RuntimeFault as fault:
            return self._failure(skill_id,execution_id,head,"FREEZE" if fault.critical else "FAILURE",fault,trace)
        except Exception as exc:
            return self._failure(skill_id,execution_id,head,"FREEZE",RuntimeFault(str(exc),"UNEXPECTED_RUNTIME_ERROR",True),trace)

    def _success(self,sid,eid,head,status,out,trace,rid,ev):
        return {"id":rid,"type":"RESULT","status":status,"skill_id":sid,"execution_id":eid,"source_head":head,"runtime_root":RUNTIME_ROOT,"runtime_version":RUNTIME_VERSION,"repository":REPOSITORY,"branch":BRANCH,"chain":trace,"skill_output":out,"evidence_id":ev["id"],"checkpoint":{"id":stable_id("CHK",eid),"expected":1,"processed":1,"verified":1 if status=="SUCCESS" else 0,"failed":0,"skipped":0,"blocked":1 if status in {"BLOCKED","FREEZE"} else 0,"remaining":0,"current_item":sid,"resume_point":"NONE" if status=="SUCCESS" else "REVALIDATE","last_verified_source":out.get("inputs",{}).get("source_of_truth",[]),"last_verified_head":head}}

    def _failure(self,sid,eid,head,status,fault,trace):
        err_id=stable_id("ERR",{"execution_id":eid,"skill_id":sid,"head":head,"code":fault.code,"message":str(fault)}); rid=stable_id("RES",{"execution_id":eid,"skill_id":sid,"status":status,"error":err_id})
        failure={"id":err_id,"code":fault.code,"message":str(fault)}
        ev=evidence_bind(eid,sid,head,trace,{"execution_id":eid,"skill_id":sid},{"status":status,"failure":failure},rid,"VERIFIED")
        return {"id":rid,"type":"RESULT","status":status,"skill_id":sid,"execution_id":eid,"source_head":head,"runtime_root":RUNTIME_ROOT,"runtime_version":RUNTIME_VERSION,"repository":REPOSITORY,"branch":BRANCH,"chain":trace,"failure":failure,"evidence_id":ev["id"],"evidence":ev,"checkpoint":{"id":stable_id("CHK",eid),"expected":1,"processed":1 if trace else 0,"verified":0,"failed":1 if status=="FAILURE" else 0,"skipped":0,"blocked":1 if status=="FREEZE" else 0,"remaining":0,"current_item":sid,"resume_point":"RETRY_AFTER_REVALIDATION" if status=="FREEZE" else "FIX_FAILURE","last_verified_source":[],"last_verified_head":head}}

    @staticmethod
    def freeze(reason:str,execution_id:str,skill_id:str,head:str)->dict[str,Any]:
        fault=IntegrityFailure(reason); err_id=stable_id("ERR",{"execution_id":execution_id,"skill_id":skill_id,"head":head,"code":fault.code,"message":str(fault)}); rid=stable_id("RES",{"execution_id":execution_id,"skill_id":skill_id,"status":"FREEZE","error":err_id})
        ev=evidence_bind(execution_id,skill_id,head,["FREEZE"],{"execution_id":execution_id,"skill_id":skill_id},{"status":"FREEZE","failure":{"id":err_id,"code":fault.code,"message":str(fault)}},rid,"VERIFIED")
        return {"id":rid,"type":"RESULT","status":"FREEZE","skill_id":skill_id,"execution_id":execution_id,"source_head":head,"runtime_root":RUNTIME_ROOT,"runtime_version":RUNTIME_VERSION,"repository":REPOSITORY,"branch":BRANCH,"chain":["FREEZE"],"failure":{"id":err_id,"code":fault.code,"message":str(fault)},"evidence_id":ev["id"],"evidence":ev,"checkpoint":{"id":stable_id("CHK",execution_id),"expected":1,"processed":1,"verified":0,"failed":0,"skipped":0,"blocked":1,"remaining":0,"current_item":skill_id,"resume_point":"REVALIDATE_SOURCE_AND_HEAD","last_verified_source":[],"last_verified_head":head}}
