import random
import unittest

from frontier_assurance_lab import FreezeError
from ghostedge_campaign_assurance import (
    CampaignExperiment,
    ControlledCampaignDetector,
    GhostedgeCampaignAssurance,
    PerturbationCampaignContract,
)


def contract(**overrides):
    values = {
        "expected_observations": {"vault": ("judge", "view")},
        "min_interventions_per_source": 2,
        "min_shams": 2,
        "min_lift_milli": 500,
    }
    values.update(overrides)
    return PerturbationCampaignContract(**values)


def experiment(eid, kind, failed=(), observed=("judge", "view"), source="vault"):
    return CampaignExperiment(
        eid,
        kind,
        None if kind == "SHAM" else source,
        observed,
        failed,
    )


class ControlledCampaignPositiveTests(unittest.TestCase):
    def setUp(self):
        self.detector = ControlledCampaignDetector(min_hits=2, min_ratio_milli=750)

    def test_controlled_excess_failure_detects_candidate(self):
        experiments = [
            experiment("i1", "INTERVENTION", ("judge",)),
            experiment("i2", "INTERVENTION", ("judge",)),
            experiment("s1", "SHAM"),
            experiment("s2", "SHAM"),
        ]
        result = self.detector.detect(contract(), experiments, {})
        self.assertEqual(result["status"], "CANDIDATES_FOUND")
        self.assertEqual(result["candidates"][0]["lift_milli"], 1000)

    def test_complete_clean_campaign_is_clean(self):
        experiments = [
            experiment("i1", "INTERVENTION"),
            experiment("i2", "INTERVENTION"),
            experiment("s1", "SHAM"),
            experiment("s2", "SHAM"),
        ]
        self.assertEqual(self.detector.detect(contract(), experiments, {})["status"], "CLEAN")

    def test_declared_dependency_is_not_candidate(self):
        experiments = [
            experiment("i1", "INTERVENTION", ("judge",)),
            experiment("i2", "INTERVENTION", ("judge",)),
            experiment("s1", "SHAM"),
            experiment("s2", "SHAM"),
        ]
        result = self.detector.detect(contract(), experiments, {"judge": ("vault",)})
        self.assertEqual(result["status"], "CLEAN")


class ControlledCampaignNegativeTests(unittest.TestCase):
    def setUp(self):
        self.detector = ControlledCampaignDetector()

    def test_empty_campaign_freezes(self):
        result = self.detector.detect(contract(), [], {})
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(
            {gap["code"] for gap in result["gaps"]},
            {"INSUFFICIENT_INTERVENTIONS", "INSUFFICIENT_SHAMS"},
        )

    def test_missing_shams_freezes(self):
        result = self.detector.detect(
            contract(),
            [experiment("i1", "INTERVENTION"), experiment("i2", "INTERVENTION")],
            {},
        )
        self.assertIn("INSUFFICIENT_SHAMS", {gap["code"] for gap in result["gaps"]})

    def test_intervention_coverage_omission_freezes(self):
        experiments = [
            experiment("i1", "INTERVENTION", observed=("judge",)),
            experiment("i2", "INTERVENTION"),
            experiment("s1", "SHAM"),
            experiment("s2", "SHAM"),
        ]
        result = self.detector.detect(contract(), experiments, {})
        self.assertIn(
            "INTERVENTION_OBSERVATION_COVERAGE_MISMATCH",
            {gap["code"] for gap in result["gaps"]},
        )

    def test_sham_coverage_omission_freezes(self):
        experiments = [
            experiment("i1", "INTERVENTION"),
            experiment("i2", "INTERVENTION"),
            experiment("s1", "SHAM", observed=("judge",)),
            experiment("s2", "SHAM"),
        ]
        result = self.detector.detect(contract(), experiments, {})
        self.assertIn(
            "SHAM_OBSERVATION_COVERAGE_MISMATCH",
            {gap["code"] for gap in result["gaps"]},
        )

    def test_unknown_source_freezes(self):
        experiments = [
            experiment("i1", "INTERVENTION", source="queue"),
            experiment("i2", "INTERVENTION"),
            experiment("s1", "SHAM"),
            experiment("s2", "SHAM"),
        ]
        result = self.detector.detect(contract(), experiments, {})
        self.assertIn("UNKNOWN_PERTURBATION_SOURCE", {gap["code"] for gap in result["gaps"]})

    def test_duplicate_experiment_id_rejected(self):
        with self.assertRaises(FreezeError):
            self.detector.detect(
                contract(),
                [experiment("x", "INTERVENTION"), experiment("x", "SHAM")],
                {},
            )

    def test_string_parent_collection_rejected(self):
        with self.assertRaises(FreezeError):
            self.detector.detect(contract(), [], {"judge": "vault"})

    def test_duplicate_observation_rejected(self):
        with self.assertRaises(FreezeError):
            experiment("i1", "INTERVENTION", observed=("judge", "judge"))

    def test_non_string_experiment_id_fails_closed(self):
        with self.assertRaises(FreezeError):
            CampaignExperiment(1, "SHAM", None, ("judge",), ())

    def test_string_observation_collection_fails_closed(self):
        with self.assertRaises(FreezeError):
            CampaignExperiment("s1", "SHAM", None, "judge", ())


