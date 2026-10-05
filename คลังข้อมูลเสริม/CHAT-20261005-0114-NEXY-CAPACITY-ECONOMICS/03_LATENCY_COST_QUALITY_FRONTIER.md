# Latency–Cost–Quality Frontier

> Classification: AI_PROPOSAL / engineering specification. It is not evidence of current NEXY.AI behavior.

## 1. Decision problem

An agent task must not optimize a single scalar such as token count or response time. The scheduler chooses a feasible execution plan whose evidence strength and semantic quality satisfy a minimum contract while resource consumption stays inside authorized limits.

For task (T), plan (p) has an outcome vector:

[
O(T,p)=langle L_{p50},L_{p95},L_{p99},C,Q,E,Rangle
]

where:

- (L): end-to-end latency distribution;
- (C): normalized resource cost;
- (Q): task-specific semantic quality;
- (E): evidence completeness;
- (R): residual risk after verification.

A plan is feasible only if all hard constraints hold. Among feasible plans, retain the Pareto frontier; do not hide trade-offs inside an undocumented weighted score.

## 2. Required task contract

Every capacity-sensitive task SHOULD declare:

| Field | Meaning |
|---|---|
| task_class | Stable workload family |
| hard_deadline_ms | Deadline that cannot be silently violated |
| soft_latency_slo | Desired percentile target |
| quality_floor | Minimum task-specific quality |
| evidence_floor | Minimum required evidence class |
| max_cost | Explicit resource ceiling |
| degradation_permissions | Optional work that may be removed |
| mutation_risk | READ_ONLY, REVERSIBLE, DURABLE, IRREVERSIBLE |
| cancellation_semantics | What happens when budget/deadline expires |

UNKNOWN values must remain UNKNOWN. A missing budget is not an infinite budget.

## 3. Quality decomposition

Avoid one opaque “quality” number. Use a vector:

[
Q=langle correctness, completeness, relevance, consistency, instruction_fidelityangle
]

Each component requires a task-specific measurement. For example:

- correctness: verified assertions / checked assertions;
- completeness: satisfied mandatory requirements / applicable mandatory requirements;
- relevance: required deliverables present with no unauthorized scope;
- consistency: contradictions found after normalization;
- instruction fidelity: preserved immutable constraints / applicable immutable constraints.

Aggregation is allowed only after the component values and weighting rule are retained.

## 4. Evidence floor

Evidence is a feasibility constraint, not a polish step.

Examples:

- repository-state claim → current repository read;
- code behavior claim → executed test at identified revision;
- external-current claim → dated authoritative source;
- architectural proposal → explicit proposal label plus internally consistent acceptance tests.

A faster plan that cannot meet the evidence floor is infeasible, even if its prose appears convincing.

## 5. Phase budget allocation

Reserve budget before execution:

[
B_{total}=B_{discovery}+B_{execution}+B_{verification}+B_{recovery}
]

Suggested starting policy for uncalibrated workloads is an ASSUMPTION, not a fact:

- discovery: 15–25%;
- execution: 35–55%;
- verification: 20–35%;
- recovery reserve: 10–20%.

These ranges MUST be calibrated from observed workloads. Verification reserve may not be consumed by optional generation.

## 6. Frontier construction

For each task class:

1. define mandatory requirements and evidence floor;
2. enumerate candidate plans;
3. reject plans violating hard constraints;
4. measure actual outcome vectors;
5. remove dominated plans;
6. select by current operating policy;
7. record predicted versus observed values;
8. recalibrate when error exceeds the declared tolerance.

Plan A dominates plan B only if A is no worse on every governed dimension and strictly better on at least one. Any conversion of dimensions into money or one score must expose its assumptions.

## 7. Tail-latency control

Mean latency is insufficient. Track:

- queue delay;
- model time;
- tool time;
- verification time;
- retry time;
- cancellation cleanup;
- p50, p95, p99, maximum within the observation window.

A p50 improvement that worsens p99 can increase user-visible failure. Admission decisions should use a high percentile matched to the SLO and sample size.

## 8. Deadline-aware execution

Let remaining slack be:

[
S=deadline-now-predicted_mandatory_work-predicted_verification
]

Policy:

- (S>guard): execute full eligible plan;
- (0<Sle guard): remove only authorized optional work;
- (Sle0): return explicit PARTIAL/BLOCKED or cancel before unsafe mutation.

Never start a durable mutation if the remaining budget cannot cover its commit, verification, and recovery path.

## 9. Experimental protocol

For every candidate plan:

- fixed task corpus and version;
- fixed evaluation rubric;
- isolated warm and cold cache cohorts;
- repeated trials sufficient to report uncertainty;
- separately measured queue and service time;
- failures retained in the denominator;
- cost includes retries, verification, and discarded work;
- no tuning on the hidden acceptance set.

Report raw per-task observations in addition to aggregates.

## 10. Decision table

| Condition | Required action |
|---|---|
| quality or evidence below floor | Reject plan |
| hard cost ceiling exceeded | BLOCK; do not bill silently |
| deadline threatened, optional work exists | Apply authorized degradation |
| deadline threatened, only mandatory work remains | PARTIAL/BLOCKED |
| prediction interval too wide | Admit conservatively or collect calibration data |
| plans are non-dominated | Preserve trade-off and use explicit policy |
| metrics unavailable | NOT_VERIFIED; do not infer success |

## 11. Failure modes

- optimizing proxy quality while real correctness falls;
- comparing warm-cache and cold-cache plans as if equivalent;
- excluding failed or timed-out tasks;
- consuming verification reserve during generation;
- choosing averages that conceal tail failure;
- treating user attention as free;
- recalibrating on a changing workload without versioning.

## 12. Acceptance properties

A conforming implementation would demonstrate:

1. hard constraints are checked before plan selection;
2. evidence floor cannot be degraded;
3. outcome vectors retain component metrics;
4. dominated plans are identifiable;
5. prediction error is measured;
6. timeout behavior is deterministic and auditable;
7. failures and retries remain in cost and latency accounting.

Status: SPECIFICATION_COMPLETE; IMPLEMENTATION_NOT_VERIFIED.
