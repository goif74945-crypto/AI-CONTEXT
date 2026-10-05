# Capacity Simulation and Evaluation Specification

> Classification: AI_PROPOSAL / test design. No simulation has been executed for NEXY.AI; all numeric examples below are parameters, not observed facts.

## 1. Purpose

Define a reproducible way to test whether admission, queues, retries, evidence work, and caches remain correct under normal load, burst load, dependency degradation, and adversarial timing.

The simulator evaluates policy; it must not be used to claim production capacity without calibrated production inputs.

## 2. Model boundary

The model contains:

- arrival generator;
- workload classifier;
- admission controller;
- priority/fairness scheduler;
- resource pools;
- dependency models;
- cache model;
- retry controller;
- cancellation/timeout behavior;
- evidence stage;
- recovery path;
- telemetry and invariant monitor.

Each component owns an explicit state transition. Event order must be deterministic when timestamps tie.

## 3. Event model

Canonical event tuple:

[
event=langle logical_time, sequence, type, task_id, resource_id, payload_digestangle
]

Order by logical_time then monotonically assigned sequence. Do not use wall-clock races to decide outcomes in a reproducibility test.

Suggested event types:

ARRIVE, ADMIT, QUEUE, START, DEPENDENCY_CALL, DEPENDENCY_RETURN, RETRY, CACHE_LOOKUP, CACHE_RESULT, VERIFY_START, VERIFY_END, CANCEL, SHED, COMPLETE, RESOURCE_RELEASE, POLICY_CHANGE, FAILURE_INJECT.

## 4. Workload record

Every synthetic or replayed task includes:

- task_id;
- workload_class;
- tenant/principal class;
- arrival time;
- priority;
- deadline;
- required resources;
- service-time distribution identifier;
- evidence requirement;
- mutation risk;
- cache eligibility;
- retry policy;
- degradation permissions;
- expected terminal state.

Synthetic records must be marked SYNTHETIC. Replayed data must be sanitized and provenance-recorded.

## 5. Resource model

For resource (r):

- capacity units;
- maximum safe concurrency;
- service-time distribution;
- queue discipline;
- failure state;
- quota window;
- recovery behavior;
- cancellation cost;
- leak detection.

Resource accounting invariant:

[
allocated_r + available_r = configured_capacity_r
]

except during a declared reconciliation state, which must be bounded and observable.

## 6. Scenario matrix

| ID | Scenario | Injection | Primary invariant |
|---|---|---|---|
| S01 | Baseline | Stable arrivals below capacity | SLO and evidence floor hold |
| S02 | Sudden burst | 10x arrival rate for bounded interval | Optional work sheds first |
| S03 | Slow dependency | Service latency multiplier | Backpressure prevents cascade |
| S04 | Hard outage | Dependency unavailable | Fail fast after breaker opens |
| S05 | Retry storm | Correlated transient failures | Retry budget bounds amplification |
| S06 | Cache stampede | Popular cold key | Single-flight and waiter caps hold |
| S07 | Stale cache | Dependency version changes | Stale result never completes claim |
| S08 | Mixed tenants | One abusive burst source | Other tenants retain governed share |
| S09 | Reservation leak | Task stalls after reservation | Lease/reaper restores capacity safely |
| S10 | Deadline collapse | Queue age exceeds slack | Unsafe mutations do not start |
| S11 | Evidence saturation | Verification resource constrained | Generation does not consume evidence floor |
| S12 | Recovery surge | Dependency returns after outage | Recovery ramp avoids second overload |
| S13 | Priority inversion | Low-priority holder blocks P0 | Inversion is bounded/resolved |
| S14 | Cancellation race | Cancel concurrent with commit | Exactly one terminal outcome |
| S15 | Unknown health | Telemetry absent | Conservative policy; no fabricated health |
| S16 | Policy rotation | Policy digest changes mid-flight | Old/new decisions remain attributable |

Multipliers are test parameters; they are not production estimates.

