# Design — NEXY Epistemic Integrity Quintet

**Classification:** AI-PROPOSED / Lo4 / EXPERIMENTAL / NOT CANON

This pack targets a different assurance layer from recent supplemental work on provenance caches, model drift, authority leases, effect transactions, evidence selection, context taint, recovery equivalence, observability, counterfactual testing and similar surfaces: **whether the reasoning/policy substrate is epistemically well-founded before a verifier or judge consumes it.**

## 1. ECOF — Epistemic Circularity Firewall
Detects self-supporting claim graphs. Inputs use mandatory `c:<claim>` and `e:<evidence>` dependencies. Tarjan SCC detection blocks self-loops and multi-claim cycles; a fixed-point pass computes grounded claims. Unknown dependencies freeze.

**Invariant:** a claim never becomes grounded merely because a circular group also cites some external evidence.

## 2. DMAG — Decision Monotonicity Auditor
Verifies authority-declared monotonic laws such as “higher risk must never improve the verdict.” The caller supplies dimension semantics and explicit verdict order; DMAG does not author policy. It rejects duplicate observation IDs and non-finite numeric coordinates, detects same-coordinate verdict conflicts, and checks ordered pairs.

**Invariant:** verification of supplied policy order, never invention of policy order.

## 3. PDZA — Policy Dead-Zone Analyzer
Exactly enumerates explicit finite policy domains under a hard budget and classifies rules as:
- unreachable: never matches;
- shadowed: matches but is never selected;
- redundant: removal changes no decision;
- live: selected and behaviorally relevant.

Tie-breaking is deterministic by `(-priority, rule_id)`.

**Invariant:** when exhaustive enumeration exceeds budget, return `FREEZE / COMBINATION_BUDGET_EXCEEDED`; never sample and call it exhaustive.

## 4. RKM — Refutation Knowledge Memory
Stores reusable negative knowledge with exact hypothesis scope, premise digest, authority epoch, counterexample, evidence IDs, expiry and revocation state.

**Invariant:** scope drift, premise drift, authority drift or staleness produces an explicit MISS rather than generalized reuse.

## 5. ACE — Assumption Closure Engine
Traverses `fact:`, `assume:`, `unknown:` and `claim:` dependencies and exposes all transitive assumptions/unknowns behind target claims. Cycles remain unresolved blockers.

**Invariant:** assumptions and unknowns are never silently promoted to facts.

## Advisory composition
`AdvisoryIntegrityGate` combines the five outputs into only `READY` or `FREEZE`. READY means only “no configured blocker in supplied advisory checks.” It is not legal execution authority, NEXY::JUDGE approval, Canon promotion, runtime proof or deployment proof.

## Trust boundary
Core implementation performs no network calls, subprocess execution, filesystem I/O, randomness, environment reads or implicit clock reads. Freshness time is an explicit RKM input.

## Complexity
- ECOF: SCC O(V+E), plus straightforward grounding loop.
- DMAG: O(n²).
- PDZA: bounded exhaustive finite-state analysis, roughly O(S×R²) in this reference implementation.
- RKM: linear in entries under one hypothesis.
- ACE: memoized graph traversal, approximately O(V+E) for acyclic regions.
