from itertools import islice, permutations
from core import Kind, Decision, StabilityError, canonicalize, evaluate

def scan(baseline,context,oracle,permutation_limit=12):
    if permutation_limit<0: raise ValueError("permutation_limit")
    base=tuple(baseline); canonicalize(base); noise=canonicalize(context)
    if any(x.kind is not Kind.CONTEXT for x in noise): raise ValueError("context must be CONTEXT")
    before=evaluate(oracle,base); evaluations=1; violations=[]
    if noise:
        evaluations+=1
        if evaluate(oracle,(*base,*noise)) is not before: violations.append("declared_context_changed_decision")
    canonical_ids=tuple(x.evidence_id for x in canonicalize(base)); seen=0
    for perm in islice(permutations(base),permutation_limit+1):
        if tuple(x.evidence_id for x in perm)==canonical_ids: continue
        result=oracle(tuple(perm)); evaluations+=1; seen+=1
        if not isinstance(result,Decision): raise StabilityError("oracle returned non-Decision")
        if result is not before: violations.append("order_changed_decision")
        if seen>=permutation_limit: break
    return {"baseline":before,"evaluations":evaluations,"violations":tuple(violations),"passed":not violations}
