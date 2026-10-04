from __future__ import annotations
import json
import random
import time
from lo4_frontier.minimal_cut_failure_geometry.engine import minimal_failure_cut_sets
from lo4_frontier.liveness_deadlock_sentinel.engine import analyze_liveness
from lo4_frontier.dependency_dominator_analyzer.engine import compute_dominators
from lo4_frontier.symmetry_state_space_reducer.engine import canonical_partition_key
from lo4_frontier.lo4_mutation_tournament.engine import run_tournament


def timed(fn):
    start=time.perf_counter(); result=fn(); return time.perf_counter()-start, result

rng=random.Random(20261005)
report={}
paths=[set(rng.sample([f'n{i}' for i in range(12)], 4)) for _ in range(12)]
report['minimal_cut_12_nodes_12_paths_s'], cuts = timed(lambda:minimal_failure_cut_sets(paths,max_nodes=20))
report['minimal_cut_result_count']=len(cuts)
items=[{'id':f'n{i}','state':'WAITING','waits_for':[f'n{(i+1)%1000}']} for i in range(1000)]
report['liveness_1000_cycle_s'], live = timed(lambda:analyze_liveness(items))
report['liveness_status']=live['status']
graph={f'n{i}':[f'n{i+1}'] if i<1499 else [] for i in range(1500)}
report['dominator_chain_1500_s'], dom = timed(lambda:compute_dominators(graph,'n0'))
report['dominator_target_size']=len(dom['n1499'])
entities={f'e{i}':{'class':f'worker-{i%4}','state':{'q':i%7,'mode':i%3}} for i in range(5000)}
report['symmetry_5000_entities_s'], key = timed(lambda:canonical_partition_key(entities))
report['symmetry_key_prefix']=key[:16]
candidates=[]
for i in range(5000):
    candidates.append({'id':f'c{i:05d}','metrics':{'safety':.95,'utility':.5+(i%5)*.1,'proof':.9,'reversibility':.9,'novelty':.5+(i%4)*.1},'invariant_failures':[]})
report['tournament_5000_candidates_s'], tournament = timed(lambda:run_tournament(candidates))
report['tournament_winner']=tournament['winner_id']
report['tournament_promotion_permitted']=tournament['promotion_permitted']
print(json.dumps(report,sort_keys=True,indent=2))
