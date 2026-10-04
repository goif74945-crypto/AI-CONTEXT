# PEPSA Design Contract

## 1. Objective

Detect structurally unsafe execution plans before side effects occur, especially plans that can leave residual state when execution stops after only a prefix has completed.

## 2. Non-goals

PEPSA does not:

- infer a plan from natural language;
- execute tools;
- authenticate approvals;
- verify a rollback implementation at runtime;
- verify provider idempotency behavior;
- replace NEXY LAW/JUDGE/CORE;
- become authority by existing in AI-CONTEXT;
- claim current DOC-C scope.

## 3. Trust boundary

`Policy` and `ExecutionPlan` are separate objects.

The plan declares **what it proposes to do**.  
The policy declares **what is allowed**.

The analyzer never copies permissions from the plan into policy. That prevents a self-authorizing plan from widening its own boundary.

## 4. Data model

### Step

Required identity fields:

- `id`
- `kind`: `READ | CREATE | UPDATE | DELETE | EXTERNAL_EFFECT`
- `resource`
- `boundary`

Optional/conditional fields:

- `depends_on[]`
- `reversible`
- `rollback_strategy`
- `approval_id`
- `idempotency_key`
- `postcondition`
- `evidence_required[]`

### Policy

- `policy_id`
- `allowed_boundaries[]`
- `protected_resources[]` using deterministic glob matching
- `max_steps`
- mutation postcondition gate
- mutation evidence gate
- external-effect idempotency gate
- terminal irreversible approval gate

## 5. Deterministic order

The graph is topologically sorted with a lexical min-heap over ready step IDs. Therefore multiple legal topological orders collapse to one stable order.

Invalid graph conditions:

- duplicate step ID;
- missing dependency;
- self-dependency;
- dependency cycle.

These return invalid-input semantics, not an execution verdict.

## 6. Partial-state algorithm

For every boundary immediately before a later step:

1. consider the prefix of steps that would already have succeeded;
2. collect prior mutating resources without declared rollback coverage;
3. if the set is non-empty, record `UNSAFE_PARTIAL_STATE`;
4. `UNSAFE_PARTIAL_STATE` is an error and causes `FREEZE`.

This is deliberately conservative. It does not trust a vague “transactional” claim as proof. A future integration may add verified transaction evidence, but this prototype does not grant safety from prose.

## 7. Irreversible actions

An irreversible mutation:

- requires `approval_id`;
- may be allowed only as the terminal action when policy permits it;
- freezes if later deterministic steps exist, because failure after the irreversible action could strand partial state.

The approval ID is only a structural declaration in v0.1. Authenticity is not verified here.

## 8. External effects

When policy enables the gate, `EXTERNAL_EFFECT` requires an `idempotency_key`.

Reason: retries or ambiguous provider responses must not silently multiply side effects. PEPSA checks presence only. Runtime/provider behavior remains separate evidence.

## 9. Canonical identity

Plan and policy identities use SHA-256 over canonical UTF-8 JSON:

- object keys sorted;
- compact separators;
- semantic set-like arrays normalized where appropriate;
- plan steps normalized by `step.id` for identity;
- dependency and evidence arrays sorted for identity;
- floating point rejected;
- no timestamps included in authority hashes.

The combined report identity binds:

`plan_hash + policy_hash + report_version`.

## 10. Failure model

| Condition | Result |
|---|---|
| malformed JSON/schema-like shape | INVALID_INPUT |
| graph cycle/missing dependency | INVALID_INPUT |
| protected mutation | FREEZE |
| unauthorized boundary | FREEZE |
| missing mutation postcondition | FREEZE |
| missing mutation evidence requirement | FREEZE |
| reversible without rollback declaration | FREEZE |
| irreversible without approval | FREEZE |
| nonterminal irreversible mutation | FREEZE |
| external effect without required idempotency key | FREEZE |
| unsafe residual prefix | FREEZE |
| no error findings | READY |

## 11. Complexity

For `V` steps and `E` dependency edges:

- graph validation/topological order: `O((V + E) log V)` because ready nodes use a heap;
- policy checks: `O(V × P)` where `P` is protected-resource glob count;
- partial-state scan: bounded by plan size and distinct residual resources.

The default policy caps the plan at 128 steps to keep preflight bounded.

## 12. Security properties

- no network access;
- no subprocess execution;
- no filesystem mutation by analyzer logic;
- CLI only reads declared JSON files and writes report text to stdout/stderr;
- strict unknown-field rejection reduces typo-driven policy bypass;
- boolean is not accepted as an integer for limits;
- float rejection avoids accidental numeric nondeterminism in hashed input.

## 13. Future work requiring separate authorization

- signed/authenticated approvals;
- verified compensation handlers;
- transaction-boundary evidence;
- provider-specific idempotency verification;
- integration into NEXY CORE/RUN/JUDGE;
- UI consequence preview;
- runtime trace comparison between preflight and executed effects.

All items above are proposals, not current implementation claims.
