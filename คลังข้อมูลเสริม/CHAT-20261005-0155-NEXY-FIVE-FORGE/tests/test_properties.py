import random
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).parents[1] / 'systems'
for name in ('context_budget_optimizer','tool_evidence_router','recovery_recipe_distiller','skill_compiler','assumption_burndown_planner'):
    sys.path.insert(0, str(BASE / name))

from context_budget_optimizer import ContextItem, optimize_context
from tool_evidence_router import ToolSpec, RouteRequest, choose_route
from recovery_recipe_distiller import FailureEpisode, distill_recipes
from skill_compiler import ExecutionRecord, compile_skill
from assumption_burndown_planner import Assumption, Probe, plan_burndown


class PropertyTests(unittest.TestCase):
    def test_context_budget_never_exceeds_budget_on_pass(self):
        rng = random.Random(20261005)
        for _ in range(300):
            items = [ContextItem(f'i{i}', rng.randint(1, 20), rng.random(), rng.randint(0,10), rng.random()) for i in range(rng.randint(1,12))]
            budget = rng.randint(0, 80)
            r = optimize_context(items, budget)
            if r.status == 'PASS':
                self.assertLessEqual(r.used_tokens, budget)
                self.assertEqual(len(r.selected), len(set(r.selected)))

    def test_tool_route_pass_always_satisfies_request(self):
        rng = random.Random(20261006)
        universe = ('a','b','c')
        for _ in range(200):
            tools=[]
            for i in range(rng.randint(1,6)):
                caps=frozenset(x for x in universe if rng.random() < .5)
                tools.append(ToolSpec(f't{i}', caps, rng.randint(0,4), rng.uniform(.7,1), rng.randint(1,500), rng.uniform(.1,5)))
            req=RouteRequest(frozenset({'a'}), rng.randint(0,3), min_tool_reliability=.75, max_latency_ms=1000, max_cost_units=10, max_tools=3)
            r=choose_route(tools, req)
            if r.status == 'PASS':
                chosen=[t for t in tools if t.name in r.tools]
                caps=frozenset().union(*(t.capabilities for t in chosen))
                self.assertTrue(req.required_capabilities.issubset(caps))
                self.assertGreaterEqual(max(t.max_evidence_class for t in chosen), req.required_evidence_class)
                self.assertLessEqual(r.latency_ms, req.max_latency_ms)
                self.assertLessEqual(r.cost_units, req.max_cost_units)

    def test_distilled_recipe_meets_success_threshold(self):
        episodes=[]
        for i in range(10):
            episodes.append(FailureEpisode(str(i),'s','e',('x',),'r',('fix',),('test',),'PASS',(f'ev{i}',)))
        recipes=distill_recipes(episodes,min_successes=3)
        self.assertEqual(len(recipes),1)
        self.assertGreaterEqual(recipes[0].success_count,3)
        self.assertGreaterEqual(len(recipes[0].evidence_ids),3)

    def test_skill_pass_implies_consistent_steps_and_thresholds(self):
        records=[ExecutionRecord(f'r{i}','obj',('a','b'),('x',),('y',),2,True,'env') for i in range(5)]
        r=compile_skill(records,min_passes=3,min_pass_ratio=.8,min_evidence_class=2)
        self.assertEqual(r.status,'PASS')
        self.assertEqual(r.steps,('a','b'))
        self.assertEqual(r.pass_ratio,1.0)

    def test_burndown_pass_covers_all_blockers(self):
        assumptions=[Assumption('a',5,1,True),Assumption('b',4,.5,True),Assumption('c',1,.2,False)]
        probes=[Probe('p1',frozenset({'a'}),1,.1),Probe('p2',frozenset({'b'}),1,.1),Probe('p3',frozenset({'c'}),1,.1)]
        r=plan_burndown(assumptions,probes,max_cost=3,max_risk=.3)
        self.assertEqual(r.status,'PASS')
        self.assertTrue({'a','b'}.issubset(set(r.covered_assumptions)))

if __name__ == '__main__':
    unittest.main()
