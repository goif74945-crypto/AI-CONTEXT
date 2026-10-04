from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, ClassVar, Mapping

SHIFT = 64
ONE_RAW = 1 << SHIFT
I128_MIN = -(1 << 127)
I128_MAX = (1 << 127) - 1
HEX64 = frozenset("0123456789abcdef")
SYSTEM_IDS = tuple(f"S{i:02d}" for i in range(1, 21))

class NumericFault(ValueError):
    pass

def _i128(v: int) -> int:
    if isinstance(v, bool) or not isinstance(v, int):
        raise NumericFault("Q64_RAW_TYPE_INVALID")
    if not I128_MIN <= v <= I128_MAX:
        raise NumericFault("Q64_OVERFLOW")
    return v

def _div0(a: int, b: int) -> int:
    if b == 0:
        raise NumericFault("Q64_DIVIDE_BY_ZERO")
    q = abs(a) // abs(b)
    return -q if (a < 0) ^ (b < 0) else q

@dataclass(frozen=True)
class Q64:
    raw: int
    ZERO: ClassVar["Q64"]
    ONE: ClassVar["Q64"]
    def __post_init__(self): _i128(self.raw)
    @classmethod
    def from_raw(cls, raw: int): return cls(_i128(raw))
    @classmethod
    def from_int(cls, v: int):
        if isinstance(v, bool) or not isinstance(v, int): raise NumericFault("Q64_INTEGER_TYPE_INVALID")
        return cls.from_raw(_i128(v * ONE_RAW))
    @classmethod
    def from_ratio(cls, n: int, d: int):
        if any(isinstance(v, bool) or not isinstance(v, int) for v in (n, d)):
            raise NumericFault("Q64_RATIO_TYPE_INVALID")
        return cls.from_raw(_i128(_div0(_i128(n * ONE_RAW), d)))
    def add(self, o: "Q64"): return Q64.from_raw(_i128(self.raw + o.raw))
    def sub(self, o: "Q64"): return Q64.from_raw(_i128(self.raw - o.raw))
    def mul(self, o: "Q64"): return Q64.from_raw(_i128(_div0(self.raw * o.raw, ONE_RAW)))
    def div(self, o: "Q64"): return Q64.from_raw(_i128(_div0(self.raw * ONE_RAW, o.raw)))
    def serialize(self): return f"q64:{self.raw}"
Q64.ZERO = Q64.from_raw(0)
Q64.ONE = Q64.from_raw(ONE_RAW)

def _plain_int(v): return isinstance(v, int) and not isinstance(v, bool)
def _contains_float(v, seen=None):
    if isinstance(v, float): return True
    if v is None or isinstance(v, (bool, int, str, bytes)): return False
    seen = set() if seen is None else seen
    if id(v) in seen: return False
    seen.add(id(v))
    if isinstance(v, Mapping): return any(_contains_float(k, seen) or _contains_float(x, seen) for k, x in v.items())
    if isinstance(v, (list, tuple, set, frozenset)): return any(_contains_float(x, seen) for x in v)
    return False

def _canon(v):
    if v is None or isinstance(v, (bool, str)): return v
    if _plain_int(v): return v
    if isinstance(v, Q64): return v.serialize()
    if isinstance(v, float): raise TypeError("BINARY_FLOAT_FORBIDDEN")
    if isinstance(v, Mapping):
        if any(not isinstance(k, str) for k in v): raise TypeError("CANONICAL_KEY_MUST_BE_STRING")
        return {k: _canon(v[k]) for k in sorted(v, key=lambda s: tuple(map(ord, s)))}
    if isinstance(v, (list, tuple)): return [_canon(x) for x in v]
    raise TypeError("UNSUPPORTED_CANONICAL_TYPE")

def canonical_digest(v):
    b = json.dumps(_canon(v), ensure_ascii=False, separators=(",", ":")).encode()
    return sha256(b).hexdigest()

