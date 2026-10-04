# Architecture — Runtime Failure Topology Mesh

Classification: **Lo4 AI proposal / experimental / non-governing.**

## Objective
Create a deterministic advisory layer for failures that are not well represented by a single exception or failed test: cyclic waiting, cyclic activity without progress, retry amplification, revision-scoped poison inputs, and useful verified work trapped behind a terminal failure.

## Composition

```text
runtime wait edges ───────────────▶ Deadlock Sentinel ─────────┐
ordered state/progress trace ─────▶ Livelock Detector ────────┤
attempt/failure history ──────────▶ Retry Storm Governor ─────┤
input+revision run history ───────▶ Poison Task Quarantine ───┤
result/evidence dependency DAG ───▶ Partial Salvage Compiler ─┤
                                                                ▼
                                                    advisory diagnostic bundle
                                                                │
                                                                ▼
                                                  future NEXY-owned adapter
                                                                │
                                                                ▼
                                                     NEXY CORE / JUDGE
```

## Global invariants
1. Diagnostics have no mutation authority.
2. Canonical fingerprints are content identities for deterministic comparison, not authentication signatures.
3. Identity-sensitive strings must be non-empty after trimming.
4. Order is normalized only where order is semantically irrelevant. Ordered runtime histories remain ordered.
5. Malformed histories fail explicitly rather than being repaired silently.
6. No module may infer idempotency, retryability, verification, evidence, or user-display safety from optimism.
7. Partial salvage cannot become whole-task completion.
8. Production library code performs no network/file/env/shell/database/model I/O.

## System 1 — Deadlock Sentinel
### Contract
Input is a set-like collection of `WaitEdge(waiter, holder, resource_id)` facts. Duplicate semantic edges are normalized away. The output contains canonical strongly connected wait components that are cyclic.

### Algorithm
The implementation uses iterative Kosaraju SCC traversal. Adjacency and reverse-adjacency maps are built in one edge pass, then traversed without Python recursion. Canonical sorting makes output independent of semantically irrelevant input ordering.

Expected structural cost is `O(V + E)` traversal plus sorting/canonicalization cost. The design avoids recursive DFS because a long acyclic chain is a valid runtime topology and must not crash the detector merely by being long.

### Semantics
- empty/acyclic topology -> `CLEAR`;
- SCC with >1 member -> `DEADLOCK`;
- self wait -> `DEADLOCK`;
- slowness without a cycle -> not deadlock.

## System 2 — Livelock / Thrash Detector
### Contract
Input is an ordered sequence of `ProgressSample(epoch, state_fingerprint, progress_counter, action_kind)` and a bounded trailing window.

### Semantics
- progress counter increases in current window -> `PROGRESSING`;
- no progress and no repeated multi-state suffix cycle -> `STALLED`;
- repeated multi-state/action suffix cycle with no progress -> `LIVELOCK`;
- any progress-counter regression in supplied history -> `FREEZE` because the progress history is internally inconsistent.

A transient prefix is allowed; an established repeated suffix still counts as livelock. Period-1 repetition is treated as idle/stall rather than livelock.

## System 3 — Retry Storm Governor
### Contract
Input is a contiguous ordered attempt history and an explicit retry policy.

### Invariants
- latest declared non-retryable failure stops;
- latest non-idempotent failure stops;
- a prior illegal retry cannot be laundered by later changing metadata to retryable/idempotent; such history becomes `FREEZE_INVALID_HISTORY`;
- same-signature storm threshold can quarantine before global max attempts;
- failure signature changes reset the trailing storm streak;
- backoff is deterministic bounded exponential delay.

The governor decides whether another retry is allowed. It does not execute it.

## System 4 — Poison Task Quarantine
### Contract
Input is an ordered history of runs carrying input fingerprint, executor revision, outcome, and failure signature.

### Semantics
Only a trailing sequence with the same `(input_fingerprint, executor_revision, failure_signature)` accumulates. A success, different failure signature, different input, or new executor revision breaks the poison streak. The quarantine key is content-derived from the exact triple.

This matters because fixing the executor revision must give the same input another chance; stale failures against an older revision must not condemn the new code indefinitely.

## System 5 — Verified Partial-Result Salvage Compiler
### Contract
Input is a DAG of result nodes. A node is salvageable only when:
- `status == PASS`;
- `verified == True`;
- at least one evidence ID exists;
- a payload identity exists;
- user-visible safety is explicitly true;
- every dependency is also salvageable.

Unknown dependency IDs and cycles fail closed. Independent verified branches can survive an unrelated failed branch.

### Authority boundary
The compiler has no authoritative task denominator, so `whole_task_complete` is structurally always false. Upstream closure logic remains responsible for completion. This prevents “all nodes I happened to receive passed” from becoming “the requested task is complete.”

## Future build order
A future NEXY integration should implement schema adapters before any runtime action mapping. The safe order is:
1. telemetry/event schemas;
2. deterministic adapters;
3. shadow diagnostics only;
4. replay corpus and false-positive measurement;
5. CORE/JUDGE-owned policy mapping;
6. operational fault/load testing;
7. only then consider release-blocking authority through explicit canonical promotion.
