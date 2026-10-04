# Failure Model

> `PROPOSAL_BY_AI` taxonomy for the standalone lab.

The planner freezes the **whole plan** rather than silently deleting or repairing invalid actions. Partial acceptance could change dependency order, rollback safety or user intent.

## Compile-time families

| Family | Representative reason codes | Meaning |
|---|---|---|
| Identity | `ACTION_ID_INVALID`, `DUPLICATE_ACTION_ID`, `HASH_INVALID`, `AUTHORITY_INVALID` | identity/evidence shape cannot be trusted |
| Policy | `EFFECT_CLASS_FORBIDDEN`, `RISK_TIER_EXCEEDED`, `TOO_MANY_ACTIONS` | plan exceeds sealed policy |
| Effects | `DECLARED_OPERATIONS_REQUIRED`, `SIDE_EFFECT_DECLARATION_CONTRADICTION` | side effects are hidden or contradictory |
| Resources | `RESOURCE_ID_INVALID`, `DUPLICATE_RESOURCE_ACCESS`, `PROTECTED_RESOURCE` | resource set invalid/protected |
| DAG | `DEPENDENCY_UNKNOWN`, `DEPENDENCY_SELF_REFERENCE`, `DEPENDENCY_CYCLE` | ordering graph invalid |
| Concurrency | `UNSERIALIZED_RESOURCE_CONFLICT` | same-resource effect has no dependency order |
| Freshness | `PRECONDITION_REQUIRED`, `PRECONDITION_INVALID` | mutation lacks valid state gate |
| Replay | `IDEMPOTENCY_REQUIRED`, `DUPLICATE_IDEMPOTENCY_KEY` | retry identity missing/ambiguous |
| Recovery | `MUTATION_REVERSIBILITY_REQUIRED`, `ROLLBACK_REQUIRED`, `ROLLBACK_COVERAGE_MISMATCH`, `ROLLBACK_INVALID` | recovery contract incomplete |
| Irreversible | `IRREVERSIBLE_FORBIDDEN`, `IRREVERSIBLE_APPROVAL_REQUIRED` | irreversible operation disallowed/unapproved |

## Preflight failures

Major strings include `PLAN_HASH_MISMATCH`, duplicate/unexpected/missing observation, resource mismatch, invalid observed hash, and PRESENT/ABSENT/HASH_MATCH failures.

Any one prevents `COMMIT_READY`.

## Compensation failures

Major cases: `PLAN_HASH_MISMATCH`, unknown completed action, completed irreversible action, or missing rollback.

A compensation freeze is intentional. Once external state was partially changed, inventing a rollback is less safe than exposing an explicit blocked recovery state.
