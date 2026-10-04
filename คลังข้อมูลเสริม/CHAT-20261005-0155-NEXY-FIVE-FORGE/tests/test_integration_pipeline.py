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


class FiveSystemIntegrationTests(unittest.TestCase):
    def test_verified_learning_pipeline(self):
        burn = plan_burndown(
            [Assumption('scope-known',5,1,True), Assumption('runtime-current',5,.8,True)],
            [Probe('inspect-context',frozenset({'scope-known'}),1,.05), Probe('run-tests',frozenset({'runtime-current'}),2,.1)],
            max_cost=3,max_risk=.2,
        )
        self.assertEqual(burn.status,'PASS')

        route = choose_route(
            [ToolSpec('repo',frozenset({'inspect'}),1,.99,50,.5), ToolSpec('runner',frozenset({'execute'}),2,.98,100,1)],
            RouteRequest(frozenset({'inspect','execute'}),2,min_tool_reliability=.95,max_latency_ms=500,max_cost_units=5),
        )
        self.assertEqual(route.status,'PASS')

        context = optimize_context([
            ContextItem('law',10,1,10,1,mandatory=True),
            ContextItem('spec',20,.9,9,.9,dependencies=('law',)),
            ContextItem('history',50,.2,2,.2),
        ],35)
        self.assertEqual(context.status,'PASS')
        self.assertIn('spec',context.selected)

        episodes=[
            FailureEpisode('e1','runner','timeout',('late',),'queue-stall',('drain','retry'),('test_timeout',),'PASS',('ev1',)),
            FailureEpisode('e2','runner','timeout',('late',),'queue-stall',('drain','retry'),('test_timeout',),'PASS',('ev2',)),
        ]
        recipes=distill_recipes(episodes)
        self.assertEqual(len(recipes),1)

        records=[
            ExecutionRecord('r1','recover runner timeout',recipes[0].repair_steps,('failure',),('verified-recovery',),2,True,'sandbox'),
            ExecutionRecord('r2','recover runner timeout',recipes[0].repair_steps,('failure',),('verified-recovery',),2,True,'sandbox'),
            ExecutionRecord('r3','recover runner timeout',recipes[0].repair_steps,('failure',),('verified-recovery',),2,True,'sandbox'),
        ]
        skill=compile_skill(records)
        self.assertEqual(skill.status,'PASS')
        self.assertEqual(skill.steps,('drain','retry'))

if __name__ == '__main__':
    unittest.main()
