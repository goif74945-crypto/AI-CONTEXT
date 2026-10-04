# Agent Orchestration and Isolation
Parallelism must not leak authority, duplicate side effects, or lose verification ownership.

Roles: Planner (decompose), Researcher (read-only evidence), Executor (scoped mutations), Verifier (independent acceptance checks), Auditor (cross-workstream consistency).

## Work-unit contract
work_id, objective, inputs, authoritative_spec, scope_in/out, allowed_tools, write_targets, forbidden_targets, dependencies, acceptance_tests, evidence_required, rollback_plan, budgets, stop_conditions.

## Concurrency
Resource lease; optimistic hash/version before write; append-only action log; external-effect dedupe key; cancellation propagation; merge conflict scan.

## Handoff
Transmit completed facts, unknowns, artifacts, evidence IDs, side effects, verification status, next safe action. “Done” is not evidence.

Scope violation => quarantine. Evidence conflict => freeze dependent decision. Verifier disagreement => NOT VERIFIED. Ambiguous tool result => re-read authoritative state.
