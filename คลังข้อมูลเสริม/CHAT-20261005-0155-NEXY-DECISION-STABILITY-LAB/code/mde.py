from itertools import combinations
from core import canonicalize, evaluate

def extract(baseline,oracle,max_evaluations=20000,max_results=32):
    if max_evaluations<1 or max_results<1: raise ValueError("invalid budget")
    base=canonicalize(baseline); target=evaluate(oracle,base); evaluations=1; results=[]; truncated=False
    for size in range(len(base)+1):
        for subset in combinations(base,size):
            if evaluations>=max_evaluations: truncated=True; break
            result=evaluate(oracle,subset); evaluations+=1
            if result is target:
                results.append(tuple(x.evidence_id for x in subset))
                if len(results)>=max_results: truncated=True; break
        if results or truncated: break
    return {"baseline":target,"minimum_size":len(results[0]) if results else None,
            "subsets":tuple(results),"evaluations":evaluations,"truncated":truncated}
