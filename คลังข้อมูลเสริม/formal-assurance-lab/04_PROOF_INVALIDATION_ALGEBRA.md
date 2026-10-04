# Proof Invalidation Algebra

Status: PROPOSAL

## Goal
Determine whether an existing proof remains valid after project change.

## Proof object
P = {claim_id, claim_type, target_identity, requirement_identity, source_dependencies, toolchain_dependencies, environment_dependencies, input_dependencies, verifier_identity, evidence_class, artifact_hashes, result}

## Dependency closure
deps(P) = transitive set of identities whose values can affect the truth of claim(P).
A proof is reusable only if every semantically relevant dependency remains equivalent under the claim contract.

## Invalidation function
INVALID(P, Δ) is true if change set Δ intersects deps(P) with a change class that can affect the claim.

Not every file change invalidates every proof.
Not every unchanged file preserves proof.

## Invalidation classes
PI01 TARGET_SOURCE_CHANGED
PI02 GOVERNING_REQUIREMENT_CHANGED
PI03 DEPENDENCY_BEHAVIOR_CHANGED
PI04 TOOLCHAIN_CHANGED
PI05 ENVIRONMENT_CHANGED
PI06 INPUT_FIXTURE_CHANGED
PI07 VERIFIER_CHANGED
PI08 EVIDENCE_POLICY_CHANGED
PI09 SECURITY_BOUNDARY_CHANGED
PI10 UNKNOWN_DEPENDENCY_CHANGED

## Conservative rule
If dependency relevance is UNKNOWN for a mandatory release claim, do not reuse proof. Mark NOT_VERIFIED until regenerated.

## Equivalence
Hash equality is sufficient for byte identity, not semantic equivalence.
Semantic equivalence may permit proof reuse only when the claim contract explicitly allows it and equivalence itself is proven.

## Proof monotonicity warning
Adding a new mandatory requirement can invalidate release closure even when all old proofs remain individually valid.

## Closure equation
ReleaseClosure(R,E) = every mandatory obligation r in R has at least one valid matching proof e in E AND no unresolved P0 conflict exists.

If R changes, recompute obligation set before reusing E.

## Counterfactual tests
- change README only: unit proof may remain valid if README is outside dependency closure.
- change compiler version: static proof may invalidate even with identical source.
- change auth TTL requirement: auth behavior proof invalidates if claim covers TTL.
- add deployment requirement: implementation tests remain valid but release closure becomes false until deployment proof exists.
- change evidence verifier: seals may require re-verification.

## Desired future output
KEEP / INVALIDATE / REVIEW / UNKNOWN per proof, with exact dependency path explaining the result.