def _hash(v): return isinstance(v, str) and len(v) == 64 and all(c in HEX64 for c in v)
def _bool(v):
    if not isinstance(v, bool): raise ValueError("BOOLEAN_INVALID")
    return v
def _int(v, minimum=None):
    if not _plain_int(v) or (minimum is not None and v < minimum): raise ValueError("INTEGER_INVALID")
    return v
def _sl(v, *, unique=True, nonempty=False):
    if not isinstance(v, list) or (nonempty and not v) or any(not isinstance(x, str) or not x for x in v):
        raise ValueError("STRING_LIST_INVALID")
    if unique and len(v) != len(set(v)): raise ValueError("STRING_LIST_DUPLICATE")
    return list(v)
def _unit_raw(v):
    q = Q64.from_raw(_int(v))
    if not 0 <= q.raw <= ONE_RAW: raise NumericFault("Q64_UNIT_RANGE_INVALID")
    return q

@dataclass(frozen=True)
class Decision:
    system_id: str
    status: str
    reason: str
    metrics: Mapping[str, str] = field(default_factory=dict)
    evidence_root: str = ""
    selected_reason: str = ""
    def to_dict(self):
        return {"system_id": self.system_id, "status": self.status, "reason": self.reason,
                "metrics": dict(self.metrics), "evidence_root": self.evidence_root,
                "selected_reason": self.selected_reason}

def _d(sid, status, reason, metrics=None, selected_reason="", evidence=None):
    m = dict(metrics or {})
    body = {"system_id": sid, "status": status, "reason": reason, "metrics": m,
            "selected_reason": selected_reason, "evidence": evidence or {}}
    try: root = canonical_digest(body)
    except (TypeError, ValueError):
        root = canonical_digest({"system_id": sid, "status": status, "reason": reason,
                                 "metrics": m, "selected_reason": selected_reason})
    return Decision(sid, status, reason, m, root, selected_reason)
def _pass(sid, **kw): return _d(sid, "PASS", "PASS", **kw)
def _freeze(sid, reason, **kw): return _d(sid, "FREEZE", reason, **kw)

def _s01(p):
    destructive, reversible, proof = _bool(p["destructive"]), _bool(p["reversible"]), p["rollback_proof"]
    if not isinstance(proof, str): raise ValueError()
    if destructive and (not reversible or not _hash(proof)): return _freeze("S01", "IRREVERSIBLE_ACTION")
    return _pass("S01", evidence={"destructive": destructive, "reversible": reversible, "rollback_proof": proof})
def _s02(p):
    waits = p["wait_ticks"]
    if not isinstance(waits, Mapping) or len(waits) < 2 or any(not isinstance(k, str) or not k for k in waits): raise ValueError()
    vals = [_int(v, 0) for v in waits.values()]; threshold = _unit_raw(p["min_fairness_q64"])
    fairness = Q64.ONE if max(vals) == 0 else Q64.from_ratio(min(vals), max(vals)); m={"fairness_q64":fairness.serialize()}
    return _freeze("S02","QUEUE_FAIRNESS_LOW",metrics=m) if fairness.raw < threshold.raw else _pass("S02",metrics=m,evidence={"wait_ticks":dict(sorted(waits.items())),"threshold":threshold.raw})
def _s03(p):
    a,b=_sl(p["requested_features"]),_sl(p["excluded_features"]); overlap=sorted(set(a)&set(b))
    return _freeze("S03","NON_GOAL_CREEP",evidence={"overlap":overlap}) if overlap else _pass("S03",evidence={"requested":sorted(a),"excluded":sorted(b)})
