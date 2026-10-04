import math
import unittest

from nexy_product_evidence.model import Direction, MetricKind, MetricObservation, MetricSpec
from nexy_product_evidence.stats import inverse_normal_cdf, normal_cdf, observed_interval, sample_size_per_arm, z_for_two_sided_alpha


class StatsTests(unittest.TestCase):
    def test_inverse_normal_median(self):
        self.assertAlmostEqual(inverse_normal_cdf(0.5), 0.0, places=12)

    def test_inverse_normal_975(self):
        self.assertAlmostEqual(inverse_normal_cdf(0.975), 1.959963984, places=6)

    def test_normal_inverse_round_trip(self):
        for p in (0.001, 0.01, 0.1, 0.5, 0.9, 0.99, 0.999):
            self.assertAlmostEqual(normal_cdf(inverse_normal_cdf(p)), p, places=7)

    def test_invalid_inverse_probability(self):
        for p in (0.0, 1.0, -0.1, 1.1):
            with self.assertRaises(ValueError):
                inverse_normal_cdf(p)

    def test_z_alpha(self):
        self.assertAlmostEqual(z_for_two_sided_alpha(0.05), 1.959963984, places=6)

    def test_proportion_sample_size_deterministic(self):
        spec = MetricSpec("x", MetricKind.PROPORTION, Direction.HIGHER_IS_BETTER, 0.4, 0.05, 0.05, 0.8)
        a = sample_size_per_arm(spec)
        b = sample_size_per_arm(spec)
        self.assertEqual(a, b)
        self.assertGreater(a, 100)

    def test_lower_proportion_sample_size(self):
        spec = MetricSpec("x", MetricKind.PROPORTION, Direction.LOWER_IS_BETTER, 0.4, 0.05, 0.05, 0.8)
        self.assertGreater(sample_size_per_arm(spec), 100)

    def test_mean_sample_size(self):
        spec = MetricSpec("latency", MetricKind.MEAN, Direction.LOWER_IS_BETTER, 100.0, 10.0, 0.05, 0.8, planning_stddev=30.0)
        self.assertGreaterEqual(sample_size_per_arm(spec), 2)

    def test_mean_requires_stddev(self):
        spec = MetricSpec("latency", MetricKind.MEAN, Direction.LOWER_IS_BETTER, 100.0, 10.0, 0.05, 0.8)
        with self.assertRaises(ValueError):
            sample_size_per_arm(spec)

    def test_observed_proportion_interval_direction(self):
        spec = MetricSpec("x", MetricKind.PROPORTION, Direction.HIGHER_IS_BETTER, 0.4, 0.05, 0.05, 0.8)
        obs = MetricObservation("x", 0.4, 0.5, 1000, 1000)
        out = observed_interval(spec, obs)
        self.assertGreater(out.effect_in_desired_direction, 0)
        self.assertLess(out.lower, out.upper)
        self.assertLess(out.p_value_vs_zero, 0.05)

    def test_lower_is_better_reorients_interval(self):
        spec = MetricSpec("latency", MetricKind.MEAN, Direction.LOWER_IS_BETTER, 100, 10, 0.05, 0.8, 20)
        obs = MetricObservation("latency", 100, 80, 200, 200, 20, 20)
        out = observed_interval(spec, obs)
        self.assertGreater(out.effect_in_desired_direction, 0)
        self.assertGreater(out.lower, 0)


if __name__ == "__main__":
    unittest.main()
