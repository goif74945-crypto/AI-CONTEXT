from __future__ import annotations

import json
import random
import unittest

from nexy_chrono_integrity import ChronoIntegrityKernel, ChronoReason, ChronoState, DeadlineEnvelope, FakeDualClock, SystemDualClock, TimeSample

NS = 1_000_000_000

class ChronoIntegrityKernelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.kernel = ChronoIntegrityKernel()
        self.clock = FakeDualClock(wall_ns=1_800_000_000 * NS, monotonic_ns=100 * NS)
        self.base = self.kernel.issue(
            envelope_id="base",
            sample=self.clock.sample(),
            timeout_ns=300 * NS,
            max_wall_monotonic_skew_ns=2 * NS,
            policy_version="p1",
            purpose="test",
        )

    def test_initial_sample_is_valid(self) -> None:
        decision = self.kernel.evaluate(self.base, self.clock.sample())
        self.assertEqual(decision.state, ChronoState.VALID)
        self.assertEqual(decision.reason, ChronoReason.OK)
        self.assertEqual(decision.remaining_ns, 300 * NS)

    def test_exact_timeout_boundary_is_expired(self) -> None:
        self.clock.advance(300 * NS)
        decision = self.kernel.evaluate(self.base, self.clock.sample())
        self.assertEqual(decision.state, ChronoState.EXPIRED)
        self.assertEqual(decision.reason, ChronoReason.DEADLINE_REACHED)
        self.assertEqual(decision.remaining_ns, 0)

    def test_one_nanosecond_before_timeout_is_valid(self) -> None:
        self.clock.advance(300 * NS - 1)
        decision = self.kernel.evaluate(self.base, self.clock.sample())
        self.assertEqual(decision.state, ChronoState.VALID)
        self.assertEqual(decision.remaining_ns, 1)

    def test_after_timeout_is_expired(self) -> None:
        self.clock.advance(301 * NS)
        decision = self.kernel.evaluate(self.base, self.clock.sample())
        self.assertEqual(decision.state, ChronoState.EXPIRED)

    def test_small_wall_clock_drift_within_budget_is_accepted(self) -> None:
        self.clock.advance(10 * NS, wall_adjust_ns=2 * NS)
        decision = self.kernel.evaluate(self.base, self.clock.sample())
        self.assertEqual(decision.state, ChronoState.VALID)
        self.assertEqual(decision.wall_monotonic_delta_ns, 2 * NS)

    def test_wall_clock_drift_above_budget_freezes(self) -> None:
        self.clock.advance(10 * NS, wall_adjust_ns=2 * NS + 1)
        decision = self.kernel.evaluate(self.base, self.clock.sample())
        self.assertEqual(decision.state, ChronoState.FREEZE)
        self.assertEqual(decision.reason, ChronoReason.WALL_MONOTONIC_DIVERGENCE)
        self.assertFalse(decision.executable)

    def test_wall_clock_rollback_above_budget_freezes(self) -> None:
        self.clock.advance(10 * NS, wall_adjust_ns=-(3 * NS))
        decision = self.kernel.evaluate(self.base, self.clock.sample())
        self.assertEqual(decision.state, ChronoState.FREEZE)
        self.assertEqual(decision.reason, ChronoReason.WALL_MONOTONIC_DIVERGENCE)

    def test_monotonic_rollback_freezes(self) -> None:
        sample = TimeSample(
            wall_ns=self.base.issued_wall_ns,
            monotonic_ns=self.base.issued_monotonic_ns - 1,
            clock_id=self.base.clock_id,
            monotonic_epoch=self.base.monotonic_epoch,
        )
        decision = self.kernel.evaluate(self.base, sample)
        self.assertEqual(decision.state, ChronoState.FREEZE)
        self.assertEqual(decision.reason, ChronoReason.MONOTONIC_ROLLBACK)

    def test_clock_id_mismatch_freezes(self) -> None:
        sample = TimeSample(
            wall_ns=self.base.issued_wall_ns,
            monotonic_ns=self.base.issued_monotonic_ns,
            clock_id="other",
            monotonic_epoch=self.base.monotonic_epoch,
        )
        decision = self.kernel.evaluate(self.base, sample)
        self.assertEqual(decision.reason, ChronoReason.CLOCK_ID_MISMATCH)
        self.assertEqual(decision.state, ChronoState.FREEZE)

    def test_epoch_mismatch_freezes(self) -> None:
        sample = TimeSample(
            wall_ns=self.base.issued_wall_ns,
            monotonic_ns=self.base.issued_monotonic_ns,
            clock_id=self.base.clock_id,
            monotonic_epoch="epoch-2",
        )
        decision = self.kernel.evaluate(self.base, sample)
        self.assertEqual(decision.reason, ChronoReason.MONOTONIC_EPOCH_MISMATCH)
        self.assertEqual(decision.state, ChronoState.FREEZE)

    def test_activation_window_blocks_before_start(self) -> None:
        delayed = self.kernel.issue(
            envelope_id="delayed",
            sample=self.clock.sample(),
            timeout_ns=30 * NS,
            activate_after_ns=10 * NS,
            max_wall_monotonic_skew_ns=2 * NS,
            policy_version="p1",
            purpose="delayed",
        )
        self.clock.advance(9 * NS)
        decision = self.kernel.evaluate(delayed, self.clock.sample())
        self.assertEqual(decision.state, ChronoState.NOT_YET_VALID)
        self.assertEqual(decision.reason, ChronoReason.BEFORE_ACTIVATION)

    def test_activation_exact_boundary_becomes_valid(self) -> None:
        delayed = self.kernel.issue(
            envelope_id="delayed",
            sample=self.clock.sample(),
            timeout_ns=30 * NS,
            activate_after_ns=10 * NS,
            max_wall_monotonic_skew_ns=2 * NS,
            policy_version="p1",
            purpose="delayed",
        )
        self.clock.advance(10 * NS)
        decision = self.kernel.evaluate(delayed, self.clock.sample())
        self.assertEqual(decision.state, ChronoState.VALID)

    def test_child_timeout_is_capped_by_parent_remaining_budget(self) -> None:
        self.clock.advance(250 * NS)
        derived = self.kernel.derive_child(
            parent=self.base,
            sample=self.clock.sample(),
            child_envelope_id="child",
            requested_timeout_ns=100 * NS,
            purpose="child",
        )
        self.assertIsNotNone(derived.envelope)
        assert derived.envelope is not None
        self.assertEqual(derived.envelope.timeout_ns, 50 * NS)
        self.assertEqual(derived.envelope.parent_envelope_id, "base")

    def test_child_timeout_can_be_smaller_than_parent_remaining_budget(self) -> None:
        self.clock.advance(20 * NS)
        derived = self.kernel.derive_child(
            parent=self.base,
            sample=self.clock.sample(),
            child_envelope_id="child",
            requested_timeout_ns=10 * NS,
            purpose="child",
        )
        assert derived.envelope is not None
        self.assertEqual(derived.envelope.timeout_ns, 10 * NS)

    def test_child_derivation_fails_closed_when_parent_expired(self) -> None:
        self.clock.advance(300 * NS)
        derived = self.kernel.derive_child(
            parent=self.base,
            sample=self.clock.sample(),
            child_envelope_id="child",
            requested_timeout_ns=10 * NS,
            purpose="child",
        )
        self.assertIsNone(derived.envelope)
        self.assertEqual(derived.decision.state, ChronoState.EXPIRED)
        self.assertEqual(derived.decision.reason, ChronoReason.PARENT_NOT_VALID)

    def test_child_derivation_fails_closed_when_parent_clock_invalid(self) -> None:
        self.clock.advance(1 * NS, wall_adjust_ns=10 * NS)
        derived = self.kernel.derive_child(
            parent=self.base,
            sample=self.clock.sample(),
            child_envelope_id="child",
            requested_timeout_ns=10 * NS,
            purpose="child",
        )
        self.assertIsNone(derived.envelope)
        self.assertEqual(derived.decision.state, ChronoState.FREEZE)
        self.assertEqual(derived.decision.reason, ChronoReason.PARENT_NOT_VALID)

    def test_child_activation_cannot_consume_entire_budget(self) -> None:
        self.clock.advance(290 * NS)
        derived = self.kernel.derive_child(
            parent=self.base,
            sample=self.clock.sample(),
            child_envelope_id="child",
            requested_timeout_ns=20 * NS,
            activate_after_ns=10 * NS,
            purpose="child",
        )
        self.assertIsNone(derived.envelope)
        self.assertEqual(derived.decision.reason, ChronoReason.CHILD_BUDGET_EXHAUSTED)

    def test_envelope_round_trip_preserves_fingerprint(self) -> None:
        raw = self.base.canonical_json()
        decoded = DeadlineEnvelope.from_json(raw)
        self.assertEqual(decoded, self.base)
        self.assertEqual(decoded.fingerprint(), self.base.fingerprint())

    def test_canonical_json_is_key_order_independent(self) -> None:
        mapping = self.base.to_dict()
        reverse = {key: mapping[key] for key in reversed(list(mapping.keys()))}
        decoded = DeadlineEnvelope.from_mapping(reverse)
        self.assertEqual(decoded.fingerprint(), self.base.fingerprint())

    def test_unknown_serialized_field_is_rejected(self) -> None:
        mapping = self.base.to_dict()
        mapping["surprise"] = True
        with self.assertRaises(ValueError):
            DeadlineEnvelope.from_mapping(mapping)

    def test_missing_serialized_field_is_rejected(self) -> None:
        mapping = self.base.to_dict()
        del mapping["purpose"]
        with self.assertRaises(ValueError):
            DeadlineEnvelope.from_mapping(mapping)

    def test_boolean_is_not_accepted_as_integer(self) -> None:
        mapping = self.base.to_dict()
        mapping["timeout_ns"] = True
        with self.assertRaises(ValueError):
            DeadlineEnvelope.from_mapping(mapping)

    def test_non_object_json_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            DeadlineEnvelope.from_json(json.dumps([1, 2, 3]))

    def test_invalid_timeout_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.kernel.issue(
                envelope_id="x",
                sample=self.clock.sample(),
                timeout_ns=0,
                max_wall_monotonic_skew_ns=0,
                policy_version="p1",
                purpose="x",
            )

    def test_activation_equal_to_timeout_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.kernel.issue(
                envelope_id="x",
                sample=self.clock.sample(),
                timeout_ns=10,
                activate_after_ns=10,
                max_wall_monotonic_skew_ns=0,
                policy_version="p1",
                purpose="x",
            )

    def test_negative_skew_budget_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.kernel.issue(
                envelope_id="x",
                sample=self.clock.sample(),
                timeout_ns=10,
                max_wall_monotonic_skew_ns=-1,
                policy_version="p1",
                purpose="x",
            )

    def test_fake_clock_rejects_negative_advance(self) -> None:
        with self.assertRaises(ValueError):
            self.clock.advance(-1)

    def test_fingerprint_changes_when_policy_version_changes(self) -> None:
        changed = DeadlineEnvelope(
            **{**self.base.to_dict(), "policy_version": "p2"}
        )
        self.assertNotEqual(changed.fingerprint(), self.base.fingerprint())

    def test_fingerprint_changes_when_timeout_changes(self) -> None:
        changed = DeadlineEnvelope(
            **{**self.base.to_dict(), "timeout_ns": self.base.timeout_ns + 1}
        )
        self.assertNotEqual(changed.fingerprint(), self.base.fingerprint())

    def test_property_validity_is_controlled_by_monotonic_elapsed_within_skew(self) -> None:
        rng = random.Random(1337)
        for i in range(1000):
            timeout = rng.randint(2, 1_000_000)
            activation = rng.randint(0, timeout - 1)
            elapsed = rng.randint(0, timeout + 100)
            skew_budget = rng.randint(0, 100)
            drift = rng.randint(-skew_budget, skew_budget)
            issued = TimeSample(
                wall_ns=10_000_000,
                monotonic_ns=50_000_000,
                clock_id="prop",
                monotonic_epoch="epoch",
            )
            envelope = self.kernel.issue(
                envelope_id=f"p-{i}",
                sample=issued,
                timeout_ns=timeout,
                activate_after_ns=activation,
                max_wall_monotonic_skew_ns=skew_budget,
                policy_version="p1",
                purpose="property",
            )
            now = TimeSample(
                wall_ns=issued.wall_ns + elapsed + drift,
                monotonic_ns=issued.monotonic_ns + elapsed,
                clock_id="prop",
                monotonic_epoch="epoch",
            )
            decision = self.kernel.evaluate(envelope, now)
            expected = (
                ChronoState.NOT_YET_VALID
                if elapsed < activation
                else ChronoState.EXPIRED
                if elapsed >= timeout
                else ChronoState.VALID
            )
            self.assertEqual(decision.state, expected)

    def test_property_any_drift_above_budget_freezes_before_deadline_logic(self) -> None:
        rng = random.Random(7331)
        for i in range(500):
            timeout = rng.randint(2, 1_000_000)
            skew_budget = rng.randint(0, 100)
            elapsed = rng.randint(0, timeout + 100)
            sign = -1 if i % 2 else 1
            drift = sign * (skew_budget + rng.randint(1, 100))
            issued = TimeSample(
                wall_ns=20_000_000,
                monotonic_ns=70_000_000,
                clock_id="prop2",
                monotonic_epoch="epoch",
            )
            envelope = self.kernel.issue(
                envelope_id=f"q-{i}",
                sample=issued,
                timeout_ns=timeout,
                max_wall_monotonic_skew_ns=skew_budget,
                policy_version="p1",
                purpose="property",
            )
            now = TimeSample(
                wall_ns=issued.wall_ns + elapsed + drift,
                monotonic_ns=issued.monotonic_ns + elapsed,
                clock_id="prop2",
                monotonic_epoch="epoch",
            )
            decision = self.kernel.evaluate(envelope, now)
            self.assertEqual(decision.state, ChronoState.FREEZE)
            self.assertEqual(decision.reason, ChronoReason.WALL_MONOTONIC_DIVERGENCE)

    def test_same_inputs_are_deterministic(self) -> None:
        self.clock.advance(42 * NS)
        sample = self.clock.sample()
        a = self.kernel.evaluate(self.base, sample)
        b = self.kernel.evaluate(self.base, sample)
        self.assertEqual(a, b)

    def test_decision_fingerprint_matches_envelope(self) -> None:
        decision = self.kernel.evaluate(self.base, self.clock.sample())
        self.assertEqual(decision.envelope_fingerprint, self.base.fingerprint())


