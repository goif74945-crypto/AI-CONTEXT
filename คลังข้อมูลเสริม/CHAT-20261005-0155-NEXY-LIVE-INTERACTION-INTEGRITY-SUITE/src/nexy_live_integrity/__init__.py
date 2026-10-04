"""NEXY Live Interaction Integrity Suite.

Reference-only package. It does not mutate or integrate with NEXY.AI runtime.
"""

from .common import GateDecision, GateStatus, canonical_digest, canonical_json
from .interrupt_epoch import ActionLease, EpochToken, InterruptEpochGate
from .cache_provenance import CacheEntry, CacheNamespace, CacheProvenanceFirewall
from .multimodal_intent import IntentContract, IntentEquivalenceGate, IntentEquivalenceResult
from .completion_boundary import CompletionBoundaryGate, CompletionResult, StreamChunk
from .input_cohesion import InputCohesionGate, InputRequirement, InputResource, CohesionResult
from .coordinator import InteractionSnapshot, build_interaction_snapshot

__all__ = [
    "ActionLease",
    "CacheEntry",
    "CacheNamespace",
    "CacheProvenanceFirewall",
    "CompletionBoundaryGate",
    "CompletionResult",
    "CohesionResult",
    "EpochToken",
    "GateDecision",
    "GateStatus",
    "InputCohesionGate",
    "InputRequirement",
    "InputResource",
    "IntentContract",
    "IntentEquivalenceGate",
    "IntentEquivalenceResult",
    "InteractionSnapshot",
    "InterruptEpochGate",
    "StreamChunk",
    "build_interaction_snapshot",
    "canonical_digest",
    "canonical_json",
]
