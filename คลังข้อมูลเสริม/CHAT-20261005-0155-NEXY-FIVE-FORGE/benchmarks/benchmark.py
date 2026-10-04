import json, sys, time
from pathlib import Path
BASE = Path(__file__).parents[1] / 'systems'
for name in ('context_budget_optimizer','tool_evidence_router','assumption_burndown_planner'):
    sys.path.insert(0, str(BASE / name))
from context_budget_optimizer import ContextItem, optimize_context
from tool_evidence_router import ToolSpec, RouteRequest, choose_route
from assumption_burndown_planner import Assumption, Probe, plan_burndown

N=2000

def bench(fn):
    t=time.perf_counter()
    for _ in range(N): fn()
    elapsed=time.perf_counter()-t
    return {'iterations':N,'seconds':round(elapsed,6),'ops_per_second':round(N/elapsed,2)}

items=[ContextItem(f'i{i}',5+i%5,.7,7,.8) for i in range(12)]
tools=[ToolSpec(f't{i}',frozenset({'a','b'} if i%2 else {'a'}),2,.98,50,1) for i in range(6)]
req=RouteRequest(frozenset({'a','b'}),2,min_tool_reliability=.9,max_latency_ms=1000,max_cost_units=10)
ass=[Assumption(f'a{i}',5 if i<2 else 2,.8,i<2) for i in range(6)]
probes=[Probe(f'p{i}',frozenset({f'a{i}'}),1,.05) for i in range(6)]

result={
 'context_budget_optimizer': bench(lambda: optimize_context(items,40)),
 'tool_evidence_router': bench(lambda: choose_route(tools,req)),
 'assumption_burndown_planner': bench(lambda: plan_burndown(ass,probes,max_cost=6,max_risk=.5)),
 'note':'Microbenchmark only; not production or NEXY runtime evidence.'
}
print(json.dumps(result,indent=2,sort_keys=True))