class ClockTests(unittest.TestCase):
    def test_system_clock_samples_keep_same_epoch(self) -> None:
        clock = SystemDualClock(clock_id="x")
        a = clock.sample()
        b = clock.sample()
        self.assertEqual(a.clock_id, "x")
        self.assertEqual(a.monotonic_epoch, b.monotonic_epoch)
        self.assertGreaterEqual(b.monotonic_ns, a.monotonic_ns)

    def test_two_system_clock_instances_use_distinct_epochs(self) -> None:
        a = SystemDualClock(clock_id="x").sample()
        b = SystemDualClock(clock_id="x").sample()
        self.assertNotEqual(a.monotonic_epoch, b.monotonic_epoch)

    def test_fake_clock_advances_both_clocks(self) -> None:
        clock = FakeDualClock(wall_ns=100, monotonic_ns=200)
        clock.advance(10)
        sample = clock.sample()
        self.assertEqual(sample.wall_ns, 110)
        self.assertEqual(sample.monotonic_ns, 210)

    def test_fake_clock_can_model_wall_jump(self) -> None:
        clock = FakeDualClock(wall_ns=100, monotonic_ns=200)
        clock.advance(10, wall_adjust_ns=50)
        sample = clock.sample()
        self.assertEqual(sample.wall_ns, 160)
        self.assertEqual(sample.monotonic_ns, 210)


