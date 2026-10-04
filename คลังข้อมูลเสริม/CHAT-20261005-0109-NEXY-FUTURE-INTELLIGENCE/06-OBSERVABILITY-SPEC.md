# Autonomous Execution Observability Spec

Objective: make failures diagnosable without recording hidden reasoning.

## Event types
TASK_STARTED, CONTRACT_RESOLVED, SOURCE_READ, DECISION_RECORDED, ACTION_REQUESTED, ACTION_SUCCEEDED, ACTION_FAILED, POSTCONDITION_VERIFIED, CHECKPOINT_WRITTEN, REQUIREMENT_PASSED, REQUIREMENT_FAILED, BLOCKED, ROLLBACK_STARTED, ROLLBACK_VERIFIED, TASK_COMPLETED.

## Required fields
event_id; task_id; timestamp; event_type; actor; tool_or_boundary; target; requirement_ids; input_ref (sanitized); output_ref; result; evidence_ref; error_class; retry_count; duration_ms; parent_event_id; correlation_id.

## Do not log
Secrets, raw credentials, unnecessary personal data, hidden chain-of-thought.

## Derived metrics
- verification coverage
- requirement pass ratio
- unverified-success ratio (target 0)
- retry amplification
- mean recovery time
- rollback success rate
- stale-context incidents
- scope deviation count
- evidence freshness
- tool-success/postcondition-failure rate

## Golden signal for autonomous agents
Not "number of actions". Use verified objective progress per unit cost/time with zero critical boundary violations.

## Trace invariant
Every state-changing action must be traceable to a task + requirement + authority + postcondition verification.
