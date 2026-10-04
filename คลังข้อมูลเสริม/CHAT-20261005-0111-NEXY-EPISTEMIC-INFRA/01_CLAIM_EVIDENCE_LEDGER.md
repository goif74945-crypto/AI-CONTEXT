# Claim / Evidence Ledger

## Purpose
Represent knowledge as auditable claims instead of unstructured prose.

## Claim record
Each claim SHOULD carry:
- claim_id: stable identifier
- proposition: atomic statement
- subject / predicate / object where applicable
- scope: domain, tenant, project, component
- valid_from / valid_until
- observed_at
- source_id[]
- evidence_type[]
- authority_tier
- confidence
- verification_state
- contradiction_ids[]
- supersedes[]
- derived_from[]
- transformation: extraction, calculation, inference, synthesis
- owner
- last_verified_at

## Verification states
VERIFIED: supported by adequate direct evidence.
PARTIALLY_VERIFIED: some components proven, remainder unresolved.
UNVERIFIED: claim exists but has not passed a verification gate.
CONTRADICTED: credible evidence conflicts with the proposition.
STALE: evidence may have been correct but freshness requirements expired.
UNKNOWN: system lacks enough evidence to form the claim.

## Authority ordering
Default ordering when user/project policy does not override:
1. explicit authoritative project specification
2. direct system state / primary artifact
3. official first-party documentation
4. reproducible measurement or test
5. high-quality secondary source
6. model inference

Authority is not truth by itself. A lower-tier direct measurement may invalidate an outdated higher-tier document if the task asks for current runtime state.

## Atomicity rule
Do not store compound claims when components can vary independently. Split “service is deployed, healthy, and secure” into separate deployment, health, and security claims.

## Evidence sufficiency
A claim is VERIFIED only when evidence establishes the proposition, identity, scope, and relevant time window. Presence of a file is not evidence that its contents are correct. A successful command is not evidence that the intended end state persisted unless state is re-read.

## Derived claims
For calculations or synthesis, store the input claim IDs and deterministic transformation. If any critical parent becomes stale or contradicted, derived claims must be invalidated or re-evaluated.

## NEXY use
This ledger can back retrieval ranking, answer citations, agent stop conditions, regression diagnosis, and “why do you believe this?” inspection.