# Design Specification — Side-Effect Transaction Firewall

> **Classification: `PROPOSAL_BY_AI`.** This design is an engineering proposal stored in AI-CONTEXT. It does not override DOC-B/C/D/E, NEXY source, sealed evidence, or explicit user instructions.

## 1. Objective

Create a deterministic, fail-closed planning layer that can receive a bounded multi-action side-effect proposal and answer one of two planning outcomes:

- `ALLOW` with a canonical `planHash`, deterministic order, and execution waves; or
- `FREEZE` with stable machine-readable reasons.

A second preflight phase binds current read-only observations to the compiled plan immediately before external execution and returns either `COMMIT_READY` or `FREEZE`.

## 2. Non-goals

- Tool execution.
- Repository mutation.
- Distributed locking.
- Durable WAL/transaction coordinator.
- Authentication or signature verification.
- Replacing NEXY's existing authority, deterministic core, queue, idempotency, or safety systems.
- Declaring itself a NEXY requirement.

## 3. Authority and trust boundary

The planner treats all candidate actions as claims. An `authorityHash`, `deterministicInputHash`, approval hash, or precondition hash being syntactically valid does not prove the underlying authority. A future trusted boundary must validate those proofs before constructing an action.

The planner itself owns structural and relational decisions: canonicalization, policy membership, conflict analysis, dependency legality, precondition completeness, rollback coverage, deterministic identity, and preflight observation consistency.

## 4. Core invariants

### I-01 Deterministic identity
Equivalent valid input sets compile to the same normalized action order, dependency order, policy identity, and plan identity independent of caller list order.

### I-02 No hidden mutation
An action whose effect class is `NONE` may not contain `WRITE`, `CREATE`, `DELETE`, `APPEND`, `EXECUTE`, or `CALL` access. A non-`NONE` effect must expose at least one such side-effecting access so conflict analysis can see it.

### I-03 Protected resources fail closed
If any declared resource matches a protected prefix or fragment, the whole plan freezes before a commit seal can exist.

### I-04 Every mutation has a freshness condition
When policy requires it, every side-effecting resource must have at least one precondition for the same declared resource.

### I-05 Unordered conflicting effects are illegal
Two actions touching the same resource may execute without ordering only when both are `READ`. If either side is side-effecting, one action must transitively depend on the other.

### I-06 Rollback coverage is exact
A reversible/compensatable mutation requiring rollback must declare rollback resources exactly equal to the action's side-effecting resource set.

### I-07 Irreversibility is explicit
An irreversible action cannot carry rollback fiction. The default policy forbids irreversible operations; an alternate policy must explicitly allow them and may require a valid approval hash.

### I-08 Preflight is exact-set verification
The observer may not omit required preconditions, duplicate them, or inject observations not requested by the plan. Hash preconditions must match exactly.

### I-09 Plan tamper invalidates later phases
Preflight sealing and compensation recompute the allowed-plan hash. If fields were mutated or a forged object is supplied, the phase freezes with `PLAN_HASH_MISMATCH`.

### I-10 Compensation cannot pretend to undo the irreversible
If a completed action is irreversible, compensation freezes rather than emitting a false rollback sequence.

## 5. Data model

### TransactionPolicy
Sealed policy material includes allowed effect classes, maximum risk tier, protected resource prefixes/fragments, mutation precondition requirement, rollback requirement, effect classes requiring idempotency, irreversible-action policy, and max action count. Set-like arrays are canonicalized and deduplicated before hashing.

### ActionSpec
Each action carries stable identity and kind, one observed-NEXY-compatible side-effect class, explicit resource accesses, declared side-effect operations, dependency IDs, preconditions, optional idempotency key, reversibility/rollback metadata, risk tier, deterministic input hash, authority claim, and optional irreversible approval hash.

### AllowedPlan
Contains sealed policy identity, canonical action array, deterministic topological order, execution waves, and plan hash.

### PreflightSeal
Binds the exact plan hash to canonical current observations. It does not itself grant production authority.

## 6. State machine

```text
DRAFT
  | compile
  +------------------+
  |                  |
  v                  v
FROZEN          COMPILED_ALLOWED
                      |
                      v
                PREFLIGHT_CHECK
                  |         |
                  v         v
               FROZEN   COMMIT_READY
                            |
                            | future external executor
                            v
                         EXECUTING
                       /           \
                      v             v
                COMPLETED      PARTIAL_FAILURE
                                   |
                                   v
                          COMPENSATION_PLAN
                             |          |
                             v          v
                          FROZEN    COMPENSATE
```

Only through `COMMIT_READY` and compensation-plan generation is implemented here. Actual execution is intentionally outside this package.

## 7. Conflict algorithm

The implementation builds a dependency graph and transitive reachability. For every pair of actions it examines accesses sharing a resource ID. If either access is side-effecting and neither action is transitively ordered before the other, the plan receives `UNSERIALIZED_RESOURCE_CONFLICT`.

This favors correctness and inspectability over asymptotic cleverness. The default proposal caps a plan at 256 actions.

## 8. Determinism strategy

- UTF-8 bytewise canonical text comparison.
- Object keys sorted before hashing.
- Safe integers encoded explicitly; bigint has a separate canonical marker.
- Set-semantic arrays normalized before hashing.
- Domain-separated SHA-256 identities.
- Freeze reasons deduplicated by canonical hash and sorted.
- DAG ready queues canonically sorted at every wave.

## 9. Recovery model

Compensation accepts the exact compiled plan plus IDs known to have completed. It verifies plan integrity, rejects unknown IDs, rejects any completed irreversible action, then emits rollback steps in reverse topological order.

Returned compensation steps are not an authority bypass. A production coordinator should translate them to fresh actions and run policy + preflight again.

## 10. Threat model

Considered: hidden side effects, protected-resource targeting, policy tamper, plan tamper, stale state/TOCTOU preconditions, duplicate/replayed requests, unordered conflicts, incomplete rollback, false rollback for irreversible operations, caller-order nondeterminism.

Not solved here: stolen credentials, forged-but-syntactically-valid authority proofs, compromised executor, distributed race after preflight, physical safety, or external service correctness.

## 11. Local bounded-performance observation

A 256-action independent-filesystem fixture was compiled 50 measured times after 5 warmups in the local Node v22.16.0 environment. Latest recorded run: median 38.308 ms, p95 59.936 ms, stable plan hash across all runs.

This is a microbenchmark, **not** a product SLO, deployment claim, or guarantee on another machine.

## 12. Compatibility strategy

The lab does not import NEXY source. Its adapter mirrors only the observed structural `SideEffectDeclaration` shape. If NEXY changes the effect-class set, compatibility should fail until explicitly updated. Silent widening is forbidden.

## 13. Production adoption gate

Before real integration, at minimum: authoritative requirement approval, exact target revision refresh, real envelope mapping, trusted authority-proof validation, executor seal validation, lock/lease strategy, durable journal, crash recovery, integration/E2E tests, and operational fault-injection evidence.

Until then this remains a tested standalone proposal.
