# NEXY Companion Adaptive Fabric (NCAF) v0.1

**Classification: AI_PROPOSED_CONCEPT_NOT_ADOPTED**

NCAF is a reference lab of five companion mechanisms. It is intentionally **not** a replacement for NEXY.AI canonical reasoning, consensus, evidence, risk, state, safety, or release logic. Each module is deterministic, bounded, independently testable, and wrapped as `ADVISORY_ONLY` before any future integration experiment.

## Design goals
- Improve efficiency or resilience around NEXY-adjacent workflows without minting new canonical authority.
- Keep hard boundaries explicit and machine-checkable.
- Prefer integer arithmetic and deterministic ordering.
- Fail closed on invalid contracts or unsatisfied hard constraints.
- Remain standard-library-only in this lab to minimize supply-chain surface.

## Concept 1 — Context Budget Allocator (CBA)
### Problem
Bounded context windows make naive “last N messages” retention cheap but semantically lossy. Important specification dependencies can be omitted while low-value recent history survives.
### Design
`ContextBudgetAllocator` selects a deterministic dependency-closed set of context items under a hard token budget. Mandatory items and their dependency closure are loaded first. Optional bundles are ranked by integer utility/freshness density.
### Invariants
- Selected tokens never exceed budget.
- Every selected item's dependencies are selected.
- Mandatory closure overflow fails closed.
- Dependency cycles are invalid.
- Identical input produces identical selection.
### Future NEXY value
Potentially useful as an **advisory pre-selector** for presentation/session context or offline context preparation. It must not silently replace canonical CIRL interpretation or infer user intent.

## Concept 2 — Evidence Conflict Resolver (ECR)
### Problem
External evidence bundles can contain mutually incompatible claims. Picking the highest-confidence single source hides disagreement.
### Design
Aggregate claims by exact value, score by bounded trust + evidence count, and emit `RESOLVED`, `CONFLICT`, or `INSUFFICIENT`. Close competing scores freeze the value instead of guessing.
### Invariants
- Mixed claim keys are rejected.
- Low evidence never becomes a resolved fact.
- Close disagreement emits no winning value.
- A resolved value must have the maximum aggregate score.
### Future NEXY value
Useful only as an **external evidence intake advisory** that can flag contradictions before canonical NEXY evidence processing. It may not replace Lo3/Lo2 conflict resolution or release evidence law.

## Concept 3 — Pareto Route Planner (PRP)
### Problem
Provider/tool scheduling often collapses quality, latency, cost, capability, and risk into one opaque heuristic.
### Design
Apply hard capability/quality/risk constraints first; remove dominated candidates; then use a deterministic integer tie-break only inside the Pareto frontier.
### Invariants
- No route outside hard constraints can be selected.
- Selected route is never Pareto-dominated by another eligible route.
- Duplicate route IDs are invalid.
- No eligible route fails closed.
### Future NEXY value
Potential scheduler for **non-authoritative provider/tool selection** where canonical law permits multiple equivalent execution providers. It must never select between competing truth outputs or override canonical deterministic choice.

## Concept 4 — Resumable Execution Journal (REJ)
### Problem
Long external operations need restart-safe progress without replaying already-completed side effects.
### Design
An append-only event journal validates per-step transitions, binds idempotency keys, and hash-chains records. It exposes unfinished steps for safe resume.
### Invariants
- Event sequence and previous hash must match.
- Tampering invalidates replay.
- Illegal transitions are rejected without mutation.
- Idempotency keys cannot cross step identity.
### Future NEXY value
A **companion checkpoint format for external/non-canonical jobs only**. It is explicitly not USL, not canonical execution state, and not evidence of NEXY state transition.

## Concept 5 — Failure Containment Engine (FCE)
### Problem
Repeated failure of a non-authoritative external dependency can amplify load and cascade into unrelated work.
### Design
Deterministic per-dependency circuit breaker using logical ticks. Closed dependencies permit attempts; threshold failure opens the circuit; cooldown permits one probe; successful probe closes, failed probe reopens.
### Invariants
- Open circuit blocks calls before cooldown.
- Half-open permits only one probe.
- Failed probe returns to open.
- Success fully resets failure state.
### Future NEXY value
Infrastructure/presentation/provider containment where retries are explicitly allowed. **Forbidden** for canonical components whose law requires immediate FREEZE/no retry.

## Shared advisory envelope
Every future adapter should wrap NCAF output with:
- `classification = AI_PROPOSED_CONCEPT_NOT_ADOPTED`
- `authority = ADVISORY_ONLY`
- `may_mutate_core = false`
- deterministic payload hash

This prevents a lab result from accidentally masquerading as canonical authorization.

## Build order
1. deterministic common canonicalization;
2. individual modules;
3. advisory integration boundary;
4. unit negative paths;
5. seeded randomized invariant tests;
6. cross-module smoke test;
7. compatibility audit;
8. evidence and durable handoff.
