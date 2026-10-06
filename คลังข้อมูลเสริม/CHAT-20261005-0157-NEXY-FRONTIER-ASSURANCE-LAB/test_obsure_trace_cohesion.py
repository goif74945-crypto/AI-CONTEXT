import importlib
import random
import unittest

from frontier_assurance_lab import EffectSpec, FreezeError, TelemetryEventSpec
from obsure_runtime_assurance import (
    EffectRunExpectation,
    ObsureRuntimeAssurance,
    RuntimeEvent,
)


FIELDS = ("trace_id", "action_id", "effect_id", "timestamp")


def api(testcase):
    try:
        return importlib.import_module("obsure_trace_cohesion")
    except ModuleNotFoundError:
        testcase.fail("obsure_trace_cohesion implementation is missing")


def schemas(effect_ids=("write", "notify")):
    return [
        TelemetryEventSpec(f"{effect_id}-{phase.lower()}", effect_id, phase, FIELDS)
        for effect_id in effect_ids
        for phase in ("INTENT", "START", "SUCCESS", "FAILURE")
    ]


def events(
    *,
    trace="trace-1",
    action="action-1",
    write_sequences=(0, 1, 2),
    notify_sequences=(3, 4, 5),
):
    output = []
    for effect_id, sequence_values in (
        ("write", write_sequences),
        ("notify", notify_sequences),
    ):
        for sequence, phase in zip(sequence_values, ("INTENT", "START", "SUCCESS")):
            values = {
                "trace_id": trace,
                "action_id": action,
                "effect_id": effect_id,
                "timestamp": "logical-time",
            }
            output.append(
                RuntimeEvent(
                    f"{effect_id}-{phase.lower()}", effect_id, sequence, values
                )
            )
    return output


def effects():
    return [EffectSpec("write", "LOW", False), EffectSpec("notify", "LOW", False)]


def expectations():
    return [
        EffectRunExpectation("write", "SUCCESS"),
        EffectRunExpectation("notify", "SUCCESS"),
    ]


def contract(testcase, dependencies=None, **overrides):
    module = api(testcase)
    values = {
        "trace_id": "trace-1",
        "action_id": "action-1",
        "dependencies": dependencies
        if dependencies is not None
        else {"write": (), "notify": ("write",)},
    }
    values.update(overrides)
    return module.TraceCohesionContract(**values)


class TraceCohesionPositiveTests(unittest.TestCase):
    def test_two_effect_dependency_trace_is_certified(self):
        result = api(self).ObsureTraceCohesionAssurance().assess(
            contract(self), effects(), schemas(), expectations(), events()
        )
        self.assertEqual(result["status"], "CERTIFIED")
        self.assertEqual(result["reason"], "TRACE_COHESIVE")
        self.assertEqual(result["issues"], [])
        self.assertRegex(result["contract_hash"], r"^[0-9a-f]{64}$")
        self.assertRegex(result["witness_hash"], r"^[0-9a-f]{64}$")

    def test_independent_effects_may_interleave(self):
        result = api(self).ObsureTraceCohesionAssurance().assess(
            contract(self, {"write": (), "notify": ()}),
            effects(),
            schemas(),
            expectations(),
            events(write_sequences=(0, 2, 4), notify_sequences=(1, 3, 5)),
        )
        self.assertEqual(result["status"], "CERTIFIED")


