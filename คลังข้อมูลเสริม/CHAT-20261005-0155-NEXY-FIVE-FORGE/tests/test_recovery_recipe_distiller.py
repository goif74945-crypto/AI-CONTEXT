import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'systems' / 'recovery_recipe_distiller'))
from recovery_recipe_distiller import FailureEpisode, distill_recipes, match_recipe


def ep(i, outcome='PASS', steps=('restart-worker',), evidence=True):
    return FailureEpisode(str(i), 'worker', 'timeout', ('late',), 'stuck queue', steps, ('test_queue',), outcome, (f'ev{i}',) if evidence else ())


class RecoveryRecipeDistillerTests(unittest.TestCase):
    def test_requires_repeated_evidence(self):
        self.assertEqual(distill_recipes([ep(1)], min_successes=2), ())

    def test_distills_and_penalizes_failures(self):
        recipes = distill_recipes([ep(1), ep(2), ep(3, 'FAIL')])
        self.assertEqual(len(recipes), 1)
        r = recipes[0]
        self.assertEqual(r.success_count, 2)
        self.assertEqual(r.failure_count, 1)
        self.assertAlmostEqual(r.confidence, 0.5)
        self.assertEqual(match_recipe(recipes, 'worker', 'timeout'), r)

    def test_inconsistent_repairs_do_not_publish(self):
        recipes = distill_recipes([ep(1, steps=('a',)), ep(2, steps=('b',))])
        self.assertEqual(recipes, ())


if __name__ == '__main__':
    unittest.main()
