from __future__ import annotations

from dataclasses import dataclass

from .canonical import fingerprint
from .models import EvidenceState, OperatorSignal, Salience, Severity, SignalKind


@dataclass(frozen=True)
class SalienceDecision:
    salience: Salience
    reasons: tuple[str, ...]
    fingerprint: str

    def as_dict(self) -> dict[str, object]:
        return {"fingerprint": self.fingerprint, "reasons": list(self.reasons), "salience": self.salience.value}


def classify_salience(signal: OperatorSignal) -> SalienceDecision:
    reasons: set[str] = set()

    if signal.kind in {SignalKind.FREEZE, SignalKind.SECURITY}:
        reasons.add(f"kind:{signal.kind.value}")
        level = Salience.CRITICAL
    elif signal.severity is Severity.CRITICAL:
        reasons.add("severity:CRITICAL")
        level = Salience.CRITICAL
    elif signal.evidence is EvidenceState.CONFLICT and (signal.blocking or signal.requires_user):
        reasons.add("blocking_conflict")
        level = Salience.CRITICAL
    elif signal.requires_user or signal.blocking or signal.kind in {SignalKind.ERROR, SignalKind.DECISION_REQUIRED}:
        if signal.requires_user:
            reasons.add("requires_user")
        if signal.blocking:
            reasons.add("blocking")
        if signal.kind in {SignalKind.ERROR, SignalKind.DECISION_REQUIRED}:
            reasons.add(f"kind:{signal.kind.value}")
        level = Salience.HIGH
    elif signal.severity is Severity.HIGH:
        reasons.add("severity:HIGH")
        level = Salience.HIGH
    elif signal.state_changed or signal.evidence_changed or signal.kind in {SignalKind.WARNING, SignalKind.COMPLETION}:
        if signal.state_changed:
            reasons.add("state_changed")
        if signal.evidence_changed:
            reasons.add("evidence_changed")
        if signal.kind in {SignalKind.WARNING, SignalKind.COMPLETION}:
            reasons.add(f"kind:{signal.kind.value}")
        level = Salience.NORMAL
    else:
        reasons.add("routine_signal")
        level = Salience.LOW

    payload = {
        "signal": signal.canonical_dict(),
        "salience": level.value,
        "reasons": sorted(reasons),
    }
    return SalienceDecision(level, tuple(sorted(reasons)), fingerprint(payload))
