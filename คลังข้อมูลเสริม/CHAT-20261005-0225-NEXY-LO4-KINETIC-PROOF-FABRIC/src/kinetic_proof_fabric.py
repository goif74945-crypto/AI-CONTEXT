from __future__ import annotations
from dataclasses import dataclass, replace
from hashlib import sha256
from typing import Iterable, Mapping

FRAC = 64
SCALE = 1 << FRAC
MIN_RAW = -(1 << 127)
MAX_RAW = (1 << 127) - 1

class QError(ValueError): pass
class QOverflow(QError): pass

def _raw(v:int)->int:
    if isinstance(v,bool) or not isinstance(v,int): raise TypeError("raw must be int")
    if not MIN_RAW <= v <= MAX_RAW: raise QOverflow("signed Q64.64 overflow")
    return v

def _tz(n:int,d:int)->int:
    if d == 0: raise ZeroDivisionError("Q64.64 division by zero")
    z = abs(n)//abs(d)
    return -z if (n<0) ^ (d<0) else z

@dataclass(frozen=True,order=True,slots=True)
class Q:
    raw:int
    def __post_init__(self): _raw(self.raw)
    @classmethod
    def zero(cls): return cls(0)
    @classmethod
    def one(cls): return cls(SCALE)
    @classmethod
    def i(cls,v:int):
        if isinstance(v,bool) or not isinstance(v,int): raise TypeError("int required")
        return cls(_raw(v<<FRAC))
    @classmethod
    def s(cls,text:str):
        if not isinstance(text,str): raise TypeError("str required")
        t=text.strip(); sign=-1 if t.startswith("-") else 1
        if t[:1] in "+-": t=t[1:]
        if not t or t.count(".")>1: raise QError("invalid decimal")
        w,d,f=t.partition("."); w=w or "0"
        if not w.isdigit() or (f and not f.isdigit()): raise QError("invalid decimal")
        frac=(int(f)*SCALE)//(10**len(f)) if d and f else 0
        return cls(_raw(sign*(int(w)*SCALE+frac)))
    def __add__(self,o): return Q(_raw(self.raw+q(o).raw))
    def __sub__(self,o): return Q(_raw(self.raw-q(o).raw))
    def __mul__(self,o): return Q(_raw(_tz(self.raw*q(o).raw,SCALE)))
    def __truediv__(self,o): return Q(_raw(_tz(self.raw*SCALE,q(o).raw)))
    def __neg__(self):
        if self.raw==MIN_RAW: raise QOverflow("negation overflow")
        return Q(-self.raw)
    def __abs__(self): return -self if self.raw<0 else self
    def text(self,digits:int=9):
        if not 0<=digits<=24: raise ValueError("digits")
        r=abs(self.raw); whole=r//SCALE; rem=r%SCALE
        frac=(rem*(10**digits))//SCALE
        return ("-" if self.raw<0 else "")+str(whole)+(f".{frac:0{digits}d}" if digits else "")

def q(v:Q|int|str)->Q:
    if isinstance(v,Q): return v
    if isinstance(v,bool): raise TypeError("bool forbidden")
    if isinstance(v,int): return Q.i(v)
    if isinstance(v,str): return Q.s(v)
    if isinstance(v,float): raise TypeError("float forbidden in deterministic path")
    raise TypeError(type(v).__name__)

Z=Q.zero(); O=Q.one()

@dataclass(frozen=True,slots=True)
class Sensor:
    source:str; value:Q; uncertainty:Q; trust:Q; age:Q; max_age:Q
    def check(self):
        if not self.source: raise QError("empty source")
        if self.uncertainty<Z or not Z<=self.trust<=O or self.age<Z or self.max_age<=Z: raise QError("invalid sensor bounds")
    @property
    def lo(self): return self.value-self.uncertainty
    @property
    def hi(self): return self.value+self.uncertainty

@dataclass(frozen=True,slots=True)
class Fusion:
    decision:str; value:Q|None; uncertainty:Q|None; support:Q; sources:tuple[str,...]; reasons:tuple[str,...]

