# Proof-Carrying Execution
Status: **AI-PROPOSED CONCEPT — NOT IMPLEMENTED / NOT APPROVED**

A high-impact autonomous action is complete only when a proof bundle connects requirement, authorization, pre-state, intended delta, execution receipt, post-state, and independent verification.

## Bundle
task_id; objective_hash; requirement_ids; authority_refs; allowed/forbidden scope; resource revisions before/after; plan revision; actions + idempotency keys; receipts; checks; invariant results; limitations; certificate status.

## Invariants
PCE-01 COMPLETE requires post-state evidence.
PCE-02 Tool success alone is not post-state evidence.
PCE-03 Unresolved forbidden-target ambiguity blocks mutation.
PCE-04 Revision mismatch invalidates a prepared write until re-planned.
PCE-05 Missing critical evidence yields NOT VERIFIED.
PCE-06 Proof bundles never persist secret values.

## Protocol
PREPARE: resolve exact target, authority, revision, constraints, rollback class.
EXECUTE: smallest authorized mutation, record receipt.
PROVE: independent readback plus behavioral/invariant checks.

## Failure semantics
receipt exists + wrong state => FAILED.
timeout after possible write => read state before retry.
revision changed => CONCURRENT_CHANGE and re-plan.
verification unavailable => NOT VERIFIED.
invariant violated => FAILED plus containment.
