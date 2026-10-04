# Design

Status: implemented as standalone reference code. Not integrated into NEXY.AI.

## Model

The planner consumes an ErasureRequest plus a DataGraph. Nodes represent canonical artifacts, blobs, derivatives, shared derivatives, caches, indexes, audit records and external exports. Directed edges encode containment, derivation, cache/index projection, audit linkage and exports.

The planner computes the reachable erasure closure, validates that closure, derives ordered actions, freezes on unsafe ambiguity, then hashes a canonical representation of the complete plan.

## Invariants

I-01 Determinism
The same semantic request and graph produce the same planHash and action sequence regardless of input node/edge order.

I-02 Fail closed
Any blocker yields status FREEZE and executionAuthorized=false.

I-03 Immutable provenance
AUDIT_LOG is never deleted. The only planned action is APPEND_AUDIT_TOMBSTONE.

I-04 No cross-principal destruction
Exclusive nodes owned by another principal produce CROSS_OWNER_MUTATION and freeze.

I-05 Shared-data safety
A SHARED_DERIVED node is rebuilt only when provenance identifies which reachable sources to remove and which unrelated sources to preserve. Missing or ambiguous provenance freezes.

I-06 Hold precedence
Active legalHold or retentionUntilTick above requestedAtTick replaces destructive mutation with RETAIN_UNDER_HOLD.

I-07 External truth boundary
External deletion is never inferred from local state. EXTERNAL_EXPORT requires REQUEST_EXTERNAL_ERASURE plus EXTERNAL_ERASURE_RECEIPT.

I-08 Evidence before completion
Receipt verification returns PASS only when every planned action has exactly one valid plan-bound receipt.

## Action semantics

REVOKE_ACCESS severs user-visible access without claiming physical destruction.
DESTROY_BLOB claims physical deletion and therefore requires BLOB_DESTRUCTION_RECEIPT.
DELETE_DERIVED removes an exclusively-owned derivative.
INVALIDATE_CACHE removes a cached projection.
REMOVE_INDEX_ENTRY removes discoverability/index state.
REBUILD_SHARED_DERIVED recomputes a shared derivative excluding erased sources while preserving unrelated sources.
APPEND_AUDIT_TOMBSTONE preserves history and records erasure without re-inserting erased content.
RETAIN_UNDER_HOLD records a justified temporary preservation obligation.
REQUEST_EXTERNAL_ERASURE delegates deletion to an identified external system and remains pending until evidence returns.

## Failure classes

TARGET_NOT_FOUND
TARGET_OWNER_MISMATCH
DUPLICATE_NODE_ID
DANGLING_EDGE
CROSS_OWNER_MUTATION
PROPAGATION_CYCLE
IMMUTABLE_MUTATION
MISSING_EXTERNAL_ADAPTER
SHARED_PROVENANCE_INCOMPLETE

Any one is sufficient to freeze the plan.

## Ordering rationale

Access revocation occurs before destructive content actions.
Retention decisions appear before destructive actions.
Blobs and derivatives are processed before cache/index cleanup.
External requests follow local projection cleanup.
Audit tombstones are ordered last as provenance evidence.

This ordering is advisory for an executor. A production executor would still require transactional/idempotent adapters and durable per-action receipts.

## Security notes

Tombstones must not contain plaintext erased content.
Evidence hashes prove receipt identity, not deletion by themselves; the adapter producing the receipt must itself be trusted and verifiable.
planHash prevents stale receipts from satisfying a changed plan.
Duplicate receipts fail verification instead of being accepted by majority.
Cycles and missing provenance are treated as unsafe ambiguity, not opportunities for guessing.
