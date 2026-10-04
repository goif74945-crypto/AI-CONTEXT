import random
import unittest

from frontier_assurance_lab import EffectSpec, FreezeError, TelemetryEventSpec
from obsure_runtime_assurance import (
    EffectRunExpectation,
    ObsureRuntimeAssurance,
    RuntimeEvent,
    RuntimeWitnessCertifier,
)

BASE = ("trace_id", "action_id", "effect_id", "timestamp")
HIGH = BASE + ("authority_ref", "evidence_ref")
CRITICAL = HIGH + ("state_digest",)


def schemas(effect_id, fields=BASE, reversible=False):
    phases = ["INTENT", "START", "SUCCESS", "FAILURE"]
    if reversible:
        phases += ["COMPENSATION_START", "COMPENSATION_RESULT"]
    return [
        TelemetryEventSpec(f"{effect_id}-{phase.lower()}", effect_id, phase, fields)
        for phase in phases
    ]


def runtime_events(effect_id, phases, fields=BASE, trace="trace-1", action="action-1"):
    values = {
        "trace_id": trace,
        "action_id": action,
        "effect_id": effect_id,
        "timestamp": "logical-time",
        "authority_ref": "authority-1",
        "evidence_ref": "evidence-1",
        "state_digest": "digest-1",
    }
    return [
        RuntimeEvent(
            f"{effect_id}-{phase.lower()}",
            effect_id,
            index,
            {field: values[field] for field in fields},
        )
        for index, phase in enumerate(phases)
    ]


class RuntimeWitnessPositiveTests(unittest.TestCase):
    def setUp(self):
        self.certifier = RuntimeWitnessCertifier()

    def test_success_witness_certified(self):
        result = self.certifier.certify(
            [EffectSpec("write", "LOW", False)],
            schemas("write"),
            [EffectRunExpectation("write", "SUCCESS")],
            runtime_events("write", ["INTENT", "START", "SUCCESS"]),
        )
        self.assertEqual(result["status"], "CERTIFIED")

    def test_failure_compensation_witness_certified(self):
        result = self.certifier.certify(
            [EffectSpec("delete", "HIGH", True)],
            schemas("delete", HIGH, True),
            [EffectRunExpectation("delete", "FAILURE", True)],
            runtime_events(
                "delete",
                [
                    "INTENT",
                    "START",
                    "FAILURE",
                    "COMPENSATION_START",
                    "COMPENSATION_RESULT",
                ],
                HIGH,
            ),
        )
        self.assertEqual(result["status"], "CERTIFIED")


