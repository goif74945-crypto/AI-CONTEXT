import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'systems' / 'tool_evidence_router'))
from tool_evidence_router import ToolSpec, RouteRequest, choose_route


class ToolEvidenceRouterTests(unittest.TestCase):
    def setUp(self):
        self.tools = [
            ToolSpec('repo', frozenset({'source'}), 1, .99, 100, 1),
            ToolSpec('test', frozenset({'execute'}), 2, .98, 200, 2),
            ToolSpec('combo', frozenset({'source', 'execute'}), 2, .90, 100, 1),
        ]

    def test_selects_reliable_route(self):
        req = RouteRequest(frozenset({'source', 'execute'}), 2, min_tool_reliability=.95, max_cost_units=10)
        result = choose_route(self.tools, req)
        self.assertEqual(result.status, 'PASS')
        self.assertEqual(result.tools, ('repo', 'test'))

    def test_evidence_gate(self):
        req = RouteRequest(frozenset({'source'}), 3)
        self.assertEqual(choose_route(self.tools, req).status, 'FREEZE')

    def test_budget_gate(self):
        req = RouteRequest(frozenset({'source', 'execute'}), 2, max_cost_units=1.5, min_tool_reliability=.95)
        self.assertEqual(choose_route(self.tools, req).status, 'FREEZE')


if __name__ == '__main__':
    unittest.main()
