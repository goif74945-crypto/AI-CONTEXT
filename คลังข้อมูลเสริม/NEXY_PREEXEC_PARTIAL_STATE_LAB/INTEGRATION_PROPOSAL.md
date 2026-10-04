# PEPSA Future Integration Proposal

**Status: AI-PROPOSED ONLY.** This file does not change current NEXY requirements.

## Proposed placement

A future integration could place PEPSA after an execution plan is already explicit and policy-resolved, but before any side-effecting tool call:

```text
Directive
  -> existing NEXY authority / planning path
  -> explicit ExecutionPlan
  -> LAW-owned Policy snapshot
  -> PEPSA structural preflight
       READY  -> existing execution authority decides whether execution may proceed
       FREEZE -> no side effect; expose deterministic finding summary
  -> runtime execution
  -> runtime evidence comparison
```

PEPSA should **not** become the final authority. It is a guard that emits analyzable evidence. CORE/LAW/JUDGE remain the governing architecture where authoritative source says so.

## Proposed ownership boundaries

| Object | Proposed owner | PEPSA authority |
|---|---|---|
| User directive | existing NEXY intake | none |
| ExecutionPlan | existing planner/core path | read-only input |
| Policy | LAW / governed configuration | read-only input |
| Approval authenticity | AUTH / governed approval service | none in v0.1 |
| Preflight report | PEPSA | deterministic generation only |
| Execute / freeze decision | existing NEXY authority | PEPSA report may be a required gate only if promoted |
| Runtime evidence | execution/observability stack | none in v0.1 |

## Proposed product experience

If promoted, NEXY::RUN could expose a compact **Consequence Preview** before high-impact work:

- 7 steps, deterministic order locked;
- 3 resources mutate;
- 3 rollback-covered;
- 0 protected resources touched;
- 0 unsafe partial states;
- plan identity hash;
- result: READY.

For a blocked plan:

- step `delete-canonical` is irreversible before two later steps;
- failure before `publish-index` can leave one residual resource;
- result: FREEZE.

The UI must not convert `FREEZE` into a friendly-looking warning that still permits execution unless authoritative policy explicitly defines an override path.

## Promotion gates

Before any integration claim, require at least:

1. **Contract promotion** — an authoritative NEXY source explicitly defines whether PEPSA or equivalent behavior is required.
2. **Resource canonicalization contract** — repository/path/API identities are canonicalized before policy matching.
3. **Approval verification** — approval identifiers are authenticated and replay-safe.
4. **Rollback verification** — declared rollback strategies are linked to executable, tested compensation behavior.
5. **Transaction evidence** — if transaction groups are later allowed, atomicity is proven by matching integration/runtime evidence rather than prose.
6. **Provider idempotency tests** — external providers are tested for the exact retry/idempotency semantics relied upon.
7. **E3 integration tests** — planner/policy/preflight/executor boundaries exercised together.
8. **E4 user-flow tests** — consequence preview and freeze behavior tested through actual user flow.
9. **E5 runtime reconciliation** — executed effects are compared with preflight declaration and drift freezes the run.
10. **Security review** — alias/path bypass, Unicode, TOCTOU, stale-policy, approval spoofing, and report tampering tested.

## Proposed runtime reconciliation extension

A later version could emit an expected effect ledger:

```text
expected_effect(step_id, resource, kind, postcondition, evidence_requirement)
```

Runtime observability would emit an actual effect ledger. A deterministic comparator could then detect:

- undeclared effects;
- missing declared effects;
- target identity drift;
- order drift;
- unexpected retries;
- partial rollback.

Any drift in an authoritative execution could become a freeze-class incident, subject to project law.

This extension is not implemented here.
