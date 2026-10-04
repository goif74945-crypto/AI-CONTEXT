# Design — Schema Migration Witness (SMW)

**Classification:** AI-PROPOSED CONCEPT / ADVISORY ONLY

## Objective
Detect silent data loss before a schema/state migration is accepted. The engine applies a deterministic forward migration and a reverse migration to an explicit witness corpus, then compares canonical before/after state.

## NEXY value
Vault structures, persisted task state, policy records, execution capsules, and API contracts may evolve. A migration that compiles is not necessarily reversible or meaning-preserving. SMW creates a compact proof obligation: if the migration cannot reconstruct known valid state, it must not be labeled lossless.

## Core contract
- Input: records + ordered forward operations + ordered reverse operations.
- Supported operations: `rename`, `drop`, `add_default`, `copy`, restricted `cast`.
- Unknown operation: hard `ValueError`.
- Input mutation: forbidden; records are deep-copied.
- Empty witness corpus: `NOT_VERIFIED`, never PASS.
- Output: deterministic report containing status, witness count, forward outputs, and exact mismatches.

## Failure semantics
- Rename/copy collision without explicit overwrite -> fail closed.
- Unsupported cast -> fail closed.
- Lossy round trip -> FAIL with mismatch evidence.
- No witness corpus -> NOT_VERIFIED.

## Complexity
For `n` records and `m` migration steps, execution is O(n*m) plus canonical serialization cost. No network, filesystem, clock, random, or hidden I/O exists in the core.

## Future NEXY integration boundary
Wrap the pure engine behind a migration-admission adapter. NEXY may supply schema-derived witness records and promote a migration only after SMW plus domain-specific invariant tests pass. This document does not authorize such integration.
