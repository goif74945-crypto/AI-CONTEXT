# Security Review

## Threat model
EOSF is intended to reduce duplicate or orphan external effects caused by retries, queue races, stale workers, crash recovery and cancellation. It is **not** an authentication system, cryptographic authorization service, distributed database, or provider transaction manager.

## Security-positive properties in the reference implementation
- strict TypeScript and fail-closed contract validation;
- canonical structural equality for critical mutation/effect identity;
- no lossy hash is used as the authoritative equality check;
- compact FNV-64 remains telemetry-only and is explicitly documented as non-security;
- no executable source imports filesystem, shell, network, HTTP, process environment or dynamic evaluation APIs;
- retry count/fanout analysis is bounded by an explicit analysis cap;
- graph cycles/unknown references/duplicates fail closed;
- stale/future/revoked/expired lease commits fail closed;
- emitted effects are suppressed on replay;
- registry/outbox contradictions freeze rather than guessing;
- materialized effects require compensation during cancellation regardless of terminal state.

## Important residual limitations
### 1. Canonical structural seal is not a storage index strategy
The prototype uses exact canonical strings for collision-free equality. Production may hash these for indexing, but authoritative comparison must use a cryptographically strong digest with collision policy or retain the canonical preimage.

### 2. Exactly-once is a protocol property, not a local function
Real exactly-once external side effects require durable atomic storage, uniqueness, crash recovery, fencing and provider behavior. This package only proves local protocol semantics.

### 3. Provider ambiguity remains real
A timeout after sending an external request can mean “not sent”, “sent but response lost”, or “provider still processing”. A future adapter must use provider idempotency/query/reconciliation. Blind retry is forbidden.

### 4. Compensation is not reversal
CCC proves that a compensation obligation exists; it does not prove the compensation semantically restores the world. That requires domain-specific evidence and may be impossible for irreversible effects.

### 5. Fence safety depends on durable monotonic storage
A number in memory does not fence anything. Promotion requires a durable compare-and-set/transaction boundary at the actual commit point.

### 6. Denial-of-service bounds
RAB has explicit graph/count caps, but production adapters still need payload size, node count and canonicalization limits.

## Static source audit
`evidence/static-io-audit.log` records a token-level check over executable TypeScript sources for obvious I/O/runtime escape imports/calls. This is supporting E1 evidence, not a formal sandbox proof.
