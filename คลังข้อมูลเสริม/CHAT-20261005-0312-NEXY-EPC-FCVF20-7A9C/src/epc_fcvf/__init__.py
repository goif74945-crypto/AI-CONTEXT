"""EPC Formal Constitutional Verification Fabric 20.

Lo4 proposal-only reference package. It has no NEXY mutation authority.
"""

from .q64 import Q64, Q64Error
from .model import (
    CourtState,
    EvidenceKind,
    EvidenceRef,
    Event,
    EventKind,
    WorkStatus,
    VoteRound,
    Disposition,
)
from .engine import Constitution, STRICT_CONSTITUTION, transition, initial_state
from .systems import SYSTEM_REGISTRY, evaluate_all

__all__ = [
    "Q64", "Q64Error", "CourtState", "EvidenceKind", "EvidenceRef",
    "Event", "EventKind", "WorkStatus", "VoteRound", "Disposition",
    "Constitution", "STRICT_CONSTITUTION", "transition", "initial_state",
    "SYSTEM_REGISTRY", "evaluate_all",
]
