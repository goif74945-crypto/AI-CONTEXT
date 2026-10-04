from itertools import combinations
from core import StabilityError, canonicalize, evaluate

def map_boundary(baseline,universe,oracle,max_distance=3,max_evaluations=10000,max_results=32):
    if not 1<=max_distance<=8 or max_evaluations<1 or max_results<1: raise ValueError("invalid budget")
    base=canonicalize(baseline); world=canonicalize(universe)
    b={x.evidence_id:x for x in base}; w={x.evidence_id:x for x in world}
    for key,item in b.items():
        if key in w and w[key].canonical()!=item.canonical(): raise StabilityError("universe conflict")
    additions=tuple(w[k] for k in sorted(w.keys()-b.keys()))
    ops=tuple([("remove",x) for x in base]+[("add",x) for x in additions])
    before=evaluate(oracle,base); evaluations=1; flips=[]; truncated=False
    for distance in range(1,min(max_distance,len(ops))+1):
        for chosen in combinations(ops,distance):
            if evaluations>=max_evaluations: truncated=True; break
            current=dict(b); removed=[]; added=[]; valid=True
            for op,item in chosen:
                if op=="remove":
                    if item.evidence_id not in current: valid=False; break
                    current.pop(item.evidence_id); removed.append(item.evidence_id)
                else:
                    if item.evidence_id in current: valid=False; break
                    current[item.evidence_id]=item; added.append(item.evidence_id)
            if not valid: continue
            after=evaluate(oracle,current.values()); evaluations+=1
            if after is not before:
                flips.append((tuple(sorted(removed)),tuple(sorted(added)),before,after))
                if len(flips)>=max_results: truncated=True; break
        if flips or truncated: break
    flips.sort(key=lambda x:(len(x[0])+len(x[1]),x[0],x[1],x[3].value))
    return {"baseline":before,"minimum_distance":len(flips[0][0])+len(flips[0][1]) if flips else None,
            "flips":tuple(flips),"evaluations":evaluations,"truncated":truncated}
