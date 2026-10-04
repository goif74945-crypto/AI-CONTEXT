# Evidence Ledger Schema

## Goal
Prevent confident-but-unverified engineering decisions.

## Canonical record
Each important assertion carries: claim_id, claim, classification (FACT | ASSUMPTION | UNKNOWN | NOT_VERIFIED), authority_level, source_locator, observed_at, freshness_policy, scope, dependencies, contradiction_set, verification_method, and verification_result.

Authority order: user specification > project files > official documentation > direct tool result > verified external source > inference.

## Conflict resolution
Higher authority wins only when it addresses the same claim and scope. Newer is not automatically better. If authoritative sources conflict, mark CONFLICT and freeze dependent destructive work.

## Freshness classes
- immutable: hashes and historical decisions
- release-bound: APIs, schemas, dependency behavior
- runtime: deployment state, health, feature flags
- volatile: availability and external service state

## Evidence debt
Any decision depending on NOT_VERIFIED creates evidence debt. Track impact, deadline, safe fallback, and verification owner.

## Anti-patterns
Never use an AI summary as primary evidence. Never infer runtime success from static code. Never infer compatibility from version numbers alone. Absence of evidence is not evidence of absence.
