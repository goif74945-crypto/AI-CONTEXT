from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable, Any

@dataclass(frozen=True)
class Action:
    action_id:str
    idempotency_key:str
    reversible:bool
    payload:Any=None
    compensation:Any=None
    approval_receipt:str|None=None


def execute_plan(actions:Iterable[Action], executor:Callable[[Action],bool], compensator:Callable[[Action],bool])->dict:
    actions=list(actions)
    if len({a.action_id for a in actions})!=len(actions): raise ValueError("duplicate action_id")
    if len({a.idempotency_key for a in actions})!=len(actions): raise ValueError("duplicate idempotency_key")
    for a in actions:
        if not a.action_id or not a.idempotency_key: raise ValueError("action_id and idempotency_key required")
        if a.reversible and a.compensation is None:
            return {"status":"FREEZE","phase":"PREPARE","reason":"missing_compensation","action_id":a.action_id}
        if not a.reversible and not a.approval_receipt:
            return {"status":"FREEZE","phase":"PREPARE","reason":"irreversible_without_approval","action_id":a.action_id}

    committed=[]
    for a in actions:
        if executor(a):
            committed.append(a)
            continue
        compensated=[]; residue=[]
        for prev in reversed(committed):
            if prev.reversible and compensator(prev): compensated.append(prev.action_id)
            else: residue.append(prev.action_id)
        return {
            "status":"FREEZE" if residue else "ROLLBACK_COMPLETE",
            "phase":"COMMIT",
            "failed_action":a.action_id,
            "compensated":compensated,
            "residual_effects":residue,
        }
    return {"status":"PASS","phase":"COMMITTED","committed":[a.action_id for a in committed]}
