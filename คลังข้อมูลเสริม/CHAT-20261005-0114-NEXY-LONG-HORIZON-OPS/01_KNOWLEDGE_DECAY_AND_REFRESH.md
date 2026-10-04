# Knowledge Decay & Refresh Protocol

Status: PROPOSAL_AI

## Problem
Repository knowledge has a half-life. A statement can be true at commit A and false at commit B without the prose changing. Long-lived AI context therefore needs expiration semantics, not merely storage.

## Proposed record
Each durable operational claim may carry:
- claim_id
- claim_text
- authority_class
- source_identity
- observed_at
- source_revision
- volatility_class
- refresh_trigger
- invalidation_trigger
- supersedes / superseded_by
- verification_method
- state: CURRENT | STALE | INVALIDATED | UNKNOWN

## Volatility classes
V0 IMMUTABLE: mathematical or frozen protocol invariant.
V1 SLOW: architecture intended to change rarely.
V2 RELEASE: may change each release.
V3 RUNTIME: can change without source commit.
V4 EXTERNAL: controlled by provider/dependency/world state.

The higher the volatility, the less acceptable it is to reuse old evidence.

## Refresh triggers
PROPOSAL_AI:
1. referenced source revision changes;
2. dependency lockfile changes;
3. schema/migration changes;
4. deployment environment changes;
5. authoritative spec changes;
6. previously required verification gate changes;
7. elapsed age exceeds domain-specific TTL.

## Anti-patterns
- "Latest" documents with no source revision.
- Runtime claims inferred from repository text.
- Copying old PASS into a new commit.
- Treating a historical incident fix as proof that the class cannot recur.
- Keeping contradictory records without explicit supersession.

## Useful future mechanism
HYPOTHESIS: a Context Freshness Linter could scan context records, resolve source identities, and emit STALE/INVALIDATED rather than silently serving old facts.

## Acceptance experiment
Given claims bound to revision R1, mutate their referenced sources to R2. The linter should invalidate only affected claims, preserve independent claims, and produce machine-readable reasons.