## 7. Metrics

### Correctness

- invariant violations;
- completions below evidence floor;
- unauthorized cross-tenant reuse;
- double commits;
- lost cancellations;
- resource accounting drift;
- stale-result completion count.

Target for correctness invariants: zero observed violations in the declared test space. This does not prove absence outside that space.

### Service

- admitted, queued, shed, blocked, completed counts;
- end-to-end and queue p50/p95/p99;
- deadline miss ratio;
- goodput: verified successful tasks per time unit;
- wasted work from cancellations and discarded retries;
- recovery time;
- breaker open duration;
- fairness deviation.

### Economics

[
cost_per_verified_completion=
rac{generation+tools+verification+retry+waste+recovery}{verified_completions}
]

Also record cost per admitted task, because shedding can cosmetically improve completion cost.

## 8. Fairness measures

Use at least two views:

1. minimum guaranteed share violations by tenant/class;
2. normalized service ratio against policy weight.

An aggregate fairness index alone can hide starvation of a small critical class. Report maximum queue age and starved-task count.

## 9. Retry amplification

Define:

[
amplification=rac{total downstream attempts}{original admitted tasks}
]

Measure globally and per dependency. A retry policy fails if amplification can grow without a configured bound during correlated failure.

## 10. Experimental controls

A valid comparison requires:

- same simulator version and seed policy;
- same event-order law;
- same workload trace;
- same dependency trace;
- same warm/cold cache state;
- same metric windows;
- policy digests recorded;
- enough replications to report uncertainty for stochastic models.

If randomness is prohibited in a target environment, use enumerated deterministic traces. If randomness is used for research, record seed and generator version.

## 11. Pass/fail gates

Mandatory gates:

- G01: zero integrity invariant violations;
- G02: zero completions below evidence floor;
- G03: zero unauthorized data disclosures;
- G04: bounded queue memory;
- G05: bounded retry amplification;
- G06: every admitted durable mutation has completion or recovery terminal state;
- G07: every reservation is released or expires through a verified mechanism;
- G08: no P3/P4 work consumes reserved P0 recovery capacity;
- G09: every metric denominator includes failures and timeouts;
- G10: result artifact identifies simulator, policy, workload, and dependency versions.

Thresholds for latency, fairness deviation, and cost remain UNKNOWN until an authorized SLO and calibrated workload exist.

## 12. Counterexample minimization

When an invariant fails:

1. preserve the full event trace;
2. derive the smallest prefix that still fails;
3. minimize workload/tasks while retaining failure;
4. record policy and state digests;
5. create a regression fixture;
6. verify the fixture fails before repair and passes after repair.

Never discard a failing trace because it is statistically rare.

## 13. Result schema

```yaml
run_id:
classification: SYNTHETIC|REPLAY
simulator_version:
policy_digest:
workload_digest:
dependency_trace_digest:
cache_initial_state_digest:
start_logical_time:
end_logical_time:
invariants:
metrics:
failures:
counterexamples:
limitations:
status: PASS|FAIL|PARTIAL|BLOCKED|NOT_VERIFIED
```

PASS means only that all declared gates passed for the identified run inputs.

## 14. Calibration plan

Before production inference:

- collect sanitized service-time and arrival histograms;
- separate task classes;
- validate tail behavior, not only means;
- compare simulated and observed queue lengths;
- backtest admission decisions;
- quantify parameter uncertainty;
- rerun sensitivity analysis at pessimistic bounds.

Until calibration is performed, production capacity remains UNKNOWN.

## 15. Build order

1. deterministic event engine;
2. resource accounting and invariants;
3. basic queues/admission;
4. dependency and retry models;
5. evidence/cancellation stages;
6. cache model;
7. failure injection;
8. trace export/replay;
9. counterexample minimizer;
10. calibrated scenario suite.

Status: TEST_SPEC_COMPLETE; SIMULATION_NOT_RUN; PRODUCTION_CAPACITY_UNKNOWN.