class PSTL:
    def __init__(self,min_trust:Q,quorum:Q,min_sources:int=2):
        if not Z<=min_trust<=O or not Z<quorum<=O or min_sources<1: raise QError("invalid PSTL policy")
        self.min_trust=min_trust; self.quorum=quorum; self.min_sources=min_sources
    def fuse(self,samples:Iterable[Sensor])->Fusion:
        a=[]; reasons=[]; seen=set()
        for s in samples:
            s.check()
            if s.source in seen: return Fusion("FREEZE",None,None,Z,(),("DUPLICATE_SOURCE",))
            seen.add(s.source)
            if s.age>s.max_age: reasons.append("STALE:"+s.source); continue
            if s.trust<self.min_trust: reasons.append("LOW_TRUST:"+s.source); continue
            a.append(s)
        if len(a)<self.min_sources: return Fusion("FREEZE",None,None,Z,(),tuple(reasons+["INSUFFICIENT_SOURCES"]))
        total=Z
        for s in a: total=total+s.trust
        if total<=Z: return Fusion("FREEZE",None,None,Z,(),("ZERO_TRUST_MASS",))
        ev={}
        for s in a:
            ev.setdefault(s.lo.raw,[[],[]])[0].append(s)
            ev.setdefault(s.hi.raw,[[],[]])[1].append(s)
        active=Z; best=Z; point=None
        for r in sorted(ev):
            for s in ev[r][0]: active=active+s.trust
            if point is None or active>best: point=Q(r); best=active
            for s in ev[r][1]: active=active-s.trust
        assert point is not None
        members=[s for s in a if s.lo<=point<=s.hi]
        ratio=best/total
        if len(members)<self.min_sources or ratio<self.quorum:
            return Fusion("FREEZE",None,None,ratio,tuple(sorted(s.source for s in members)),tuple(reasons+["QUORUM_NOT_MET"]))
        lo=max((s.lo for s in members),key=lambda x:x.raw); hi=min((s.hi for s in members),key=lambda x:x.raw)
        if lo>hi: return Fusion("FREEZE",None,None,ratio,(),("IMPOSSIBLE_INTERSECTION",))
        mid=Q(_tz(lo.raw+hi.raw,2)); unc=Q(_tz(hi.raw-lo.raw,2))
        return Fusion("PASS",mid,unc,ratio,tuple(sorted(s.source for s in members)),tuple(reasons))

@dataclass(frozen=True,slots=True)
class Drift:
    decision:str; max_residual:Q; mean_residual:Q; reasons:tuple[str,...]

class WMDS:
    def __init__(self,soft:Q,hard:Q,weights:Mapping[str,Q]|None=None):
        if not Z<soft<hard: raise QError("require 0 < soft < hard")
        self.soft=soft; self.hard=hard; self.weights=dict(weights or {})
    def evaluate(self,pred:Mapping[str,Q],obs:Mapping[str,Q],tol:Mapping[str,Q])->Drift:
        axes=sorted(tol)
        if not axes: raise QError("no axes")
        weighted=Z; mass=Z; mx=Z
        for axis in axes:
            if axis not in pred or axis not in obs: return Drift("FREEZE",mx,Z,("MISSING_AXIS:"+axis,))
            if tol[axis]<=Z: return Drift("FREEZE",mx,Z,("INVALID_TOLERANCE:"+axis,))
            w=self.weights.get(axis,O)
            if w<Z: return Drift("FREEZE",mx,Z,("NEGATIVE_WEIGHT:"+axis,))
            r=abs(obs[axis]-pred[axis])/tol[axis]
            mx=max(mx,r,key=lambda x:x.raw); weighted=weighted+r*w; mass=mass+w
        if mass<=Z: return Drift("FREEZE",mx,Z,("ZERO_WEIGHT_MASS",))
        mean=weighted/mass
        if mx>=self.hard: return Drift("FREEZE",mx,mean,("HARD_DIVERGENCE",))
        if mx>=self.soft: return Drift("CAUTION",mx,mean,("SOFT_DIVERGENCE",))
        return Drift("PASS",mx,mean,())

@dataclass(frozen=True,slots=True)
class KState: position:Q; velocity:Q
@dataclass(frozen=True,slots=True)
class Actuation: target_velocity:Q; force:Q; duration:Q; obstacle_distance:Q
@dataclass(frozen=True,slots=True)
class Envelope:
    speed_limit:Q; force_limit:Q; acceleration_limit:Q; max_deceleration:Q; reaction_time:Q; boundary_min:Q; boundary_max:Q; margin:Q
    def check(self):
        if self.speed_limit<Z or self.force_limit<Z or self.acceleration_limit<Z or self.max_deceleration<=Z or self.reaction_time<Z or self.margin<Z or self.boundary_min>self.boundary_max: raise QError("invalid envelope")
