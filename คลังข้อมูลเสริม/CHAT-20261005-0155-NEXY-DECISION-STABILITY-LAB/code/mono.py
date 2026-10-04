from itertools import combinations
from core import Kind, canonicalize, evaluate

def verify(baseline,candidates,oracle,max_group_size=2):
    if max_group_size<1: raise ValueError("max_group_size")
    base=canonicalize(baseline); pool=canonicalize(candidates); before=evaluate(oracle,base)
    evaluations=1; violations=[]
    for kind in (Kind.SUPPORT,Kind.BLOCK):
        same=tuple(x for x in pool if x.kind is kind)
        for size in range(1,min(max_group_size,len(same))+1):
            for group in combinations(same,size):
                after=evaluate(oracle,(*base,*group)); evaluations+=1
                bad=(kind is Kind.SUPPORT and after.rank<before.rank) or (kind is Kind.BLOCK and after.rank>before.rank)
                if bad:
                    violations.append({"ids":tuple(x.evidence_id for x in group),"kind":kind,"before":before,"after":after})
    return {"baseline":before,"evaluations":evaluations,"violations":tuple(violations),"passed":not violations}
