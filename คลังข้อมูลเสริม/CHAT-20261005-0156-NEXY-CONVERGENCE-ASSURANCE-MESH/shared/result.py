from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class GateResult:
    status: str
    reason: str
    details: Mapping[str, Any] = field(default_factory=dict)

    @property
    def releasable(self) -> bool:
        return self.status in {"PASS", "RELEASE", "READY", "PLANNED", "VERIFIED"}
