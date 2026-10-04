from __future__ import annotations
from dataclasses import dataclass, field
from typing import FrozenSet, Iterable

UNTRUSTED_EXTERNAL="UNTRUSTED_EXTERNAL"; MODEL_GENERATED="MODEL_GENERATED"; SECRET="SECRET"
VERIFIED_EVIDENCE="VERIFIED_EVIDENCE"; AUTHORITY_SOURCE="AUTHORITY_SOURCE"

@dataclass(frozen=True)
class Node:
    node_id:str
    own_taints:FrozenSet[str]=field(default_factory=frozenset)
    parent_ids:tuple[str,...]=()
    verification_evidence:tuple[str,...]=()

class Graph:
    def __init__(self): self.nodes={}
    def add(self,node:Node):
        if not node.node_id or node.node_id in self.nodes: raise ValueError("node_id must be unique and non-empty")
        missing=[p for p in node.parent_ids if p not in self.nodes]
        if missing: raise ValueError(f"missing parents: {missing}")
        self.nodes[node.node_id]=node
    def effective_taints(self,node_id:str)->FrozenSet[str]:
        seen=set()
        def walk(nid):
            if nid in seen: return set()
            seen.add(nid); n=self.nodes[nid]
            out=set(n.own_taints)
            for p in n.parent_ids: out |= walk(p)
            return out
        return frozenset(walk(node_id))
    def decide(self,node_id:str,sink:str)->dict:
        n=self.nodes[node_id]; t=self.effective_taints(node_id)
        if sink=="EXTERNAL_EGRESS" and SECRET in t:
            return {"status":"FREEZE","reason":"secret_egress_blocked","taints":sorted(t)}
        if sink=="AUTHORITY_INPUT":
            risky=bool({UNTRUSTED_EXTERNAL,MODEL_GENERATED}&set(t))
            verified=bool(n.verification_evidence) and VERIFIED_EVIDENCE in n.own_taints
            if risky and not verified:
                return {"status":"FREEZE","reason":"untrusted_authority_promotion","taints":sorted(t)}
        return {"status":"PASS","reason":"policy_satisfied","taints":sorted(t)}
