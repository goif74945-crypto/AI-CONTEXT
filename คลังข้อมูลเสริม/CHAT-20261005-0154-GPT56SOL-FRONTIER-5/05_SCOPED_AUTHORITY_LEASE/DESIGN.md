# Scoped Authority Lease Engine (SALE) — Design

## Problem
A user may want an agent to act autonomously for a bounded task, but broad standing authority is dangerous and hard to audit.

## Objective
Represent delegated authority as a short-lived lease constrained by subject, capability, resource patterns, action set, usage cap and parent delegation bounds.

## Invariants
- A lease cannot authorize outside its own scope.
- A child lease cannot expand parent capability/action/resource/expiry/max-use bounds.
- Revoked or expired lease freezes.
- Exhausted lease freezes.
- Lease IDs are content hashes for lineage only, not cryptographic signatures.

## Production caveat
The reference engine evaluates policy but does not authenticate issuance. Production use would require signed receipts/identity binding and secure revocation storage.
