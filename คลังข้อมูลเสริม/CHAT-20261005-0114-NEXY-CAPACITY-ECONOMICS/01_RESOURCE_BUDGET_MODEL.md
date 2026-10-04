# Resource Budget Model

> Classification: AI_PROPOSAL / engineering reference. Not a statement of current NEXY.AI behavior.

## Problem
Agent systems often optimize answer quality while treating compute, tokens, tool calls, wall-clock time, external API quotas, and human attention as invisible. That works until concurrency rises and the system discovers physics, billing, and rate limits simultaneously.

## Budget vector
Represent each task T with a budget vector:

B(T) = <tokens_in, tokens_out, tool_calls, tool_latency_ms, model_latency_ms, monetary_cost, concurrency_slots, external_quota, evidence_cost, human_interruptions>

A task is admissible only when its predicted consumption fits hard constraints or an authorized degradation policy exists.

## Hard vs soft budgets
Hard budgets MUST NOT be exceeded silently:
- security boundaries;
- external provider quotas that would cause failure;
- explicit user cost ceilings;
- irreversible action limits;
- maximum allowed concurrency for protected resources.

Soft budgets MAY be traded:
- latency target;
- token target;
- number of evidence sources;
- search breadth;
- retry count.

## Budget lifecycle
1. ESTIMATE: predict demand with uncertainty interval.
2. RESERVE: reserve scarce resources before irreversible or expensive work.
3. EXECUTE: debit actual consumption.
4. RECONCILE: compare prediction with actual.
5. LEARN: update estimator.
6. RELEASE: return unused reservation.

## Estimation
For resource r:
predicted_r = baseline(task_class,r) × complexity_factor × evidence_factor × uncertainty_multiplier.

Store p50 and p95 rather than a single number. A point estimate encourages false precision.

## Evidence budget
Verification itself consumes resources. Define:
total_cost = execution_cost + verification_cost + recovery_reserve.

Never spend the entire budget on generation and leave zero capacity to prove the result.

## Retry budget
Retries are bounded by:
- maximum attempts;
- maximum cumulative cost;
- maximum elapsed time;
- repeated-failure signature.

If the same normalized failure repeats without new evidence, retrying is prohibited. Escalate or change strategy.

## Resource debt
Resource debt is work deferred by a degraded execution path. Examples: skipped optional enrichment, reduced search breadth, deferred recomputation. Debt must be explicit and must never include skipped mandatory verification.

## Suggested telemetry
task_class, predicted_budget, reserved_budget, actual_budget, budget_variance, degradation_level, retry_count, evidence_spend, completion_status.

## Acceptance properties
- No mandatory evidence is removed merely to meet a soft latency target.
- Hard budget breach produces explicit BLOCKED/PARTIAL, not fabricated COMPLETE.
- Estimation error is observable.
- Resource accounting is attributable per task and per dependency.
