from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .model import Capsule, EventKind
from .replay import replay


@dataclass(frozen=True, slots=True)
class TrustReceipt:
    """Compact, payload-minimized receipt for a verified capsule."""

    capsule_id: str
    proposal_status: str
    project_target: str
    authority_fingerprint: str
    terminal_state: str
    event_count: int
    event_kind_counts: dict[str, int]
    verification_status_counts: dict[str, int]
    tool_action_count: int
    output_digest: str
    freeze_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "capsule_id": self.capsule_id,
            "proposal_status": self.proposal_status,
            "project_target": self.project_target,
            "authority_fingerprint": self.authority_fingerprint,
            "terminal_state": self.terminal_state,
            "event_count": self.event_count,
            "event_kind_counts": self.event_kind_counts,
            "verification_status_counts": self.verification_status_counts,
            "tool_action_count": self.tool_action_count,
            "output_digest": self.output_digest,
            "freeze_reason": self.freeze_reason,
        }


def public_receipt(capsule: Capsule) -> TrustReceipt:
    report = replay(capsule)
    final = next(event for event in reversed(capsule.events) if event.kind is EventKind.FINAL)
    event_counts = Counter(event.kind.value for event in capsule.events)
    verification_counts = Counter(report.verification_statuses)
    return TrustReceipt(
        capsule_id=capsule.capsule_id,
        proposal_status=capsule.proposal_status,
        project_target=capsule.project_target,
        authority_fingerprint=capsule.authority_fingerprint,
        terminal_state=capsule.terminal_state.value,
        event_count=len(capsule.events),
        event_kind_counts=dict(sorted(event_counts.items())),
        verification_status_counts=dict(sorted(verification_counts.items())),
        tool_action_count=len(report.tool_actions),
        output_digest=str(final.payload["output_digest"]),
        freeze_reason=report.freeze_reason,
    )
