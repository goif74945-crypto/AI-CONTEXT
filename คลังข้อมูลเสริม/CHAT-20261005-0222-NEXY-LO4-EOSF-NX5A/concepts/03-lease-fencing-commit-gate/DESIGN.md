# LFCG — Lease Fencing Commit Gate

**Classification:** Lo4 AI proposal / non-Canon.

## Problem
A stale worker can continue running after its lease expires or is reassigned. Lease-holder identity alone cannot prevent that worker from committing late.

## Mechanism
Every lease acquisition advances a monotonically increasing `fence`. A commit is legal only when resource, holder, exact fence and validity sequence all match the current durable lease and the lease is not revoked.

## Fail-closed reasons
`WRONG_RESOURCE`, `REVOKED`, `WRONG_HOLDER`, `STALE_FENCE`, `FUTURE_FENCE`, `LEASE_EXPIRED`.

## Invariant
No worker holding a lower fence may commit after a newer lease exists.

## NEXY value
Provides an explicit distributed-worker safety primitive that complements queue idempotency and stale-job expiry.

## Promotion warning
An in-memory fence proves nothing in production. The fence must be persisted and enforced atomically at the actual commit point.
