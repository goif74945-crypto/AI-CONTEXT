"""Standalone proposal prototypes for deterministic NEXY-compatible assurance research."""

from .metamorphic import (
    MetamorphicRelation,
    MetamorphicResult,
    RelationDefinitionError,
    verify_relation,
)
from .conservation import (
    ConservationRule,
    ConservationResult,
    ConservationError,
    verify_transition,
    verify_sequence,
)
from .witness import (
    EvidenceItem,
    WitnessResult,
    WitnessError,
    extract_minimal_witness,
)
from .fingerprint import (
    ScenarioRecord,
    BehaviorFingerprint,
    BehaviorDiff,
    FingerprintError,
    build_fingerprint,
    diff_fingerprints,
)
from .spec_mutation import (
    Constraint,
    ConstraintOp,
    MutationCase,
    MutationReport,
    SpecMutationError,
    validate_spec,
    generate_illegal_mutations,
    run_mutation_sentinel,
)

__all__ = [name for name in globals() if not name.startswith("_")]
