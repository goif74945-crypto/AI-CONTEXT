from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any, Mapping


class ChronoState(str, Enum):
    VALID = "VALID"
    NOT_YET_VALID = "NOT_YET_VALID"
    EXPIRED = "EXPIRED"
    FREEZE = "FREEZE"


class ChronoReason(str, Enum):
    OK = "OK"
    BEFORE_ACTIVATION = "BEFORE_ACTIVATION"
    DEADLINE_REACHED = "DEADLINE_REACHED"
    CLOCK_ID_MISMATCH = "CLOCK_ID_MISMATCH"
    MONOTONIC_EPOCH_MISMATCH = "MONOTONIC_EPOCH_MISMATCH"
    MONOTONIC_ROLLBACK = "MONOTONIC_ROLLBACK"
    WALL_MONOTONIC_DIVERGENCE = "WALL_MONOTONIC_DIVERGENCE"
    INVALID_SAMPLE = "INVALID_SAMPLE"
    PARENT_NOT_VALID = "PARENT_NOT_VALID"
    CHILD_BUDGET_EXHAUSTED = "CHILD_BUDGET_EXHAUSTED"


@dataclass(frozen=True, slots=True)
class TimeSample:
    """A single dual-clock observation.

    wall_ns is civil/UTC-like time and may jump.
    monotonic_ns is elapsed-process/boot time and must never move backwards within an epoch.
    clock_id names the logical clock provider. monotonic_epoch identifies the lifetime within
    which monotonic values are comparable.
    """

    wall_ns: int
    monotonic_ns: int
    clock_id: str
    monotonic_epoch: str

    def __post_init__(self) -> None:
        if self.wall_ns < 0:
            raise ValueError("wall_ns must be >= 0")
        if self.monotonic_ns < 0:
            raise ValueError("monotonic_ns must be >= 0")
        if not self.clock_id.strip():
            raise ValueError("clock_id must be non-empty")
        if not self.monotonic_epoch.strip():
            raise ValueError("monotonic_epoch must be non-empty")


