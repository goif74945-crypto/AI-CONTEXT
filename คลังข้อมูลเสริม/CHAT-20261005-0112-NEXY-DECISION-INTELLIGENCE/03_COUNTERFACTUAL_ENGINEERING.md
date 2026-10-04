# Counterfactual Engineering

## Goal
Predict consequences before mutation and make predictions falsifiable.

For proposed change C ask: what exists without C; what state delta C creates; which contracts observe it; which failures become newly possible; which remain regardless; and what observation would prove the prediction wrong.

## Counterfactual graph
CAUSE -> STATE DELTA -> OBSERVER -> BEHAVIOR DELTA -> IMPACT

Every edge is FACT, INFERENCE, ASSUMPTION, or UNKNOWN. UNKNOWN never silently becomes deterministic.

## Change shadow
Inspect call/import graph, producers/consumers, schemas, caches, permissions, queues/events, deployment configuration, observability, tests, and durable context that may become stale.

## Negative-space analysis
Search explicitly for missing timeout, fallback, idempotency, rollback, provenance, version negotiation, cancellation and partial-failure semantics.

## Pre-mortem
Assume failure. Classify explanations as plausible+detectable, plausible+poorly-detectable, implausible, or UNKNOWN. Prioritize plausible+poorly-detectable cases for instrumentation and tests.

## Falsification contract
Before execution state at least one observation that would invalidate the plan. A plan that cannot be falsified is too vague to verify.
