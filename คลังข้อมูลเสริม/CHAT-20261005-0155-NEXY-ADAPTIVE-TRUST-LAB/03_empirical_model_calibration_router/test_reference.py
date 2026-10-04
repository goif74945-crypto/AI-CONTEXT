import unittest
from reference import Observation, RoutePolicy, route


class TestEMCR(unittest.TestCase):
    def obs(self, model, success, confidence, latency=100, cost=10):
        return Observation(model, "reasoning", success, confidence, latency, cost)

    def test_routes_to_better_calibrated_reliable_model(self):
        rows = [
            self.obs("a", True, .95), self.obs("a", True, .9), self.obs("a", True, .9),
            self.obs("b", True, .99), self.obs("b", False, .99), self.obs("b", True, .99),
        ]
        d = route(rows, "reasoning")
        self.assertEqual(d.status, "ROUTE")
        self.assertEqual(d.model_id, "a")

    def test_insufficient_samples_probes(self):
        self.assertEqual(route([self.obs("a", True, .9)], "reasoning").status, "PROBE")

    def test_budget_filters_all_candidates(self):
        rows = [self.obs("a", True, .9, latency=9000) for _ in range(3)]
        self.assertEqual(route(rows, "reasoning", RoutePolicy(max_latency_ms=1000)).status, "FREEZE")

    def test_malformed_confidence_freezes(self):
        rows = [self.obs("a", True, 1.2) for _ in range(3)]
        self.assertEqual(route(rows, "reasoning").status, "FREEZE")

    def test_other_capability_does_not_pollute(self):
        rows = [Observation("x", "vision", True, .9, 10, 1) for _ in range(5)]
        self.assertEqual(route(rows, "reasoning").status, "PROBE")


if __name__ == "__main__":
    unittest.main()