def _s04(p):
    attempt=_int(p["attempt"],1); budget=_int(p.get("retry_budget",p.get("max_attempts")),1)
    if attempt>budget:return _freeze("S04","RETRY_BUDGET_EXCEEDED")
    unknown=_bool(p["prior_effect_unknown"]) if "prior_effect_unknown" in p else p.get("prior_effect")=="UNKNOWN"
    if unknown and not (_bool(p["side_effect_free"]) or _bool(p["idempotency_proven"])): return _freeze("S04","AMBIGUOUS_RETRY_HARM")
    return _pass("S04",evidence={"attempt":attempt,"budget":budget,"prior_unknown":unknown})
def _s05(p):
    items=p["preconditions"]
    if not isinstance(items,list) or not items:raise ValueError()
    seen=set()
    for x in items:
        if not isinstance(x,Mapping) or not isinstance(x.get("id"),str) or not x["id"] or x["id"] in seen:raise ValueError()
        seen.add(x["id"])
        if not _bool(x["disclosed"]):return _freeze("S05","PRECONDITION_HIDDEN")
        if not _bool(x["satisfied"]):return _freeze("S05","PRECONDITION_UNSATISFIED")
    return _pass("S05",evidence={"ids":sorted(seen)})
def _s06(p):
    c,w,e=_int(p["current_tick"],0),_int(p["warning_tick"],0),_int(p["expiry_tick"],0); warned=_bool(p["user_warned"])
    if w>e:raise ValueError()
    if c>=e:return _freeze("S06","SESSION_EXPIRED")
    if c>=w and not warned:return _freeze("S06","EXPIRY_NOT_DISCLOSED")
    return _pass("S06",evidence={"current":c,"warning":w,"expiry":e,"warned":warned})
def _s07(p):
    requested=_bool(p["revocation_requested"]); active=_sl(p["active_handles"]); revoked=_sl(p["revoked_handles"]); missing=sorted(set(active)-set(revoked))
    return _freeze("S07","REVOCATION_INCOMPLETE",evidence={"missing":missing}) if requested and missing else _pass("S07",evidence={"active":sorted(active),"revoked":sorted(revoked)})
def _s08(p):
    ok=[isinstance(p.get("code"),str) and bool(p.get("code")), isinstance(p.get("blocking_layer"),str) and bool(p.get("blocking_layer")), isinstance(p.get("recoverable"),bool), isinstance(p.get("remediation"),str) and bool(p.get("remediation"))]
    score=Q64.from_ratio(sum(ok),4); m={"actionability_q64":score.serialize()}
    return _pass("S08",metrics=m,evidence={"complete":True}) if all(ok) else _freeze("S08","ERROR_NOT_ACTIONABLE",metrics=m)
def _s09(p):
    statuses=_sl(p["component_statuses"],unique=False,nonempty=True); reported=p["reported_status"]
    if not isinstance(reported,str) or not reported:raise ValueError()
    allpass=all(x=="PASS" for x in statuses)
    if not allpass and reported in {"PASS","OK","SUCCESS"}:return _freeze("S09","PARTIAL_SUCCESS_MISREPORTED")
    if allpass and reported!="PASS":return _freeze("S09","SUCCESS_STATE_INCONSISTENT")
    return _pass("S09",evidence={"component_statuses":statuses,"reported_status":reported})
def _s10(p):
    a,b=p["internal_state"],p["visible_state"]
    if not isinstance(a,str) or not a or not isinstance(b,str) or not b:raise ValueError()
    return _freeze("S10","STATE_DISCLOSURE_MISMATCH") if a!=b else _pass("S10",evidence={"state":a})
def _s11(p):
    if not _bool(p["server_only"]):return _freeze("S11","SECRET_BOUNDARY_NOT_SERVER_ONLY")
    cfg=p["config"]
    if not isinstance(cfg,Mapping):raise ValueError()
    for k,v in cfg.items():
        if not isinstance(k,str) or not isinstance(v,str):raise ValueError()
        placeholder=v=="INJECT_AT_RUNTIME" or (v.startswith(") and v.endswith(") and len(v)>3)
        sensitive=any(t in k.upper() for t in ("SECRET","TOKEN","PASSWORD","API_KEY","PRIVATE_KEY")) or v.startswith(("sk-","ghp_","github_pat_","xoxb-","AKIA"))
        if sensitive and not placeholder:return _freeze("S11","SECRET_LITERAL_PRESENT",evidence={"key":k})
    return _pass("S11",evidence={"keys":sorted(cfg)})