class ModelValidationTests(unittest.TestCase):
    def test_time_sample_rejects_negative_wall(self) -> None:
        with self.assertRaises(ValueError):
            TimeSample(wall_ns=-1, monotonic_ns=0, clock_id="x", monotonic_epoch="e")

    def test_time_sample_rejects_negative_monotonic(self) -> None:
        with self.assertRaises(ValueError):
            TimeSample(wall_ns=0, monotonic_ns=-1, clock_id="x", monotonic_epoch="e")

    def test_time_sample_rejects_blank_clock_id(self) -> None:
        with self.assertRaises(ValueError):
            TimeSample(wall_ns=0, monotonic_ns=0, clock_id=" ", monotonic_epoch="e")

    def test_time_sample_rejects_blank_epoch(self) -> None:
        with self.assertRaises(ValueError):
            TimeSample(wall_ns=0, monotonic_ns=0, clock_id="x", monotonic_epoch=" ")

    def test_deadline_rejects_blank_identity(self) -> None:
        with self.assertRaises(ValueError):
            DeadlineEnvelope(
                envelope_id="",
                clock_id="x",
                monotonic_epoch="e",
                issued_wall_ns=0,
                issued_monotonic_ns=0,
                activate_after_ns=0,
                timeout_ns=1,
                max_wall_monotonic_skew_ns=0,
                policy_version="p",
                purpose="x",
            )
