# Capacity & Cost Envelopes
Status: PROPOSAL_AI

Correctness under one request is not correctness under sustained load. Agentic workflows may also be economically unbounded.

## Envelope
Budget wall-clock time, retries, tool calls, external requests, bytes, context growth, queue contribution, concurrency, cost class, and side-effect count.

GREEN = within envelope. AMBER = degrade optional work. RED = stop expansion but preserve correctness. FREEZE = continuing risks integrity/authority.

## Degradation order
Remove cosmetic enrichment; reduce speculative breadth; reduce redundant retrieval; postpone advisory analytics; preserve authority resolution, validation, safety and evidence; never invent missing results.

## Amplifiers
Recursive delegation, non-idempotent retries, weakly bounded fan-out, re-verifying unchanged evidence, context duplication, over-polling, and expensive fallbacks.

## Experiment
Replay tasks at 1x, 10x and adversarial fan-out. Verify bounded retries, stable side effects, explicit exhaustion and no correctness downgrade.
