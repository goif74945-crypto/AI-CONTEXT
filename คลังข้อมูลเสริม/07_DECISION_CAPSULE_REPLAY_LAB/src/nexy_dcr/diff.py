from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import sha256_hex
from .model import Capsule


@dataclass(frozen=True, slots=True)
class Divergence:
    category: str
    path: str
    left: Any
    right: Any

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "path": self.path,
            "left": self.left,
            "right": self.right,
        }


def diff_capsules(left: Capsule, right: Capsule) -> list[Divergence]:
    differences: list[Divergence] = []

    if left.project_target != right.project_target:
        differences.append(
            Divergence("identity", "project_target", left.project_target, right.project_target)
        )

    if left.authority_fingerprint != right.authority_fingerprint:
        differences.append(
            Divergence(
                "authority",
                "authority_fingerprint",
                left.authority_fingerprint,
                right.authority_fingerprint,
            )
        )

    if left.terminal_state != right.terminal_state:
        differences.append(
            Divergence(
                "terminal",
                "terminal_state",
                left.terminal_state.value,
                right.terminal_state.value,
            )
        )

    common = min(len(left.events), len(right.events))
    for index in range(common):
        le = left.events[index]
        re = right.events[index]
        if le.kind != re.kind:
            differences.append(
                Divergence("event_kind", f"events[{index}].kind", le.kind.value, re.kind.value)
            )
            continue
        left_payload_digest = sha256_hex(le.payload)
        right_payload_digest = sha256_hex(re.payload)
        if left_payload_digest != right_payload_digest:
            differences.append(
                Divergence(
                    "event_payload",
                    f"events[{index}].payload",
                    {"digest": left_payload_digest, "payload": le.payload},
                    {"digest": right_payload_digest, "payload": re.payload},
                )
            )

    if len(left.events) != len(right.events):
        differences.append(
            Divergence("event_count", "events.length", len(left.events), len(right.events))
        )

    return differences