def _s12(p):
    owned,exported=_sl(p["owned_ids"]),_sl(p["exported_ids"]); excluded=p["excluded"]
    if not isinstance(excluded,Mapping) or any(not isinstance(k,str) or not isinstance(v,str) or not v for k,v in excluded.items()):raise ValueError()
    missing=sorted(set(owned)-set(exported)-set(excluded)); foreign=sorted((set(exported)|set(excluded))-set(owned))
    return _freeze("S12","OWNERSHIP_EXPORT_INCOMPLETE",evidence={"missing":missing,"foreign":foreign}) if missing or foreign else _pass("S12",evidence={"owned":sorted(owned),"exported":sorted(exported),"excluded":dict(sorted(excluded.items()))})
def _s13(p):
    declared,verified=_sl(p["declared"],nonempty=True),_sl(p["verified"]); covered=len(set(declared)&set(verified)); q=Q64.from_ratio(covered,len(declared)); m={"claim_coverage_q64":q.serialize()}
    return _freeze("S13","UNVERIFIED_CAPABILITY_CLAIM",metrics=m) if covered!=len(declared) else _pass("S13",metrics=m,evidence={"declared":sorted(declared),"verified":sorted(verified)})
def _s14(p):
    if not _bool(p["duplicate"]):return _pass("S14",evidence={"duplicate":False})
    keys=("original_intent_hash","replay_intent_hash","original_result_hash","replay_result_hash")
    if any(not _hash(p[k]) for k in keys):raise ValueError()
    if p[keys[0]]!=p[keys[1]]:return _freeze("S14","IDEMPOTENCY_INTENT_CONFLICT")
    if p[keys[2]]!=p[keys[3]]:return _freeze("S14","IDEMPOTENCY_RESULT_CONFLICT")
    if p.get("user_feedback")!="REPLAYED":return _freeze("S14","REPLAY_FEEDBACK_MISSING")
    return _pass("S14",evidence={"intent_hash":p[keys[0]],"result_hash":p[keys[2]],"feedback":"REPLAYED"})
def _s15(p):
    if not _bool(p["limited"]):return _pass("S15",evidence={"limited":False})
    c,r,u=_int(p["current_tick"],0),_int(p["retry_after_ticks"],1),_int(p["unlock_tick"],0); disclosed=_bool(p.get("user_disclosed",p.get("recovery_disclosed")))
    if u!=c+r:return _freeze("S15","RATE_LIMIT_RECOVERY_INCONSISTENT")
    return _pass("S15",evidence={"current":c,"retry_after":r,"unlock":u}) if disclosed else _freeze("S15","RATE_LIMIT_RECOVERY_HIDDEN")
def _s16(p):
    events=p["events"]
    if not isinstance(events,list) or not events:raise ValueError()
    ids=None; normalized=[]
    for i,e in enumerate(events,1):
        if not isinstance(e,Mapping):raise ValueError()
        if _int(e["sequence"],1)!=i:return _freeze("S16","AUDIT_SEQUENCE_INVALID",evidence=normalized)
        cur=(e["request_id"],e["trace_id"],e["correlation_id"])
        if any(not isinstance(v,str) or not v for v in cur):raise ValueError()
        if ids is None:ids=cur
        elif cur!=ids:return _freeze("S16","AUDIT_CORRELATION_BROKEN",evidence=normalized)
        normalized.append({"sequence":i,"request_id":cur[0],"trace_id":cur[1],"correlation_id":cur[2],**({"event":e["event"]} if isinstance(e.get("event"),str) else {})})
    return _pass("S16",evidence=normalized)
