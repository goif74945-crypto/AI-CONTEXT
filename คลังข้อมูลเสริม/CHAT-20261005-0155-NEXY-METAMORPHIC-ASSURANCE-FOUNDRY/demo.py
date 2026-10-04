import json
from nmaf import MetamorphicRelation, TestCandidate, minimize_counterexample, outputs_equal, reorder_mapping_insertion, run_relation, schedule_tests


def executor(d):
    payload=d.get("payload")
    if not isinstance(payload,dict): return {"status":"FREEZE","reason":"INVALID_PAYLOAD"}
    return {"status":"OK","keys":sorted(payload)}

r=MetamorphicRelation("MR-DEMO-ORDER","mapping insertion order is non-semantic for this fixture contract",reorder_mapping_insertion,outputs_equal)
relation=run_relation(r,{"payload":{"b":2,"a":1}},executor)
shrunk=minimize_counterexample({"noise":[1,2,3],"trigger":"FREEZE","irrelevant":True},lambda x:isinstance(x,dict) and x.get("trigger")=="FREEZE")
schedule=schedule_tests([TestCandidate("release-law",1.0,frozenset({"release"}),2,mandatory=True),TestCandidate("metadata-order",.4,frozenset({"canonicalization"}),1,novelty=.5)],3)
print(json.dumps({"relation_passed":relation.passed,"minimized":shrunk.minimized,"schedule":schedule.selected_ids,"freeze_required":schedule.freeze_required},ensure_ascii=False,sort_keys=True))