@dataclass(frozen=True, slots=True)
class DeadlineEnvelope:
    envelope_id: str
    clock_id: str
    monotonic_epoch: str
    issued_wall_ns: int
    issued_monotonic_ns: int
    activate_after_ns: int
    timeout_ns: int
    max_wall_monotonic_skew_ns: int
    policy_version: str
    purpose: str
    parent_envelope_id: str | None = None

    def __post_init__(self) -> None:
        if not self.envelope_id.strip():
            raise ValueError("envelope_id must be non-empty")
        if not self.clock_id.strip():
            raise ValueError("clock_id must be non-empty")
        if not self.monotonic_epoch.strip():
            raise ValueError("monotonic_epoch must be non-empty")
        if self.issued_wall_ns < 0 or self.issued_monotonic_ns < 0:
            raise ValueError("issued times must be >= 0")
        if self.activate_after_ns < 0:
            raise ValueError("activate_after_ns must be >= 0")
        if self.timeout_ns <= 0:
            raise ValueError("timeout_ns must be > 0")
        if self.activate_after_ns >= self.timeout_ns:
            raise ValueError("activate_after_ns must be < timeout_ns")
        if self.max_wall_monotonic_skew_ns < 0:
            raise ValueError("max_wall_monotonic_skew_ns must be >= 0")
        if not self.policy_version.strip():
            raise ValueError("policy_version must be non-empty")
        if not self.purpose.strip():
            raise ValueError("purpose must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "activate_after_ns": self.activate_after_ns,
            "clock_id": self.clock_id,
            "envelope_id": self.envelope_id,
            "issued_monotonic_ns": self.issued_monotonic_ns,
            "issued_wall_ns": self.issued_wall_ns,
            "max_wall_monotonic_skew_ns": self.max_wall_monotonic_skew_ns,
            "monotonic_epoch": self.monotonic_epoch,
            "parent_envelope_id": self.parent_envelope_id,
            "policy_version": self.policy_version,
            "purpose": self.purpose,
            "timeout_ns": self.timeout_ns,
        }

    def canonical_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)

    def fingerprint(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "DeadlineEnvelope":
        expected = {
            "activate_after_ns",
            "clock_id",
            "envelope_id",
            "issued_monotonic_ns",
            "issued_wall_ns",
            "max_wall_monotonic_skew_ns",
            "monotonic_epoch",
            "parent_envelope_id",
            "policy_version",
            "purpose",
            "timeout_ns",
        }
        unknown = set(value) - expected
        missing = expected - set(value)
        if unknown:
            raise ValueError(f"unknown fields: {sorted(unknown)}")
        if missing:
            raise ValueError(f"missing fields: {sorted(missing)}")
        return cls(
            envelope_id=_expect_str(value["envelope_id"], "envelope_id"),
            clock_id=_expect_str(value["clock_id"], "clock_id"),
            monotonic_epoch=_expect_str(value["monotonic_epoch"], "monotonic_epoch"),
            issued_wall_ns=_expect_int(value["issued_wall_ns"], "issued_wall_ns"),
            issued_monotonic_ns=_expect_int(value["issued_monotonic_ns"], "issued_monotonic_ns"),
            activate_after_ns=_expect_int(value["activate_after_ns"], "activate_after_ns"),
            timeout_ns=_expect_int(value["timeout_ns"], "timeout_ns"),
            max_wall_monotonic_skew_ns=_expect_int(
                value["max_wall_monotonic_skew_ns"], "max_wall_monotonic_skew_ns"
            ),
            policy_version=_expect_str(value["policy_version"], "policy_version"),
            purpose=_expect_str(value["purpose"], "purpose"),
            parent_envelope_id=_expect_optional_str(value["parent_envelope_id"], "parent_envelope_id"),
        )

    @classmethod
    def from_json(cls, raw: str) -> "DeadlineEnvelope":
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise ValueError("deadline envelope JSON must be an object")
        return cls.from_mapping(parsed)


@dataclass(frozen=True, slots=True)
class ChronoDecision:
    state: ChronoState
    reason: ChronoReason
    elapsed_monotonic_ns: int | None
    elapsed_wall_ns: int | None
    wall_monotonic_delta_ns: int | None
    remaining_ns: int | None
    envelope_fingerprint: str

    @property
    def executable(self) -> bool:
        return self.state is ChronoState.VALID


@dataclass(frozen=True, slots=True)
class ChildDerivation:
    decision: ChronoDecision
    envelope: DeadlineEnvelope | None


def _expect_int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    return value


def _expect_str(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    return value


def _expect_optional_str(value: Any, field: str) -> str | None:
    if value is None:
        return None
    return _expect_str(value, field)


from dataclasses import replace


class ChronoIntegrityKernel:
    """Deterministic evaluator for TTL/deadline semantics under imperfect wall clocks.

    Security posture:
    - Monotonic time decides activation/expiry.
    - Wall time is cross-checked against monotonic elapsed time.
    - Clock identity/epoch mismatches fail closed.
    - Exact timeout boundary is expired, never still valid.
    """

    def issue(
        self,
        *,
        envelope_id: str,
        sample: TimeSample,
        timeout_ns: int,
        max_wall_monotonic_skew_ns: int,
        policy_version: str,
        purpose: str,
        activate_after_ns: int = 0,
        parent_envelope_id: str | None = None,
    ) -> DeadlineEnvelope:
        return DeadlineEnvelope(
            envelope_id=envelope_id,
            clock_id=sample.clock_id,
            monotonic_epoch=sample.monotonic_epoch,
            issued_wall_ns=sample.wall_ns,
            issued_monotonic_ns=sample.monotonic_ns,
            activate_after_ns=activate_after_ns,
            timeout_ns=timeout_ns,
            max_wall_monotonic_skew_ns=max_wall_monotonic_skew_ns,
            policy_version=policy_version,
            purpose=purpose,
            parent_envelope_id=parent_envelope_id,
        )

    def evaluate(self, envelope: DeadlineEnvelope, sample: TimeSample) -> ChronoDecision:
        fingerprint = envelope.fingerprint()

        if sample.clock_id != envelope.clock_id:
            return self._freeze(ChronoReason.CLOCK_ID_MISMATCH, fingerprint)
        if sample.monotonic_epoch != envelope.monotonic_epoch:
            return self._freeze(ChronoReason.MONOTONIC_EPOCH_MISMATCH, fingerprint)

        elapsed_mono = sample.monotonic_ns - envelope.issued_monotonic_ns
        elapsed_wall = sample.wall_ns - envelope.issued_wall_ns

        if elapsed_mono < 0:
            return ChronoDecision(
                state=ChronoState.FREEZE,
                reason=ChronoReason.MONOTONIC_ROLLBACK,
                elapsed_monotonic_ns=elapsed_mono,
                elapsed_wall_ns=elapsed_wall,
                wall_monotonic_delta_ns=None,
                remaining_ns=None,
                envelope_fingerprint=fingerprint,
            )

        delta = elapsed_wall - elapsed_mono
        if abs(delta) > envelope.max_wall_monotonic_skew_ns:
            return ChronoDecision(
                state=ChronoState.FREEZE,
                reason=ChronoReason.WALL_MONOTONIC_DIVERGENCE,
                elapsed_monotonic_ns=elapsed_mono,
                elapsed_wall_ns=elapsed_wall,
                wall_monotonic_delta_ns=delta,
                remaining_ns=None,
                envelope_fingerprint=fingerprint,
            )

        if elapsed_mono < envelope.activate_after_ns:
            return ChronoDecision(
                state=ChronoState.NOT_YET_VALID,
                reason=ChronoReason.BEFORE_ACTIVATION,
                elapsed_monotonic_ns=elapsed_mono,
                elapsed_wall_ns=elapsed_wall,
                wall_monotonic_delta_ns=delta,
                remaining_ns=envelope.timeout_ns - elapsed_mono,
                envelope_fingerprint=fingerprint,
            )

        if elapsed_mono >= envelope.timeout_ns:
            return ChronoDecision(
                state=ChronoState.EXPIRED,
                reason=ChronoReason.DEADLINE_REACHED,
                elapsed_monotonic_ns=elapsed_mono,
                elapsed_wall_ns=elapsed_wall,
                wall_monotonic_delta_ns=delta,
                remaining_ns=0,
                envelope_fingerprint=fingerprint,
            )

        return ChronoDecision(
            state=ChronoState.VALID,
            reason=ChronoReason.OK,
            elapsed_monotonic_ns=elapsed_mono,
            elapsed_wall_ns=elapsed_wall,
            wall_monotonic_delta_ns=delta,
            remaining_ns=envelope.timeout_ns - elapsed_mono,
            envelope_fingerprint=fingerprint,
        )

    def derive_child(
        self,
        *,
        parent: DeadlineEnvelope,
        sample: TimeSample,
        child_envelope_id: str,
        requested_timeout_ns: int,
        purpose: str,
        activate_after_ns: int = 0,
    ) -> ChildDerivation:
        if requested_timeout_ns <= 0:
            raise ValueError("requested_timeout_ns must be > 0")
        if activate_after_ns < 0:
            raise ValueError("activate_after_ns must be >= 0")

        parent_decision = self.evaluate(parent, sample)
        if parent_decision.state is not ChronoState.VALID:
            return ChildDerivation(
                decision=replace(parent_decision, reason=ChronoReason.PARENT_NOT_VALID),
                envelope=None,
            )

        assert parent_decision.remaining_ns is not None
        child_timeout = min(requested_timeout_ns, parent_decision.remaining_ns)
        if child_timeout <= 0 or activate_after_ns >= child_timeout:
            exhausted = ChronoDecision(
                state=ChronoState.FREEZE,
                reason=ChronoReason.CHILD_BUDGET_EXHAUSTED,
                elapsed_monotonic_ns=parent_decision.elapsed_monotonic_ns,
                elapsed_wall_ns=parent_decision.elapsed_wall_ns,
                wall_monotonic_delta_ns=parent_decision.wall_monotonic_delta_ns,
                remaining_ns=0,
                envelope_fingerprint=parent.fingerprint(),
            )
            return ChildDerivation(decision=exhausted, envelope=None)

        child = self.issue(
            envelope_id=child_envelope_id,
            sample=sample,
            timeout_ns=child_timeout,
            max_wall_monotonic_skew_ns=parent.max_wall_monotonic_skew_ns,
            policy_version=parent.policy_version,
            purpose=purpose,
            activate_after_ns=activate_after_ns,
            parent_envelope_id=parent.envelope_id,
        )
        return ChildDerivation(decision=self.evaluate(child, sample), envelope=child)

    @staticmethod
    def _freeze(reason: ChronoReason, fingerprint: str) -> ChronoDecision:
        return ChronoDecision(
            state=ChronoState.FREEZE,
            reason=reason,
            elapsed_monotonic_ns=None,
            elapsed_wall_ns=None,
            wall_monotonic_delta_ns=None,
            remaining_ns=None,
            envelope_fingerprint=fingerprint,
        )


from dataclasses import dataclass
import time
import uuid


class SystemDualClock:
    """Process-local dual clock.

    The monotonic epoch intentionally changes when this object is recreated. Persistent systems
    must not compare monotonic timestamps across unknown process/boot epochs without an external
    time-continuity mechanism.
    """

    def __init__(self, *, clock_id: str = "system") -> None:
        if not clock_id.strip():
            raise ValueError("clock_id must be non-empty")
        self._clock_id = clock_id
        self._epoch = uuid.uuid4().hex

    def sample(self) -> TimeSample:
        return TimeSample(
            wall_ns=time.time_ns(),
            monotonic_ns=time.monotonic_ns(),
            clock_id=self._clock_id,
            monotonic_epoch=self._epoch,
        )


@dataclass(slots=True)
class FakeDualClock:
    wall_ns: int
    monotonic_ns: int
    clock_id: str = "fake"
    monotonic_epoch: str = "epoch-1"

    def sample(self) -> TimeSample:
        return TimeSample(
            wall_ns=self.wall_ns,
            monotonic_ns=self.monotonic_ns,
            clock_id=self.clock_id,
            monotonic_epoch=self.monotonic_epoch,
        )

    def advance(self, ns: int, *, wall_adjust_ns: int = 0) -> None:
        if ns < 0:
            raise ValueError("advance ns must be >= 0")
        self.monotonic_ns += ns
        self.wall_ns += ns + wall_adjust_ns
