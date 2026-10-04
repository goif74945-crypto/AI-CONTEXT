# Evaluation Plan
> Classification: AI-PROPOSED CONCEPT.

## Acceptance tests for a future implementation
T1 Expired critical evidence blocks execution.
T2 Updating an upstream HARD dependency marks all critical descendants for review.
T3 A SOFT dependency does not cause unnecessary global invalidation.
T4 A temporal contradiction can preserve both claims with disjoint validity windows.
T5 Missing provenance cannot silently become VERIFIED.
T6 Archived artifacts remain auditable after invalidation.
T7 Refresh priority favors one high-impact volatile claim over many low-impact static notes.
T8 Cyclic dependencies terminate safely and are reported.
T9 A source disappearing does not erase previously captured evidence metadata.
T10 Revalidation creates a new verification event rather than rewriting history.

## Adversarial cases
Clock skew; future timestamps; malformed TTL; duplicated evidence; source URL reused for changed content; contradictory authoritative sources; recursive dependency cycles; fan-out explosion; partial graph corruption; unavailable verifier.

## Required evidence for declaring implementation complete
- machine-readable test results
- fixtures for each failure case
- before/after graph snapshots
- deterministic invalidation traces
- no unresolved P0/P1 correctness failures
