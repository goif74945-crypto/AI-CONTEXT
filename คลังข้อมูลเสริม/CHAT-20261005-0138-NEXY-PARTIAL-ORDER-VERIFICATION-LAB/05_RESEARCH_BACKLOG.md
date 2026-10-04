# NPOVL Research Backlog

All entries are **AI_PROPOSED / NOT_CURRENT_NEXY_REQUIREMENT** unless later adopted by authoritative specification.

## R1 — Persistent/source sets

Current v1 uses sleep-set reduction and can still traverse many nonterminal prefixes. Investigate persistent sets or source sets to reduce POR search-node overhead while preserving the same fail-closed input contract.

Acceptance idea: domain corpus shows strictly no class loss against exact oracle, and node count is never worse than v1 above an agreed tolerance.

## R2 — Optimal / quasi-optimal exploration

Research wakeup-tree, alternative-based, or quasi-optimal POR. The literature warns that optimal-alternative computation can itself be hard, so any upgrade needs explicit complexity budgets rather than a magical “optimal=true” flag.

## R3 — Dynamic independence

Model state-dependent conflicts discovered during execution. This would move the system toward DPOR and materially increase trust requirements because independence would depend on runtime observations.

## R4 — Repeated actions and loops

Current action IDs occur once. Define event-instance identity, loop bounds and retry semantics without accidentally equating two distinct side effects.

## R5 — Hierarchical resources

Support structured resource identities such as object/field/path ranges. Must prove alias conservatism. Prefix matching alone is insufficient for arbitrary systems.

## R6 — Tool side-effect descriptors

Define signed/versioned effect descriptors for tools so `effects_complete` is evidence-backed rather than a caller assertion.

## R7 — Property-level proof

Replace the boolean trace-invariance attestation with a checkable property contract for supported assertion classes. Unsafe property types should automatically disable reduction.

## R8 — Counterexample minimization

When a representative fails, minimize the dependent-order witness and connect it to the causal-debugging/evidence systems already present in AI-CONTEXT without merging their authority domains.

## R9 — Incremental recomputation

When one action/effect changes, reuse unaffected independence and class computations while invalidating all derived plan evidence that depends on the changed contract.

## R10 — Cross-implementation differential test

Compare the Python reference kernel with an independently implemented Rust or formal model version. Shared test fixtures alone are insufficient if both implementations share the same algorithmic bug.

## R11 — Formalization

Encode v1 semantics in TLA+, Alloy, Lean, Isabelle, or another formal system. Target theorem: under explicit v1 assumptions, every legal static trace class has at least one emitted representative unless the algorithm returns BLOCKED.

## R12 — Domain benchmark

Build a sanitized corpus from actual verification DAG shapes, without copying secrets or runtime-private state. Measure full-order count, class count, POR nodes, evidence size, and wall time separately.
