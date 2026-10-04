import unittest

from aep import AbsenceEvidencePlanner, Observation, SurfaceSpec


class AbsenceEvidencePlannerTests(unittest.TestCase):
    def setUp(self):
        self.surfaces = [
            SurfaceSpec("spec", max_age_seconds=100, expected_version="v2", scan_cost=5),
            SurfaceSpec("repo", max_age_seconds=50, expected_version="abc", scan_cost=2),
            SurfaceSpec("runtime", max_age_seconds=10, expected_version="run-9", scan_cost=8),
        ]

    def test_pass_requires_complete_fresh_version_bound_coverage(self):
        obs = [
            Observation("spec", "feature-x", 95, "v2"),
            Observation("repo", "feature-x", 95, "abc"),
            Observation("runtime", "feature-x", 95, "run-9"),
        ]
        result = AbsenceEvidencePlanner.evaluate("feature-x", self.surfaces, obs, now=100)
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.next_scan_plan, ())

    def test_missing_or_stale_surface_blocks_absence_claim_and_plans_cheapest_scan_first(self):
        obs = [Observation("spec", "feature-x", 95, "v2")]
        result = AbsenceEvidencePlanner.evaluate("feature-x", self.surfaces, obs, now=100)
        self.assertEqual(result.status, "NOT_VERIFIED")
        self.assertEqual(result.missing_surfaces, ("repo", "runtime"))
        self.assertEqual(result.next_scan_plan, ("repo", "runtime"))

    def test_hit_refutes_absence_even_when_other_surfaces_are_missing(self):
        obs = [Observation("repo", "feature-x", 95, "abc", hits=("src/feature_x.py",))]
        result = AbsenceEvidencePlanner.evaluate("feature-x", self.surfaces, obs, now=100)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.hit_surfaces, ("repo",))

    def test_version_mismatch_is_not_current_evidence(self):
        obs = [
            Observation("spec", "feature-x", 95, "v1"),
            Observation("repo", "feature-x", 95, "abc"),
            Observation("runtime", "feature-x", 95, "run-9"),
        ]
        result = AbsenceEvidencePlanner.evaluate("feature-x", self.surfaces, obs, now=100)
        self.assertEqual(result.status, "NOT_VERIFIED")
        self.assertEqual(result.version_mismatch_surfaces, ("spec",))


if __name__ == "__main__":
    unittest.main()
