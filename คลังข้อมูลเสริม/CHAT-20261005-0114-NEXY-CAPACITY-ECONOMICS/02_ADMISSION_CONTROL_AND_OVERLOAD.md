# Admission Control and Overload Semantics

> Classification: AI_PROPOSAL.

## Objective
Prevent a high-capability agent system from becoming less reliable under load.

## Core invariant
Overload must reduce optional work before it reduces correctness.

## Admission decision
For incoming task T evaluate:
- priority class;
- deadline;
- predicted resource vector;
- dependency health;
- evidence requirements;
- queue age;
- reversibility;
- user-visible criticality.

Decision ∈ {ADMIT, QUEUE, DEGRADE_OPTIONAL, SHED, BLOCK}.

## Priority classes
P0: safety/integrity/recovery.
P1: active user mutation with bounded deadline.
P2: interactive read/research.
P3: background enrichment.
P4: speculative precomputation.

Lower priority must not starve indefinitely. Apply aging, but never let aging bypass safety constraints.

## Degradation ladder
D0 FULL: normal execution.
D1 COMPACT: reduce optional prose and duplicate retrieval.
D2 NARROW: reduce optional search breadth while preserving required evidence.
D3 DEFER: defer nonessential enrichment.
D4 READ_ONLY: prohibit optional mutations if dependency health is uncertain.
D5 SHED: reject low-priority work with explicit reason.

Forbidden degradation:
- inventing missing evidence;
- skipping required validation;
- weakening authorization checks;
- converting UNKNOWN to FACT;
- hiding partial completion.

## Backpressure
Each dependency exposes health:
HEALTHY, SATURATED, RATE_LIMITED, DEGRADED, UNAVAILABLE, UNKNOWN.

Upstream planners must react before cascading failure. Queue length alone is insufficient; use queue age, service time, retry rate, and dependency saturation.

## Circuit breaker
Open when a dependency shows a statistically meaningful failure burst. While open:
- fail fast for operations that require it;
- use a verified alternative only if semantics match;
- periodically probe recovery;
- never silently substitute a weaker source for an authoritative one.

## Fairness
Use weighted fair queuing across users/task classes. Add per-tenant burst caps to prevent one large research job from monopolizing scarce tools.

## Load-shedding evidence
Every shed/block event should record:
task id, class, reason, limiting resource, retry guidance, whether user-visible, and whether any mutation occurred.

## Chaos cases
- 10x request spike.
- provider latency increases 20x.
- rate limit drops unexpectedly.
- one tool returns fast but stale data.
- retry storm from a shared downstream failure.
- large task holds reservations and stalls.
- background jobs consume all evidence quota.

Expected outcome: critical integrity work remains available; optional work degrades first.
