# 08 — AI-Proposed Future Extensions

Everything in this file is **PROPOSAL / RESEARCH**, not NEXY law.

## A. Authority Lease Tokens
Issue short-lived, capability-bounded execution leases derived from a directive epoch. A worker can compute freely but mutation requires a still-current lease. Revocation is then an O(1) epoch/lease-generation change rather than per-job cancellation.

**Benefit:** faster cancellation propagation across large swarms.
**Risk:** clock-based expiry can reintroduce nondeterminism; prefer logical generations where possible.

## B. Epoch-Aware Queue Tombstones
When a directive is replaced/revoked, write a queue-level tombstone for the old epoch. Consumers reject jobs before expensive execution and again before mutation.

**Benefit:** saves compute and reduces stale side-effect attempts.
**Risk:** tombstone delivery lag; final commit gate remains mandatory.

## C. Supersession Impact Graph
Track which prepared actions, artifacts, evidence and queued jobs depend on each directive epoch. On supersession, produce a deterministic invalidation set.

**Benefit:** operator sees blast radius before/after changing a directive.
**Risk:** graph completeness becomes a correctness requirement.

## D. Two-Phase Intent Commit
For very high-impact tasks, separate `PREPARE_DIRECTIVE` and `ACTIVATE_DIRECTIVE`. Workers may precompute under a candidate directive but no mutation is allowed until activation.

**Benefit:** cheap speculative computation without accidental authority.
**Risk:** more control-plane complexity and storage.

## E. Cross-Agent Authority Watermark
Attach `(epoch, lineage_hash)` to every inter-agent message/result. A consumer rejects stale upstream results even before preparing an action.

**Benefit:** stale information dies earlier in a swarm.
**Risk:** should not turn presentation metadata into trusted authority; watermark must be injected/verified by the control plane.

## F. Supersession Race Fuzzer
Build a scheduler/fault-injection harness that interleaves:
- directive replacement;
- queue dequeue;
- worker completion;
- approval issuance;
- commit gate;
- executor dispatch;
- crash/restart.

The invariant is: **no side effect whose authority epoch is no longer current may become durable.**

This is the highest-value next verification step before real integration because deterministic unit tests do not prove transactional behavior across DB/queue boundaries.
