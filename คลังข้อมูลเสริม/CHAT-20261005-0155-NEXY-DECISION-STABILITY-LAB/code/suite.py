from core import Decision, canonicalize, evaluate, fingerprint
import mono, iris, edge, mde
from damp import Guard, Observation

def run(oracle,*,baseline,monotonic_candidates,irrelevant_context,universe,temporal_evidence,promotion_dwell=2):
    base=tuple(baseline)
    a=mono.verify(base,monotonic_candidates,oracle)
    b=iris.scan(base,irrelevant_context,oracle)
    c=edge.map_boundary(base,universe,oracle)
    d=mde.extract(base,oracle)
    guard=Guard(initial=Decision.FREEZE,promotion_dwell=promotion_dwell)
    temporal=[]
    for seq,evidence in enumerate(temporal_evidence):
        canonical=canonicalize(evidence)
        temporal.append(guard.observe(Observation(seq,evaluate(oracle,canonical),fingerprint(canonical))))
    return {"mono":a,"iris":b,"edge":c,"mde":d,"temporal":tuple(temporal),"passed":a["passed"] and b["passed"]}
