from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .canonical import fingerprint
from .models import Delivery, EvidenceState, OperatorSignal, SignalKind
from .routing import route_signal


@dataclass(frozen=True)
class CompressedMilestone:
    signal: OperatorSignal
    collapsed_before: int

    def as_dict(self) -> dict[str, object]:
        return {"collapsed_before": self.collapsed_before, "signal": self.signal.canonical_dict()}


@dataclass(frozen=True)
class CompressionResult:
    input_count: int
    output_count: int
    milestones: tuple[CompressedMilestone, ...]
    trailing_collapsed: int
    fingerprint: str

    def as_dict(self) -> dict[str, object]:
        return {
            "fingerprint": self.fingerprint,
            "input_count": self.input_count,
            "milestones": [m.as_dict() for m in self.milestones],
            "output_count": self.output_count,
            "trailing_collapsed": self.trailing_collapsed,
        }


def _validate_order(signals: list[OperatorSignal]) -> list[OperatorSignal]:
    ordered = sorted(signals, key=lambda s: (s.sequence, s.signal_id))
    seqs = [s.sequence for s in ordered]
    if len(set(seqs)) != len(seqs):
        raise ValueError("signal sequences must be unique")
    ids = [s.signal_id for s in ordered]
    if len(set(ids)) != len(ids):
        raise ValueError("signal_id values must be unique")
    return ordered


def compress_milestones(signals: Iterable[OperatorSignal]) -> CompressionResult:
    items = _validate_order(list(signals))
    last_semantic: dict[str, tuple[str, EvidenceState, SignalKind]] = {}
    pending_collapsed = 0
    kept: list[CompressedMilestone] = []

    for signal in items:
        semantic = (signal.state, signal.evidence, signal.kind)
        previous = last_semantic.get(signal.component)
        route = route_signal(signal, quiet_mode=True)
        keep = (
            previous is None
            or semantic != previous
            or signal.state_changed
            or signal.evidence_changed
            or signal.requires_user
            or signal.requires_ack
            or route.delivery is Delivery.NOW
            or signal.kind is SignalKind.COMPLETION
        )
        if keep:
            kept.append(CompressedMilestone(signal=signal, collapsed_before=pending_collapsed))
            pending_collapsed = 0
            last_semantic[signal.component] = semantic
        else:
            pending_collapsed += 1

    if pending_collapsed and not kept:
        raise AssertionError("non-empty input cannot compress to zero milestones")

    data = {
        "input_count": len(items),
        "milestones": [m.as_dict() for m in kept],
        "output_count": len(kept),
        "trailing_collapsed": pending_collapsed,
    }
    return CompressionResult(len(items), len(kept), tuple(kept), pending_collapsed, fingerprint(data))
