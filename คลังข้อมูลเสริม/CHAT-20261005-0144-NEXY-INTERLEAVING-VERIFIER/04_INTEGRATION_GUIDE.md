# Future NEXY Integration Guide

**Status: AI-PROPOSED ONLY. No NEXY integration is implemented or authorized by this lab.**

## Intended adapter boundary
A future adapter could translate a NEXY-side candidate action plan into the verifier DSL, execute this verifier in isolation, and return only the machine report to the authoritative judge/policy layer.

Conceptual flow:
`candidate plan -> authoritative adapter -> normalized verifier model -> interleaving report -> NEXY policy/judge decision`

The verifier must never become the owner of NEXY policy. It answers a narrow question: whether the supplied bounded deterministic model is schedule-confluent and invariant-preserving.

## Required promotion gates
Before any real integration:
1. Define which NEXY component owns action atomicity boundaries.
2. Define authoritative mapping from real operations to DSL effects/preconditions.
3. Prove adapters do not omit externally visible intermediate states.
4. Bind reports to exact source/plan identity.
5. Test against historical race/duplicate/idempotency failures.
6. Add integration evidence showing a FAIL/FREEZE cannot be bypassed by downstream routing.
7. Benchmark state-space growth on representative plans and define approved caps/partition strategy.
8. Define how real I/O, retries, timeouts, and idempotency are modeled. They are not represented by the current core DSL.

## Relationship to existing auxiliary work
- Side-Effect Transaction Lab: plans transactional safety and side-effect boundaries. This lab checks interleaving semantics of a supplied abstract action plan.
- Context Delta Lab: invalidates/replans evidence when context changes. This lab does not compare project snapshots.
- Resource Governor: allocates bounded AI execution resources. This lab's state/transition caps are proof-integrity limits, not AI model token/resource scheduling.
- NEXY concurrency model: documents concurrency invariants. This lab is executable bounded verification for specific abstract plans.

## Adapter rule
If an adapter cannot faithfully encode an operation without hidden state or timing, it must return `NOT_VERIFIED/FREEZE` rather than simplifying the model until it passes.