class TraceCohesionNegativeTests(unittest.TestCase):
    def test_spliced_actions_pass_base_but_freeze_cohesion(self):
        spliced = events()
        for event in spliced[3:]:
            object.__setattr__(
                event,
                "fields",
                {**event.fields, "trace_id": "trace-2", "action_id": "action-2"},
            )
        base = ObsureRuntimeAssurance().assess(
            effects(), schemas(), expectations(), spliced
        )
        self.assertEqual(base["status"], "CERTIFIED")

        result = api(self).ObsureTraceCohesionAssurance().assess(
            contract(self), effects(), schemas(), expectations(), spliced
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(
            {issue["code"] for issue in result["issues"]},
            {"ACTION_ID_MISMATCH", "TRACE_ID_MISMATCH"},
        )

    def test_dependency_inversion_freezes(self):
        result = api(self).ObsureTraceCohesionAssurance().assess(
            contract(self),
            effects(),
            schemas(),
            expectations(),
            events(write_sequences=(3, 4, 5), notify_sequences=(0, 1, 2)),
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["issues"][0]["code"], "DEPENDENCY_ORDER_VIOLATION")

    def test_compensated_parent_must_finish_before_child_intent(self):
        effect_values = [
            EffectSpec("write", "LOW", True),
            EffectSpec("notify", "LOW", False),
        ]
        schema_values = schemas()
        schema_values += [
            TelemetryEventSpec(
                f"write-{phase.lower()}", "write", phase, FIELDS
            )
            for phase in ("COMPENSATION_START", "COMPENSATION_RESULT")
        ]
        expectation_values = [
            EffectRunExpectation("write", "FAILURE", True),
            EffectRunExpectation("notify", "SUCCESS"),
        ]

        def event(effect_id, phase, sequence):
            return RuntimeEvent(
                f"{effect_id}-{phase.lower()}",
                effect_id,
                sequence,
                {
                    "trace_id": "trace-1",
                    "action_id": "action-1",
                    "effect_id": effect_id,
                    "timestamp": "logical-time",
                },
            )

        event_values = [
            event("write", "INTENT", 0),
            event("write", "START", 1),
            event("write", "FAILURE", 2),
            event("notify", "INTENT", 3),
            event("write", "COMPENSATION_START", 4),
            event("write", "COMPENSATION_RESULT", 5),
            event("notify", "START", 6),
            event("notify", "SUCCESS", 7),
        ]
        result = api(self).ObsureTraceCohesionAssurance().assess(
            contract(self),
            effect_values,
            schema_values,
            expectation_values,
            event_values,
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["issues"][0]["code"], "DEPENDENCY_ORDER_VIOLATION")
        self.assertEqual(result["issues"][0]["parent_completion_phase"], "COMPENSATION_RESULT")

    def test_contract_must_cover_exact_effect_set(self):
        with self.assertRaises(FreezeError):
            api(self).ObsureTraceCohesionAssurance().assess(
                contract(self, {"write": ()}),
                effects(),
                schemas(),
                expectations(),
                events(),
            )

    def test_unknown_dependency_parent_rejected(self):
        with self.assertRaises(FreezeError):
            contract(self, {"write": (), "notify": ("missing",)})

    def test_dependency_cycle_rejected(self):
        with self.assertRaises(FreezeError):
            contract(self, {"write": ("notify",), "notify": ("write",)})

    def test_duplicate_dependency_parent_rejected(self):
        with self.assertRaises(FreezeError):
            contract(self, {"write": (), "notify": ("write", "write")})

    def test_event_generator_rejected_before_materialization(self):
        with self.assertRaises(FreezeError):
            api(self).ObsureTraceCohesionAssurance().assess(
                contract(self),
                effects(),
                schemas(),
                expectations(),
                (event for event in events()),
            )

    def test_foreign_event_rejected_before_sort(self):
        with self.assertRaises(FreezeError):
            api(self).ObsureTraceCohesionAssurance().assess(
                contract(self), effects(), schemas(), expectations(), [object()]
            )


class TraceCohesionAdversarialTests(unittest.TestCase):
    def test_contract_snapshots_mutable_dependency_input(self):
        dependencies = {"write": (), "notify": ("write",)}
        trace_contract = contract(self, dependencies)
        dependencies["notify"] = ("unknown",)

        result = api(self).ObsureTraceCohesionAssurance().assess(
            trace_contract, effects(), schemas(), expectations(), events()
        )

        self.assertEqual(result["status"], "CERTIFIED")
        self.assertEqual(trace_contract.dependencies["notify"], ("write",))

    def test_input_permutations_are_deterministic(self):
        assurance = api(self).ObsureTraceCohesionAssurance()
        baseline = assurance.assess(
            contract(self), effects(), schemas(), expectations(), events()
        )
        rng = random.Random(74945)
        for _ in range(50):
            shuffled = [effects(), schemas(), expectations(), events()]
            for values in shuffled:
                rng.shuffle(values)
            self.assertEqual(
                assurance.assess(contract(self), *shuffled), baseline
            )

    def test_duplicate_cross_effect_sequence_preserves_base_freeze(self):
        result = api(self).ObsureTraceCohesionAssurance().assess(
            contract(self, {"write": (), "notify": ()}),
            effects(),
            schemas(),
            expectations(),
            events(write_sequences=(0, 1, 2), notify_sequences=(0, 3, 4)),
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "BASE_RUNTIME_INVALID")

    def test_contract_identity_changes_contract_hash(self):
        assurance = api(self).ObsureTraceCohesionAssurance()
        first = assurance.assess(
            contract(self), effects(), schemas(), expectations(), events()
        )
        other_events = events(trace="trace-2")
        second = assurance.assess(
            contract(self, trace_id="trace-2"),
            effects(),
            schemas(),
            expectations(),
            other_events,
        )
        self.assertNotEqual(first["contract_hash"], second["contract_hash"])
        self.assertNotEqual(first["witness_hash"], second["witness_hash"])


class TraceCohesionIntegrationTests(unittest.TestCase):
    def test_base_and_cohesion_results_are_both_bound(self):
        result = api(self).ObsureTraceCohesionAssurance().assess(
            contract(self), effects(), schemas(), expectations(), events()
        )
        self.assertEqual(result["base"]["status"], "CERTIFIED")
        self.assertRegex(result["base"]["result_hash"], r"^[0-9a-f]{64}$")
        self.assertRegex(result["result_hash"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
