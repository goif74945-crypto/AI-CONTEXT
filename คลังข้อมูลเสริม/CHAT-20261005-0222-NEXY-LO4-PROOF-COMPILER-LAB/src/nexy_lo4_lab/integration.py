from __future__ import annotations

from dataclasses import dataclass

from .authority import AuthorityClaim, AuthorityLevel, AuthorityProvenanceSeal
from .output_compiler import (
    ClaimArtifact,
    CompileResult,
    EvidenceRecord,
    ProofCarryingOutputCompiler,
)
from .planner import ClaimRequirement, MinimumProofPlanner, Probe
from .uncertainty import ClaimNode, EpistemicStatus, UncertaintyContainmentLattice
from .witness import RequirementBoundaryWitnessEngine, RequirementSpec


@dataclass(frozen=True)
class IntegrationResult:
    authority_digest: str
    proof_probe_ids: tuple[str, ...]
    witness_kinds: tuple[str, ...]
    compile_result: CompileResult


def run_reference_pipeline() -> IntegrationResult:
    """Run a deterministic happy-path composition of all five Lo4 proposals."""
    authority = AuthorityProvenanceSeal(
        {"current-user-directive": AuthorityLevel.USER_DIRECTIVE}
    ).seal(
        [
            AuthorityClaim(
                claim_id="user-law",
                statement="Only verified output may be released.",
                level=AuthorityLevel.USER_DIRECTIVE,
                source_ref="current-user-directive",
            ),
            AuthorityClaim(
                claim_id="build-rule",
                statement="Release claim requires E2 proof.",
                level=AuthorityLevel.CURRENT_SPEC,
                source_ref="proposal-test-contract",
                parent_claim_id="user-law",
            ),
        ],
        target_claim_id="build-rule",
    )

    states = UncertaintyContainmentLattice().evaluate(
        [ClaimNode("release-claim", EpistemicStatus.PASS)]
    )

    plan = MinimumProofPlanner().plan(
        [ClaimRequirement("release-claim", 2)],
        [
            Probe("static-check", cost=1, evidence_class=1, covers=frozenset({"release-claim"})),
            Probe("unit-check", cost=3, evidence_class=2, covers=frozenset({"release-claim"})),
        ],
    )

    witnesses = RequirementBoundaryWitnessEngine().generate(
        RequirementSpec(
            requirement_id="attempt-limit",
            field="attempts",
            operator="max",
            value=5,
            required=True,
        )
    )

    compiled = ProofCarryingOutputCompiler().compile(
        [
            ClaimArtifact(
                claim_id="release-claim",
                text="Reference pipeline claim is verified at E2.",
                authority_digest=authority.digest,
                uncertainty_status=states["release-claim"].effective_status,
                target_version="local-reference-v1",
                evidence_class_required=2,
                evidence_refs=("unit-check",),
            )
        ],
        trusted_authority_digests=frozenset({authority.digest}),
        evidence_catalog=(
            EvidenceRecord(
                evidence_ref="unit-check",
                claim_id="release-claim",
                evidence_class=2,
                passed=True,
                target_version="local-reference-v1",
            ),
        ),
    )

    return IntegrationResult(
        authority_digest=authority.digest,
        proof_probe_ids=plan.selected_probe_ids,
        witness_kinds=tuple(w.kind for w in witnesses),
        compile_result=compiled,
    )