class RuntimeWitnessNegativeTests(unittest.TestCase):
    def setUp(self):
        self.effect = [EffectSpec("write", "LOW", False)]
        self.schema = schemas("write")
        self.expectation = [EffectRunExpectation("write", "SUCCESS")]
        self.certifier = RuntimeWitnessCertifier()

    def certify(self, events):
        return self.certifier.certify(
            self.effect, self.schema, self.expectation, events
        )

    def test_missing_start_freezes(self):
        result = self.certify(runtime_events("write", ["INTENT", "SUCCESS"]))
        self.assertIn("PHASE_CARDINALITY", {i["code"] for i in result["issues"]})

    def test_wrong_terminal_freezes(self):
        result = self.certify(runtime_events("write", ["INTENT", "START", "FAILURE"]))
        codes = {i["code"] for i in result["issues"]}
        self.assertIn("TERMINAL_CONTRADICTION", codes)

    def test_correlation_drift_freezes(self):
        events = runtime_events("write", ["INTENT", "START", "SUCCESS"])
        drift = RuntimeEvent(
            events[1].name,
            events[1].effect_id,
            events[1].sequence,
            {**events[1].fields, "trace_id": "trace-2"},
        )
        result = self.certify([events[0], drift, events[2]])
        self.assertIn("CORRELATION_DRIFT", {i["code"] for i in result["issues"]})

    def test_missing_actual_value_freezes(self):
        events = runtime_events("write", ["INTENT", "START", "SUCCESS"])
        invalid = RuntimeEvent(
            events[0].name,
            events[0].effect_id,
            events[0].sequence,
            {**events[0].fields, "trace_id": ""},
        )
        result = self.certify([invalid, *events[1:]])
        self.assertIn("MISSING_FIELD_VALUES", {i["code"] for i in result["issues"]})

    def test_out_of_order_lifecycle_freezes(self):
        events = runtime_events("write", ["START", "INTENT", "SUCCESS"])
        result = self.certify(events)
        self.assertIn(
            "LIFECYCLE_ORDER_VIOLATION", {i["code"] for i in result["issues"]}
        )

    def test_duplicate_sequence_freezes(self):
        events = runtime_events("write", ["INTENT", "START", "SUCCESS"])
        duplicate = RuntimeEvent(
            events[1].name, events[1].effect_id, events[0].sequence, events[1].fields
        )
        result = self.certify([events[0], duplicate, events[2]])
        self.assertIn("DUPLICATE_SEQUENCE", {i["code"] for i in result["issues"]})

    def test_unexpected_compensation_freezes(self):
        schema = schemas("write", BASE, True)
        events = runtime_events(
            "write", ["INTENT", "START", "SUCCESS", "COMPENSATION_START"], BASE
        )
        result = self.certifier.certify(
            [EffectSpec("write", "LOW", True)], schema, self.expectation, events
        )
        self.assertIn("UNEXPECTED_COMPENSATION", {i["code"] for i in result["issues"]})

    def test_invalid_compensation_expectation_rejected(self):
        with self.assertRaises(FreezeError):
            EffectRunExpectation("write", "SUCCESS", True)


class RuntimeWitnessAdversarialTests(unittest.TestCase):
    def test_input_permutations_have_identical_result(self):
        certifier = RuntimeWitnessCertifier()
        effects = [EffectSpec("write", "CRITICAL", False)]
        specs = schemas("write", CRITICAL)
        expected = [EffectRunExpectation("write", "SUCCESS")]
        events = runtime_events("write", ["INTENT", "START", "SUCCESS"], CRITICAL)
        baseline = certifier.certify(effects, specs, expected, events)
        rng = random.Random(74945)
        for _ in range(100):
            shuffled_specs = specs[:]
            shuffled_events = events[:]
            rng.shuffle(shuffled_specs)
            rng.shuffle(shuffled_events)
            self.assertEqual(
                certifier.certify(effects, shuffled_specs, expected, shuffled_events),
                baseline,
            )

    def test_unadmitted_event_freezes(self):
        result = RuntimeWitnessCertifier().certify(
            [EffectSpec("write", "LOW", False)],
            schemas("write"),
            [EffectRunExpectation("write", "SUCCESS")],
            [RuntimeEvent("forged", "write", 0, {})],
        )
        self.assertIn("UNADMITTED_EVENT", {i["code"] for i in result["issues"]})


class ObsureRuntimeIntegrationTests(unittest.TestCase):
    def test_critical_spec_and_runtime_certified(self):
        result = ObsureRuntimeAssurance().assess(
            [EffectSpec("deploy", "CRITICAL", False)],
            schemas("deploy", CRITICAL),
            [EffectRunExpectation("deploy", "SUCCESS")],
            runtime_events("deploy", ["INTENT", "START", "SUCCESS"], CRITICAL),
        )
        self.assertEqual(result["status"], "CERTIFIED")
        self.assertEqual(result["reason"], "RUNTIME_CERTIFIED")

    def test_insufficient_spec_blocks_runtime_certification(self):
        result = ObsureRuntimeAssurance().assess(
            [EffectSpec("deploy", "CRITICAL", False)],
            schemas("deploy", BASE),
            [EffectRunExpectation("deploy", "SUCCESS")],
            runtime_events("deploy", ["INTENT", "START", "SUCCESS"], BASE),
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "SPECIFICATION_INSUFFICIENT")
        self.assertIsNone(result["runtime"])


if __name__ == "__main__":
    unittest.main()
