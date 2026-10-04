from __future__ import annotations

from dataclasses import dataclass

from .canonical import fingerprint
from .models import Delivery, OperatorSignal, Salience, SignalKind
from .salience import classify_salience


@dataclass(frozen=True)
class RouteDecision:
    delivery: Delivery
    reasons: tuple[str, ...]
    salience: Salience
    fingerprint: str

    def as_dict(self) -> dict[str, object]:
        return {
            "delivery": self.delivery.value,
            "fingerprint": self.fingerprint,
            "reasons": list(self.reasons),
            "salience": self.salience.value,
        }


def route_signal(signal: OperatorSignal, *, quiet_mode: bool = False) -> RouteDecision:
    salience = classify_salience(signal)
    reasons = set(salience.reasons)

    if signal.kind in {SignalKind.FREEZE, SignalKind.SECURITY} or salience.salience is Salience.CRITICAL:
        delivery = Delivery.NOW
        reasons.add("non_suppressible")
    elif salience.salience is Salience.HIGH:
        delivery = Delivery.NOW if signal.requires_user or signal.blocking else Delivery.BATCH
        reasons.add("high_attention")
    elif salience.salience is Salience.NORMAL:
        delivery = Delivery.BATCH
        reasons.add("batchable")
    else:
        delivery = Delivery.SILENT_LOG if quiet_mode else Delivery.BATCH
        reasons.add("quiet_mode" if quiet_mode else "routine_batch")

    if signal.requires_ack and delivery is Delivery.SILENT_LOG:
        delivery = Delivery.BATCH
        reasons.add("ack_requires_visibility")

    payload = {
        "delivery": delivery.value,
        "quiet_mode": quiet_mode,
        "reasons": sorted(reasons),
        "salience": salience.salience.value,
        "signal": signal.canonical_dict(),
    }
    return RouteDecision(delivery, tuple(sorted(reasons)), salience.salience, fingerprint(payload))
