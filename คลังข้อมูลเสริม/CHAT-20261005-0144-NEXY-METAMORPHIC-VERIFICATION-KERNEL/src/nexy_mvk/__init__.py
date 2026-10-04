"""NEXY Metamorphic Verification Kernel.

This package is standalone and integration-ready. It does not import or mutate
NEXY.AI. Integrators provide an adapter implementing :class:`SystemAdapter`.
"""

from .engine import VerificationEngine
from .model import (
    Case,
    Observation,
    OracleResult,
    RelationResult,
    RelationStatus,
    VerificationReport,
)
from .relations import (
    deterministic_replay,
    evidence_removal_safety,
    irrelevant_context_invariance,
    permission_reduction_monotonicity,
    semantic_variant_invariance,
)

__all__ = [
    "Case",
    "Observation",
    "OracleResult",
    "RelationResult",
    "RelationStatus",
    "VerificationReport",
    "VerificationEngine",
    "deterministic_replay",
    "evidence_removal_safety",
    "irrelevant_context_invariance",
    "permission_reduction_monotonicity",
    "semantic_variant_invariance",
]