class ControlledCampaignAdversarialTests(unittest.TestCase):
    def test_input_permutations_are_deterministic(self):
        detector = ControlledCampaignDetector()
        experiments = [
            experiment("i1", "INTERVENTION", ("judge",)),
            experiment("i2", "INTERVENTION", ("judge",)),
            experiment("s1", "SHAM"),
            experiment("s2", "SHAM"),
        ]
        baseline = detector.detect(contract(), experiments, {})
        rng = random.Random(74945)
        for _ in range(100):
            shuffled = experiments[:]
            rng.shuffle(shuffled)
            self.assertEqual(detector.detect(contract(), shuffled, {}), baseline)

    def test_sham_failures_remove_false_excess_signal(self):
        experiments = [
            experiment("i1", "INTERVENTION", ("judge",)),
            experiment("i2", "INTERVENTION", ("judge",)),
            experiment("s1", "SHAM", ("judge",)),
            experiment("s2", "SHAM", ("judge",)),
        ]
        result = ControlledCampaignDetector().detect(contract(), experiments, {})
        judge = next(row for row in result["diagnostics"] if row["child"] == "judge")
        self.assertEqual(result["status"], "CLEAN")
        self.assertEqual(judge["lift_milli"], 0)


class GhostedgeCampaignIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.assurance = GhostedgeCampaignAssurance()

    def test_controlled_candidate_is_preserved(self):
        experiments = [
            experiment("i1", "INTERVENTION", ("judge",)),
            experiment("i2", "INTERVENTION", ("judge",)),
            experiment("s1", "SHAM"),
            experiment("s2", "SHAM"),
        ]
        result = self.assurance.assess(contract(), experiments, {})
        self.assertEqual(result["status"], "CANDIDATES_FOUND")
        self.assertEqual(result["reason"], "CONTROLLED_CANDIDATES_FOUND")

    def test_uncontrolled_candidate_rejected_by_sham_freezes(self):
        experiments = [
            experiment("i1", "INTERVENTION", ("judge",)),
            experiment("i2", "INTERVENTION", ("judge",)),
            experiment("s1", "SHAM", ("judge",)),
            experiment("s2", "SHAM", ("judge",)),
        ]
        result = self.assurance.assess(contract(), experiments, {})
        self.assertEqual(result["original"]["status"], "CANDIDATES_FOUND")
        self.assertEqual(result["controlled"]["status"], "CLEAN")
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "UNCONTROLLED_SIGNAL_REJECTED_BY_SHAM_BASELINE")

    def test_empty_campaign_integration_freezes(self):
        result = self.assurance.assess(contract(), [], {})
        self.assertEqual(result["original"]["status"], "CLEAN")
        self.assertEqual(result["controlled"]["status"], "FREEZE")
        self.assertEqual(result["status"], "FREEZE")


if __name__ == "__main__":
    unittest.main()
