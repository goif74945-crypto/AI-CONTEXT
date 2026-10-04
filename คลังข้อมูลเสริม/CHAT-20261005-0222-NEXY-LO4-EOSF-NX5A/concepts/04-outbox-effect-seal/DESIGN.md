# OES — Outbox Effect Seal

**Classification:** Lo4 AI proposal / non-Canon.

## Problem
A crash between state mutation and external side effect can cause either a missing effect or a duplicated retry. A generic “retry request” does not solve this.

## State model
`PREPARED -> COMMITTED -> EMITTED`, with `PREPARED -> CANCELLED` allowed before commit.

## Replay semantics
- exact same PREPARED/COMMITTED state resumes from that state;
- already EMITTED suppresses repeat emission;
- same effect ID with different exact payload seal freezes;
- CANCELLED identity cannot silently be resurrected;
- emission before COMMITTED is forbidden.

## Critical equality
Payload equality uses exact canonical structural seals. Compact non-cryptographic hashes are not authoritative.

## NEXY value
Provides a proposed transactional outbox protocol around mutating routes/queue workers while preserving fail-closed replay semantics.

## Promotion warning
Production requires a real database transaction/unique constraint and provider reconciliation. This local state machine alone cannot create exactly-once delivery.
