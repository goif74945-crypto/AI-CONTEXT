from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .canonical import fingerprint
from .models import OperatorSignal, Severity


class DebtState(str, Enum):
    ACTIVE = "ACTIVE"
    OVERDUE = "OVERDUE"
    ACKNOWLEDGED = "ACKNOWLEDGED"


DEFAULT_BUDGET = {
    Severity.LOW: 20,
    Severity.NORMAL: 10,
    Severity.HIGH: 4,
    Severity.CRITICAL: 1,
}


@dataclass(frozen=True)
class AckRecord:
    signal_id: str
    sequence: int

    @classmethod
    def from_dict(cls, raw: dict[str, object]) -> "AckRecord":
        signal_id = raw.get("signal_id")
        sequence = raw.get("sequence")
        if not isinstance(signal_id, str) or not signal_id:
            raise ValueError("ack signal_id must be a non-empty string")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
            raise ValueError("ack sequence must be a non-negative integer")
        return cls(signal_id, sequence)


@dataclass(frozen=True)
class DebtItem:
    signal_id: str
    severity: Severity
    opened_sequence: int
    due_sequence: int
    state: DebtState
    acknowledged_sequence: int | None

    def as_dict(self) -> dict[str, object]:
        return {
            "acknowledged_sequence": self.acknowledged_sequence,
            "due_sequence": self.due_sequence,
            "opened_sequence": self.opened_sequence,
            "severity": self.severity.value,
            "signal_id": self.signal_id,
            "state": self.state.value,
        }


@dataclass(frozen=True)
class DebtSnapshot:
    current_sequence: int
    all_clear: bool
    items: tuple[DebtItem, ...]
    fingerprint: str

    def as_dict(self) -> dict[str, object]:
        return {
            "all_clear": self.all_clear,
            "current_sequence": self.current_sequence,
            "fingerprint": self.fingerprint,
            "items": [item.as_dict() for item in self.items],
        }


def build_ack_debt(
    signals: Iterable[OperatorSignal],
    acknowledgements: Iterable[AckRecord],
    *,
    current_sequence: int,
    budget: dict[Severity, int] | None = None,
) -> DebtSnapshot:
    if not isinstance(current_sequence, int) or isinstance(current_sequence, bool) or current_sequence < 0:
        raise ValueError("current_sequence must be a non-negative integer")
    limits = dict(DEFAULT_BUDGET if budget is None else budget)
    if set(limits) != set(Severity):
        raise ValueError("budget must define every severity")
    if any(not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in limits.values()):
        raise ValueError("budget values must be non-negative integers")

    debt_signals = sorted((s for s in signals if s.requires_ack), key=lambda s: (s.sequence, s.signal_id))
    if len({s.signal_id for s in debt_signals}) != len(debt_signals):
        raise ValueError("ack-required signal_id values must be unique")
    if any(s.sequence > current_sequence for s in debt_signals):
        raise ValueError("cannot include future signals")

    acks = sorted(list(acknowledgements), key=lambda a: (a.sequence, a.signal_id))
    if len({a.signal_id for a in acks}) != len(acks):
        raise ValueError("each signal may be acknowledged at most once")
    signal_by_id = {s.signal_id: s for s in debt_signals}
    for ack in acks:
        if ack.signal_id not in signal_by_id:
            raise ValueError(f"ack references unknown/non-ack signal: {ack.signal_id}")
        if ack.sequence < signal_by_id[ack.signal_id].sequence:
            raise ValueError(f"ack precedes signal: {ack.signal_id}")
        if ack.sequence > current_sequence:
            raise ValueError(f"ack occurs in the future: {ack.signal_id}")
    ack_by_id = {a.signal_id: a for a in acks}

    items: list[DebtItem] = []
    for signal in debt_signals:
        due = signal.sequence + limits[signal.severity]
        ack = ack_by_id.get(signal.signal_id)
        if ack is not None:
            state = DebtState.ACKNOWLEDGED
            ack_seq = ack.sequence
        elif current_sequence > due:
            state = DebtState.OVERDUE
            ack_seq = None
        else:
            state = DebtState.ACTIVE
            ack_seq = None
        items.append(DebtItem(signal.signal_id, signal.severity, signal.sequence, due, state, ack_seq))

    all_clear = not any(
        item.state is not DebtState.ACKNOWLEDGED and item.severity in {Severity.HIGH, Severity.CRITICAL}
        for item in items
    )
    data = {"all_clear": all_clear, "current_sequence": current_sequence, "items": [i.as_dict() for i in items]}
    return DebtSnapshot(current_sequence, all_clear, tuple(items), fingerprint(data))