@dataclass(frozen=True,slots=True)
class Proof:
    decision:str; stopping_distance:Q|None; projected_position:Q|None; reasons:tuple[str,...]

class AEPE:
    def prove(self,state:KState,req:Actuation,env:Envelope)->Proof:
        env.check(); reasons=[]
        if req.duration<=Z or req.obstacle_distance<Z: return Proof("FREEZE",None,None,("INVALID_REQUEST",))
        if abs(req.target_velocity)>env.speed_limit: reasons.append("SPEED_LIMIT")
        if abs(req.force)>env.force_limit: reasons.append("FORCE_LIMIT")
        if abs(req.target_velocity-state.velocity)>env.acceleration_limit*req.duration: reasons.append("ACCELERATION_LIMIT")
        projected=state.position+req.target_velocity*req.duration
        if projected<env.boundary_min or projected>env.boundary_max: reasons.append("BOUNDARY")
        v=max(abs(state.velocity),abs(req.target_velocity),key=lambda x:x.raw)
        stop=(v*v)/(Q.i(2)*env.max_deceleration)+v*env.reaction_time
        if req.obstacle_distance<stop+env.margin: reasons.append("INSUFFICIENT_STOPPING_CLEARANCE")
        return Proof("FREEZE" if reasons else "PASS",stop,projected,tuple(reasons))

@dataclass(frozen=True,slots=True)
class Hazard: thermal:Q; energy:Q; wear:Q
@dataclass(frozen=True,slots=True)
class HazardPolicy: decay:Hazard; cap:Hazard
@dataclass(frozen=True,slots=True)
class HazardResult: decision:str; committed:Hazard; proposed:Hazard|None; reasons:tuple[str,...]

class CHI:
    def step(self,current:Hazard,impulse:Hazard,policy:HazardPolicy)->HazardResult:
        vals=(current.thermal,current.energy,current.wear,impulse.thermal,impulse.energy,impulse.wear,policy.cap.thermal,policy.cap.energy,policy.cap.wear)
        if any(x<Z for x in vals) or any(not Z<=x<=O for x in (policy.decay.thermal,policy.decay.energy,policy.decay.wear)): raise QError("invalid hazard policy/state")
        try:
            p=Hazard(current.thermal*policy.decay.thermal+impulse.thermal,current.energy*policy.decay.energy+impulse.energy,current.wear*policy.decay.wear+impulse.wear)
        except QOverflow: return HazardResult("FREEZE",current,None,("NUMERIC_OVERFLOW",))
        rs=[]
        if p.thermal>policy.cap.thermal: rs.append("THERMAL_CAP")
        if p.energy>policy.cap.energy: rs.append("ENERGY_CAP")
        if p.wear>policy.cap.wear: rs.append("WEAR_CAP")
        return HazardResult("FREEZE",current,p,tuple(rs)) if rs else HazardResult("PASS",p,p,())

@dataclass(frozen=True,slots=True)
class HState:
    epoch:int; last_sequence:int; reflex_latched:bool; state_hash:str
    def check(self):
        if self.epoch<0 or self.last_sequence<0 or len(self.state_hash)!=64: raise ValueError("invalid handoff state")
        int(self.state_hash,16)
@dataclass(frozen=True,slots=True)
class Command:
    source:str; kind:str; epoch:int; sequence:int; issued_at:Q; lease_until:Q; state_hash:str
    def digest(self): return sha256(f"{self.source}|{self.kind}|{self.epoch}|{self.sequence}|{self.issued_at.raw}|{self.lease_until.raw}|{self.state_hash}".encode()).hexdigest()
@dataclass(frozen=True,slots=True)
class HResult: decision:str; state:HState; digest:str; reasons:tuple[str,...]

