from dataclasses import dataclass
from core import Decision, StabilityError

@dataclass(frozen=True,slots=True)
class Observation:
    sequence:int
    proposed:Decision
    evidence_fingerprint:str
    def __post_init__(self):
        if self.sequence<0 or not self.evidence_fingerprint: raise StabilityError("invalid observation")

class Guard:
    def __init__(self,initial=Decision.FREEZE,promotion_dwell=2,require_stable_fingerprint=True):
        if promotion_dwell<1: raise ValueError("promotion_dwell")
        self.public=initial; self.dwell=promotion_dwell; self.stable=require_stable_fingerprint
        self.last=None; self.pending=None; self.count=0; self.pending_fp=None
    def _clear(self):
        self.pending=None; self.count=0; self.pending_fp=None
    def observe(self,obs):
        if self.last is not None and obs.sequence<=self.last: raise StabilityError("sequence must strictly increase")
        self.last=obs.sequence; proposed=obs.proposed
        if proposed.rank<self.public.rank:
            self.public=proposed; self._clear()
            return {"public":self.public,"changed":True,"reason":"safety_regression_immediate","pending_count":0}
        if proposed is self.public:
            self._clear()
            return {"public":self.public,"changed":False,"reason":"stable_same_decision","pending_count":0}
        reset=self.pending is None or proposed is not self.pending or (self.stable and self.pending_fp is not None and obs.evidence_fingerprint!=self.pending_fp)
        if reset:
            self.pending=proposed; self.count=1; self.pending_fp=obs.evidence_fingerprint
        else:
            self.count+=1
        if self.count>=self.dwell:
            self.public=proposed; self._clear()
            return {"public":self.public,"changed":True,"reason":"promotion_dwell_satisfied","pending_count":0}
        return {"public":self.public,"changed":False,"reason":"promotion_pending","pending_count":self.count}
