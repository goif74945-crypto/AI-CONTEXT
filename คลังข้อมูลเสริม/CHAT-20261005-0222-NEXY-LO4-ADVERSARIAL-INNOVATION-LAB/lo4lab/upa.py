from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class TruthState(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"
    CONFLICT = "CONFLICT"


_BITS = {
    TruthState.TRUE: (1, 0),
    TruthState.FALSE: (0, 1),
    TruthState.UNKNOWN: (0, 0),
    TruthState.CONFLICT: (1, 1),
}
_FROM_BITS = {bits: state for state, bits in _BITS.items()}


@dataclass(frozen=True)
class EvidenceValue:
    state: TruthState
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if len(set(self.provenance)) != len(self.provenance):
            raise ValueError("provenance entries must be unique")
        if any(not item for item in self.provenance):
            raise ValueError("provenance entries must be non-empty")

    @property
    def releaseable(self) -> bool:
        return self.state is TruthState.TRUE

    def _merge_provenance(self, other: "EvidenceValue") -> tuple[str, ...]:
        return tuple(dict.fromkeys((*self.provenance, *other.provenance)))

    def negate(self) -> "EvidenceValue":
        t, f = _BITS[self.state]
        return EvidenceValue(_FROM_BITS[(f, t)], self.provenance)

    def logical_and(self, other: "EvidenceValue") -> "EvidenceValue":
        t1, f1 = _BITS[self.state]
        t2, f2 = _BITS[other.state]
        state = _FROM_BITS[(t1 & t2, f1 | f2)]
        return EvidenceValue(state, self._merge_provenance(other))

    def logical_or(self, other: "EvidenceValue") -> "EvidenceValue":
        t1, f1 = _BITS[self.state]
        t2, f2 = _BITS[other.state]
        state = _FROM_BITS[(t1 | t2, f1 & f2)]
        return EvidenceValue(state, self._merge_provenance(other))

    def knowledge_join(self, other: "EvidenceValue") -> "EvidenceValue":
        """Merge independent assertions without discarding contradiction.

        TRUE joined with FALSE becomes CONFLICT. UNKNOWN joined with a known
        assertion becomes that known assertion. Provenance is always retained.
        """
        t1, f1 = _BITS[self.state]
        t2, f2 = _BITS[other.state]
        state = _FROM_BITS[(t1 | t2, f1 | f2)]
        return EvidenceValue(state, self._merge_provenance(other))

    @staticmethod
    def require_all(values: Iterable["EvidenceValue"]) -> "EvidenceValue":
        data = tuple(values)
        if not data:
            raise ValueError("require_all needs at least one value")
        out = data[0]
        for value in data[1:]:
            out = out.logical_and(value)
        return out
