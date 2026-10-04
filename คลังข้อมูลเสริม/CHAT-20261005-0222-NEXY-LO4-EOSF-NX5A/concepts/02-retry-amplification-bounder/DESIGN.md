# RAB — Retry Amplification Bounder

**Classification:** Lo4 AI proposal / non-Canon.

## Problem
Nested retries + fanout can multiply external-effect attempts far beyond what a local `maxAttempts` value suggests.

## Model
Each bounded graph node declares `maxAttempts`, `fanOut`, `localEffectsPerAttempt`, `retryExplicitlySafe`, and child nodes.

For each node, RAB computes a worst-case recurrence:
`attempts(node) = maxAttempts * (localEffectsPerAttempt + fanOut * sum(attempts(child)))`.

## Invariants
- every multi-attempt node must explicitly declare safe retry;
- cycles and unknown children fail closed;
- bounded integer arithmetic uses BigInt internally;
- configurable analysis cap prevents combinatorial/count explosion;
- worst-case effect attempts must fit the caller's explicit budget.

## NEXY value
Turns DOC-C's “no automatic retry by default / retry only if explicitly safe” into a machine-checkable quantitative preflight.
