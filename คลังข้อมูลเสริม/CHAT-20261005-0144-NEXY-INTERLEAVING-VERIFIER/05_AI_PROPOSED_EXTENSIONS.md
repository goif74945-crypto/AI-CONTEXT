# AI-Proposed Future Extensions

Everything here is a proposal, not current NEXY scope.

## P1 — Partial Order Reduction by Independence Proof
Current state merging is exact but still explores every distinct `(done,state)` pair. A future reducer could identify proven-independent actions and prune equivalent transition orders before execution.

Promotion requirement: formal equivalence tests against exhaustive enumeration; any uncertain independence must remain unpruned.

## P2 — Bounded Retry / Idempotency Automata
Model retryable actions as explicit finite automata with idempotency keys and duplicate-delivery transitions.

Promotion requirement: keep retries bounded; never map generic retry semantics onto physical/destructive effects without domain authority.

## P3 — Multi-object OCC Model
Add declarative revision/compare-and-swap transitions for storage/Vault-style optimistic concurrency control.

Promotion requirement: exact stale-version and retry semantics must come from authoritative storage contracts.

## P4 — Temporal Invariants
Support bounded temporal properties such as “once FREEZE occurs, no mutation transition is reachable afterward.”

Promotion requirement: explicit finite-trace semantics and independent oracle tests.

## P5 — Counterexample Minimizer
Given a failing plan, deterministically remove irrelevant actions/fields until a minimal divergence witness remains.

Promotion requirement: preserve failure class and prove minimized witness reproduces original counterexample.

## P6 — Real Trace Replay Adapter
Convert captured, provenance-bound execution traces into verifier fixtures for postmortem schedule analysis.

Promotion requirement: trace completeness and source identity must be proven; missing events must FREEZE analysis.
