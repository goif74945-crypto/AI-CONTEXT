# Failure Experiments and Recovery Playbook

> Classification: AI_PROPOSAL / engineering research. No experiment here has been executed against NEXY.AI.

## 1. Objective

Test failure semantics before production incidents do it involuntarily. The target is not merely availability; it is preservation of authority, evidence, isolation, bounded resource use, and a truthful terminal state.

## 2. Safety contract for experiments

Before injection, define:

- exact target and environment;
- blast-radius boundary;
- protected data and resources;
- abort trigger;
- rollback/recovery procedure;
- expected invariant;
- observation channels;
- experiment owner;
- maximum duration;
- evidence artifact location.

Experiments against production require separate explicit authorization. This document does not grant it.

## 3. Universal invariants

During every failure:

1. no unauthorized mutation;
2. no completion claim below evidence floor;
3. no cross-tenant disclosure;
4. no duplicated irreversible effect;
5. resource use remains bounded;
6. cancellation produces a traceable outcome;
7. every task reaches one terminal status or a declared recoverable limbo state with bounded lease;
8. unknown dependency state is not reported as healthy;
9. recovery does not erase the original failure evidence.

## 4. Failure taxonomy

### Capacity failures
Queue explosion, memory exhaustion, slot starvation, reservation leak, head-of-line blocking.

### Dependency failures
Timeout, partial response, stale response, schema drift, rate limiting, correlated outage, recovery flapping.

### Control failures
Policy mismatch, priority inversion, cancellation race, retry storm, circuit-breaker oscillation.

### Data/evidence failures
Cache poisoning, provenance loss, evidence expiry, conflicting sources, incomplete write verification.

### Accounting failures
Double debit, missing debit, unreleased reservation, negative capacity, cost attribution drift.

### Recovery failures
Duplicate replay, late response overwriting newer state, thundering recovery, inconsistent checkpoint.

## 5. Experiment cards

### F01 — Reservation leak

Injection: stop a task after reservation but before release.

Expected:

- lease expires or authorized reaper acts;
- capacity returns exactly once;
- original task is not marked COMPLETE;
- audit trail links reservation, task, and release.

Fail if capacity is permanently lost or double-released.

### F02 — Correlated timeout and retry storm

Injection: all calls to one dependency time out for a bounded interval.

Expected:

- retries obey per-task and global budgets;
- circuit breaker limits new attempts;
- retry amplification remains bounded;
- unrelated dependency pools remain usable.

Fail if retry traffic grows after useful throughput reaches zero.

### F03 — Slow-but-successful stale response

Injection: an old request returns after a new policy/version is active.

Expected:

- generation/version precondition rejects the late result;
- newer state remains authoritative;
- discarded work is accounted as waste.

Fail if completion status regresses to an older decision.

### F04 — Cache authorization crossover

Injection: same semantic input from two tenants with different authority.

Expected:

- keys or authorization checks isolate results;
- no payload, hit metadata, or timing disclosure crosses boundary.

Fail on any shared result without explicit compatible scope.

### F05 — Evidence resource saturation

Injection: verification workers are exhausted while generation remains available.

Expected:

- verification reserve/admission throttles generation;
- tasks remain QUEUED/PARTIAL, never COMPLETE without proof;
- P0 recovery evidence retains capacity.

Fail if generation backlog consumes all remaining resources.

### F06 — Cancellation during durable commit

Injection: cancel immediately before, during, and after commit boundary.

Expected:

- deterministic idempotency key;
- exactly one authoritative effect;
- terminal state distinguishes committed, rolled back, and UNKNOWN_REQUIRES_RECONCILIATION;
- reconciliation resolves UNKNOWN before retry.

Fail on duplicate or silently lost effect.

### F07 — Metric blackout

Injection: remove queue/dependency telemetry.

Expected:

- health becomes UNKNOWN;
- controller enters documented conservative mode;
- no zero value is substituted for missing data;
- alert indicates observability loss.

Fail if missing telemetry is interpreted as healthy idle capacity.

### F08 — Recovery surge

Injection: restore a dependency after accumulated demand.

Expected:

- gradual probe/ramp;
- bounded concurrency;
- queued work respects priority and age;
- downstream does not re-enter outage from synchronized replay.

Fail on oscillating breaker or second overload caused by recovery.

### F09 — Policy change mid-flight

Injection: rotate admission/degradation policy while tasks execute.

Expected:

- each decision records policy digest;
- transition law states which policy governs existing work;
- prohibited new mutations cannot begin under superseded policy;
- audit can reconstruct both cohorts.

Fail if one task mixes incompatible policy rules without trace.

### F10 — Checkpoint corruption

Injection: truncate or alter a resumable checkpoint.

Expected:

- digest/schema validation fails;
- corrupt checkpoint is quarantined;
- resume falls back to last valid state or BLOCKED;
- no guessed state reconstruction.

Fail if corrupt data is accepted as current truth.

## 6. Recovery state model

Suggested states:

NORMAL → SUSPECTED → CONTAINING → DEGRADED → RECOVERING → VALIDATING → NORMAL

Side states:

FROZEN, MANUAL_RECONCILIATION, TERMINATED.

Transitions require recorded evidence. Time alone does not prove recovery.

## 7. Recovery gates

A dependency may return to normal service only after:

- health probes succeed under declared criteria;
- error and latency windows stabilize;
- schema/authority identity matches;
- backlog is below safe threshold or draining under cap;
- cache invalidations are complete where required;
- reconciliation finds no unresolved durable effects;
- rollback path remains available during ramp.

## 8. Experiment evidence record

```yaml
experiment_id:
proposal_version:
target:
environment:
authorization:
pre_state_digest:
injection:
start_time_source:
abort_conditions:
expected_invariants:
observed_events:
terminal_state:
violations:
recovery_actions:
post_state_digest:
status: PASS|FAIL|PARTIAL|BLOCKED|NOT_VERIFIED
limitations:
```

## 9. Stop conditions

Immediately abort and contain if:

- protected scope may be affected;
- observability required for safety is lost;
- experiment identity/target differs from authorization;
- an irreversible effect lacks idempotency/recovery;
- tenant isolation is uncertain;
- capacity accounting cannot be reconciled.

## 10. Acceptance criteria for a future implementation

- each experiment is reproducible from a versioned fixture;
- negative tests fail before a repair and pass afterward;
- failure traces retain ordering and policy digests;
- recovery is tested, not inferred from component restart;
- no experiment PASS is generalized beyond its target/version/environment;
- counterexamples become permanent regression cases.

Status: PLAYBOOK_COMPLETE; EXPERIMENTS_NOT_RUN.