def _s17(p):
    requested=_bool(p["cancel_requested"]); components=p["components"]
    if not isinstance(components,Mapping) or not components or any(not isinstance(k,str) or not k or not isinstance(v,str) or not v for k,v in components.items()):raise ValueError()
    if "side_effect_after_cancel" in p:effect=_bool(p["side_effect_after_cancel"])
    else:
        effects=p.get("side_effects_after_cancel")
        if not isinstance(effects,list):raise ValueError()
        effect=bool(effects)
    if requested and effect:return _freeze("S17","POST_CANCEL_SIDE_EFFECT")
    if requested and any(v not in {"CANCELLED","STOPPED"} for v in components.values()):return _freeze("S17","CANCELLATION_NOT_PROPAGATED")
    return _pass("S17",evidence={"components":dict(sorted(components.items())),"post_cancel_effect":effect})
def _s18(p):
    stale,expired=_bool(p["stale"]),_bool(p["expired"]); status=p["user_status"]; effect=_bool(p["side_effect_after_expiry"])
    if not isinstance(status,str):raise ValueError()
    if stale and effect:return _freeze("S18","POST_EXPIRY_SIDE_EFFECT")
    if stale and not expired:return _freeze("S18","STALE_JOB_NOT_EXPIRED")
    if stale and status not in {"EXPIRED","STALE"}:return _freeze("S18","STALE_JOB_UNDISCLOSED")
    return _pass("S18",evidence={"stale":stale,"expired":expired,"user_status":status})
def _s19(p):
    req,exp=_sl(p["required_evidence"],nonempty=True),_sl(p["explained_evidence"])
    if any(not _hash(x) for x in req+exp):raise ValueError()
    rs,es=set(req),set(exp); coverage=Q64.from_ratio(len(rs&es),len(rs)); m={"coverage_q64":coverage.serialize()}; invented=sorted(es-rs); missing=sorted(rs-es)
    if invented:return _freeze("S19","EVIDENCE_EXPLANATION_INVENTED",metrics=m,evidence={"invented":invented})
    if missing:return _freeze("S19","EVIDENCE_EXPLANATION_LOSS",metrics=m,evidence={"missing":missing})
    return _pass("S19",metrics=m,evidence={"evidence":sorted(rs)})
PRECEDENCE=("SECURITY_BREACH","AUTHORITY_VIOLATION","CANON_CONFLICT","EVIDENCE_MISSING","DEPENDENCY_FAILURE","TIMEOUT")
RANK={v:i for i,v in enumerate(PRECEDENCE)}
def _s20(p):
    reasons=_sl(p["reasons"],nonempty=True); unknown=sorted(set(reasons)-set(RANK))
    if unknown:return _freeze("S20","UNKNOWN_REASON",evidence={"unknown":unknown})
    ordered=sorted(set(reasons),key=lambda x:(RANK[x],tuple(map(ord,x))))
    return _pass("S20",selected_reason=ordered[0],evidence={"reasons":ordered})

HANDLERS={f"S{i:02d}":globals()[f"_s{i:02d}"] for i in range(1,21)}
def evaluate(system_id: str, payload: Any) -> Decision:
    if system_id not in HANDLERS:return _freeze(system_id if isinstance(system_id,str) else "UNKNOWN","UNKNOWN_SYSTEM")
    if _contains_float(payload):return _freeze(system_id,"BINARY_FLOAT_FORBIDDEN")
    if not isinstance(payload,Mapping):return _freeze(system_id,"SCHEMA_INVALID")
    try:
        canonical_digest(payload)
        return HANDLERS[system_id](payload)
    except NumericFault:return _freeze(system_id,"NUMERIC_INVALID")
    except (KeyError,TypeError,ValueError,OverflowError,RecursionError):return _freeze(system_id,"SCHEMA_INVALID")
