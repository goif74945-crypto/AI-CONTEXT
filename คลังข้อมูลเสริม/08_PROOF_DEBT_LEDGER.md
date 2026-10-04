# Proof Debt Ledger
Status: PROPOSAL / AI-PROPOSED CONCEPT
Authority: ADVISORY ONLY

Proof debt = gap between what the project claims/depends on and what admissible evidence currently demonstrates.

## Classes
PD1 CLAIM_WITHOUT_PROOF
PD2 PROOF_WITHOUT_SOURCE_BINDING
PD3 PROOF_WITHOUT_REQUIREMENT_BINDING
PD4 STALE_PROOF
PD5 PARTIAL_AS_COMPLETE
PD6 NON_REPRODUCIBLE_PROOF
PD7 UNVERIFIED_EXTERNAL_DEPENDENCY
PD8 MANUAL_ONLY_ASSERTION
PD9 NEGATIVE_REQUIREMENT_UNTESTED
PD10 RECOVERY_PATH_UNPROVEN
PD11 MIGRATION_INVARIANT_UNPROVEN
PD12 OBSERVABILITY_BLIND_SPOT

## Record
id; claim; requirement_ids; severity; blast_radius; evidence_required; evidence_present; source_identity; invalidators; first_seen; last_checked; status; blocking_release; remediation; verification_method.

## Priority
Do not collapse to one average. Rank by authority criticality, irreversible blast radius, harm potential, dependency fanout, uncertainty, and detectability. One critical unproven destructive-action invariant can dominate hundreds of proven low-risk claims.

## Interest
Debt compounds when downstream systems depend on an unproven claim, summaries copy it without provenance, tests encode assumptions, or generated context repeats it until it appears factual.

## Burn-down
enumerate claims -> map claim/requirement/evidence -> find missing edges -> rank -> create falsifiable test -> bind source/environment -> verify -> retain counterexample -> close only with evidence pointer.

## Anti-gaming
Never lower severity to green a dashboard, redefine a claim after failure, count prose as proof, count test existence as execution, treat historical evidence as current authorization, or average critical failures away.

## Invalidation
Closed debt is not permanently closed. Any dependency change can reopen it deterministically.

## Adoption criterion
Every closed item must expose independent evidence and every release-blocking item must be queryable without model interpretation.
