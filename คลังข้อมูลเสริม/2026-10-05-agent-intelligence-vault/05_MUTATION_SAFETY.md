# Mutation Safety Layer
Every write operation should have: target identity, authority, fresh precondition, intended delta, blast radius, reversibility class, idempotency behavior, expected postcondition, readback method.
Mutation states: PROPOSED, AUTHORIZED, APPLIED_UNVERIFIED, VERIFIED, PARTIAL, ROLLED_BACK, FAILED.
For multi-write workflows, assume non-atomicity unless the underlying system guarantees transactions.
On partial failure: freeze new writes, inventory successful mutations, compare intended transaction, roll forward or rollback using the smallest safe action, then verify.
