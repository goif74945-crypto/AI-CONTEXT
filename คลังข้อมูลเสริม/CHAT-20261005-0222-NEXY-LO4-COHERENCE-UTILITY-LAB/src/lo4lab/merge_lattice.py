from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .canonical import canonical_json, fingerprint


class MergeError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class Claim:
    claim_id: str
    subject: str
    predicate: str
    scope: str
    value: Any
    authority_rank: int
    evidence_digest: str

    def __post_init__(self) -> None:
        for field_name in ("claim_id", "subject", "predicate", "scope", "evidence_digest"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise MergeError(f"{field_name} must be non-empty")
        if not isinstance(self.authority_rank, int) or self.authority_rank < 0:
            raise MergeError("authority_rank must be non-negative int")

    @property
    def semantic_key(self) -> tuple[str, str, str]:
        return (self.subject, self.predicate, self.scope)

    @property
    def identity_fingerprint(self) -> str:
        return fingerprint({"claim_id":self.claim_id,"subject":self.subject,"predicate":self.predicate,"scope":self.scope,"value":self.value,"authority_rank":self.authority_rank,"evidence_digest":self.evidence_digest})


@dataclass(frozen=True, slots=True)
class Retraction:
    retraction_id: str
    claim_id: str
    reason: str
    def __post_init__(self) -> None:
        if not self.retraction_id.strip() or not self.claim_id.strip() or not self.reason.strip():
            raise MergeError("retraction fields must be non-empty")


@dataclass(frozen=True, slots=True)
class Replica:
    claims: tuple[Claim,...]=()
    retractions: tuple[Retraction,...]=()

@dataclass(frozen=True, slots=True)
class ResolvedKey:
    key: tuple[str,str,str]
    status: str
    values: tuple[Any,...]
    claim_ids: tuple[str,...]
    authority_rank: int|None

@dataclass(frozen=True, slots=True)
class MergeResult:
    status:str
    claims:tuple[Claim,...]
    retractions:tuple[Retraction,...]
    resolved:tuple[ResolvedKey,...]
    reason_codes:tuple[str,...]
    state_fingerprint:str


def merge_replicas(replicas:Iterable[Replica])->MergeResult:
    claim_by_id:dict[str,Claim]={}
    retraction_by_id:dict[str,Retraction]={}
    for replica in replicas:
        for claim in replica.claims:
            existing=claim_by_id.get(claim.claim_id)
            if existing is not None and existing.identity_fingerprint!=claim.identity_fingerprint:
                raise MergeError(f"claim identity collision: {claim.claim_id}")
            claim_by_id[claim.claim_id]=claim
        for retraction in replica.retractions:
            existing=retraction_by_id.get(retraction.retraction_id)
            if existing is not None and existing!=retraction:
                raise MergeError(f"retraction identity collision: {retraction.retraction_id}")
            retraction_by_id[retraction.retraction_id]=retraction
    claims=tuple(sorted(claim_by_id.values(),key=lambda c:c.claim_id))
    retractions=tuple(sorted(retraction_by_id.values(),key=lambda r:r.retraction_id))
    tombstoned={r.claim_id for r in retractions}
    unknown_targets=sorted(tombstoned-set(claim_by_id))
    if unknown_targets:
        raise MergeError(f"retraction references unknown claim ids: {unknown_targets}")
    active=[c for c in claims if c.claim_id not in tombstoned]
    grouped:dict[tuple[str,str,str],list[Claim]]={}
    for claim in active:
        grouped.setdefault(claim.semantic_key,[]).append(claim)
    resolved:list[ResolvedKey]=[]
    conflicts=0
    for key in sorted(grouped):
        group=grouped[key]
        top_rank=max(c.authority_rank for c in group)
        top=[c for c in group if c.authority_rank==top_rank]
        by_value:dict[str,list[Claim]]={}; values:dict[str,Any]={}
        for claim in top:
            fp=fingerprint(claim.value); by_value.setdefault(fp,[]).append(claim); values[fp]=claim.value
        fps=sorted(by_value); status="PASS" if len(fps)==1 else "CONFLICT"
        if status=="CONFLICT": conflicts+=1
        resolved.append(ResolvedKey(key,status,tuple(values[fp] for fp in fps),tuple(sorted(c.claim_id for fp in fps for c in by_value[fp])),top_rank))
    overall="CONFLICT" if conflicts else "PASS"
    reasons=("UNRESOLVED_CONCURRENT_CONFLICT",) if conflicts else ("CONVERGED",)
    payload={"claims":[{"claim_id":c.claim_id,"subject":c.subject,"predicate":c.predicate,"scope":c.scope,"value":c.value,"authority_rank":c.authority_rank,"evidence_digest":c.evidence_digest} for c in claims],"retractions":[{"retraction_id":r.retraction_id,"claim_id":r.claim_id,"reason":r.reason} for r in retractions],"resolved":[{"key":list(r.key),"status":r.status,"values":list(r.values),"claim_ids":list(r.claim_ids),"authority_rank":r.authority_rank} for r in resolved],"status":overall,"reason_codes":list(reasons)}
    canonical_json(payload)
    return MergeResult(overall,claims,retractions,tuple(resolved),reasons,fingerprint(payload))