class RHPV:
    def evaluate(self,state:HState,cmd:Command,now:Q)->HResult:
        state.check(); d=cmd.digest()
        if cmd.source not in {"SAFE","REFLEX"}: return HResult("FREEZE",state,d,("UNKNOWN_SOURCE",))
        if cmd.issued_at<Z or cmd.lease_until<cmd.issued_at: return HResult("FREEZE",state,d,("INVALID_LEASE",))
        if cmd.issued_at>now: return HResult("FREEZE",state,d,("COMMAND_FROM_FUTURE",))
        if now>cmd.lease_until: return HResult("FREEZE",state,d,("LEASE_EXPIRED",))
        if cmd.sequence<=state.last_sequence: return HResult("FREEZE",state,d,("REPLAY_OR_REORDER",))
        if cmd.source=="REFLEX":
            if cmd.kind!="STOP": return HResult("FREEZE",state,d,("REFLEX_NON_STOP_FORBIDDEN",))
            if cmd.epoch<state.epoch: return HResult("FREEZE",state,d,("STALE_REFLEX_EPOCH",))
            return HResult("PASS",replace(state,epoch=cmd.epoch,last_sequence=cmd.sequence,reflex_latched=True),d,("REFLEX_STOP_LATCHED",))
        if state.reflex_latched: return HResult("FREEZE",state,d,("REFLEX_LATCH_ACTIVE",))
        if cmd.epoch!=state.epoch: return HResult("FREEZE",state,d,("EPOCH_MISMATCH",))
        if cmd.state_hash!=state.state_hash: return HResult("FREEZE",state,d,("STATE_BINDING_MISMATCH",))
        return HResult("PASS",replace(state,last_sequence=cmd.sequence),d,())
    def reset(self,state:HState,new_epoch:int,new_state_hash:str)->HState:
        state.check()
        if new_epoch!=state.epoch+1: raise ValueError("reset must advance epoch exactly one")
        n=HState(new_epoch,state.last_sequence,False,new_state_hash); n.check(); return n

def state_hash(position:Q,velocity:Q)->str:
    return sha256(f"p={position.raw}|v={velocity.raw}".encode()).hexdigest()

@dataclass(frozen=True,slots=True)
class PipelineResult:
    decision:str; stages:tuple[tuple[str,str],...]; hazard:Hazard; handoff:HState; reasons:tuple[str,...]

class KineticProofFabric:
    def __init__(self,pstl:PSTL,wmds:WMDS): self.pstl=pstl; self.wmds=wmds; self.aepe=AEPE(); self.chi=CHI(); self.rhpv=RHPV()
    def evaluate(self,*,position_samples:list[Sensor],velocity_samples:list[Sensor],predicted_position:Q,predicted_velocity:Q,position_tolerance:Q,velocity_tolerance:Q,request:Actuation,envelope:Envelope,current_hazard:Hazard,impulse:Hazard,hazard_policy:HazardPolicy,handoff:HState,epoch:int,sequence:int,now:Q,lease_until:Q)->PipelineResult:
        stages=[]
        p=self.pstl.fuse(position_samples); v=self.pstl.fuse(velocity_samples); stages += [("PSTL_POSITION",p.decision),("PSTL_VELOCITY",v.decision)]
        if p.decision!="PASS" or v.decision!="PASS" or p.value is None or v.value is None: return PipelineResult("FREEZE",tuple(stages),current_hazard,handoff,p.reasons+v.reasons)
        d=self.wmds.evaluate({"position":predicted_position,"velocity":predicted_velocity},{"position":p.value,"velocity":v.value},{"position":position_tolerance,"velocity":velocity_tolerance}); stages.append(("WMDS",d.decision))
        if d.decision=="FREEZE": return PipelineResult("FREEZE",tuple(stages),current_hazard,handoff,d.reasons)
        a=self.aepe.prove(KState(p.value,v.value),request,envelope); stages.append(("AEPE",a.decision))
        if a.decision!="PASS": return PipelineResult("FREEZE",tuple(stages),current_hazard,handoff,a.reasons)
        h=self.chi.step(current_hazard,impulse,hazard_policy); stages.append(("CHI",h.decision))
        if h.decision!="PASS": return PipelineResult("FREEZE",tuple(stages),current_hazard,handoff,h.reasons)
        sh=state_hash(p.value,v.value)
        if handoff.state_hash!=sh: return PipelineResult("FREEZE",tuple(stages+[("RHPV","FREEZE")]),current_hazard,handoff,("HANDOFF_STATE_STALE",))
        hr=self.rhpv.evaluate(handoff,Command("SAFE","ACTUATE",epoch,sequence,now,lease_until,sh),now); stages.append(("RHPV",hr.decision))
        if hr.decision!="PASS": return PipelineResult("FREEZE",tuple(stages),current_hazard,handoff,hr.reasons)
        return PipelineResult("PASS",tuple(stages),h.committed,hr.state,d.reasons)
