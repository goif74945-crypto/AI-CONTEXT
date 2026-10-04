import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'systems' / 'context_budget_optimizer'))
from context_budget_optimizer import ContextItem, optimize_context


class ContextBudgetOptimizerTests(unittest.TestCase):
    def test_dependency_closure_and_budget(self):
        items = [
            ContextItem('law', 20, 0.8, 10, 0.9, mandatory=True),
            ContextItem('spec', 30, 0.9, 9, 0.8, dependencies=('law',)),
            ContextItem('note', 50, 0.2, 2, 0.2),
        ]
        result = optimize_context(items, 55)
        self.assertEqual(result.status, 'PASS')
        self.assertEqual(result.selected, ('law', 'spec'))
        self.assertLessEqual(result.used_tokens, 55)

    def test_mandatory_overflow_freezes(self):
        items = [ContextItem('law', 100, 1.0, 10, 1.0, mandatory=True)]
        result = optimize_context(items, 10)
        self.assertEqual(result.status, 'FREEZE')

    def test_unknown_dependency_freezes(self):
        result = optimize_context([ContextItem('x', 1, 1, 1, 1, dependencies=('missing',))], 10)
        self.assertEqual(result.status, 'FREEZE')

    def test_deterministic(self):
        items = [
            ContextItem('b', 10, .5, 5, .5),
            ContextItem('a', 10, .5, 5, .5),
        ]
        r1 = optimize_context(items, 10)
        r2 = optimize_context(reversed(items), 10)
        self.assertEqual(r1.selected, r2.selected)
        self.assertEqual(r1.selected, ('a',))


if __name__ == '__main__':
    unittest.main()
