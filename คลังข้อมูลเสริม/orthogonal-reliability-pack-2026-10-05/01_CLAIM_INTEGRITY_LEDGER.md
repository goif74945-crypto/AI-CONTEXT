# Claim Integrity Ledger
## Objective
Prevent unsupported completion/correctness claims.

## Record schema
claim_id; atomic_statement; class={FACT,ASSUMPTION,UNKNOWN,NOT_VERIFIED}; source_type; source_locator; observed_at; freshness_policy; verification_method; verifier_result={PASS,FAIL,INCONCLUSIVE}; dependencies[]; invalidation_triggers[].

## Invariants
C1 FACT requires retraceable evidence.
C2 ASSUMPTION cannot satisfy acceptance criteria.
C3 UNKNOWN remains UNKNOWN until evidence changes it.
C4 Critical FAIL or INCONCLUSIVE blocks global COMPLETE.
C5 Expired evidence must be revalidated.
C6 Agent prose cannot serve as evidence for its own claim.
C7 Existence of an artifact proves existence only, not semantic correctness.

## Contradiction protocol
Freeze affected claim; preserve all conflicting evidence; compare authority/freshness/scope; prefer direct verification where possible; otherwise mark NOT_VERIFIED.

## Evidence ladder
A direct execution/test result.
B authoritative project artifact.
C official external specification/documentation.
D independently verified external evidence.
E inference.
Critical acceptance should normally require A/B. E may guide next action but should not close a requirement.

## Completion predicate
COMPLETE only if all critical requirement nodes have fresh PASS evidence, no unresolved critical contradiction, and all required regression gates pass.
