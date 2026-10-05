# AI_PROPOSALS — Future Capacity and Resource Systems

> Every item in this file is an AI_PROPOSAL. None is a canonical requirement, approved roadmap item, or statement of current NEXY.AI implementation.

## Proposal governance

A proposal may advance only through:

IDEA → REVIEWED → AUTHORIZED_EXPERIMENT → EVIDENCED → ACCEPTED_OR_REJECTED

Default state is IDEA. Absence of rejection is not acceptance. Any experiment or implementation requires separate authority and must identify protected scope.

## P01 — Evidence Escrow

### Problem
Long tasks often spend nearly all resources on generation and later discover they cannot verify the output.

### Idea
Admission reserves an immutable evidence escrow per task. Only verification and recovery operations may consume it. Optional generation cannot borrow from escrow.

### Interfaces
- reserve(task, evidence_class, amount);
- debit_evidence(task, operation);
- release_unused(task);
- report_shortfall(task).

### Invariants
- COMPLETE is impossible if mandatory evidence work was not funded or executed;
- escrow ownership is task-scoped;
- unused escrow returns exactly once.

### Risks
Over-reservation reduces throughput; under-reservation blocks completion. Estimator calibration is required.

### Decisive experiment
Compare completion quality, blocked rate, and verified-goodput with and without escrow during evidence-resource saturation.

Status: IDEA.

## P02 — Semantic Budget Compiler

### Problem
User intents such as “fast,” “deep,” or “do not exceed cost” are not directly schedulable.

### Idea
Compile a Task Contract into explicit hard/soft resource constraints, evidence floor, degradation permissions, and stop conditions.

### Output
A signed/versioned budget plan with:
- constraint provenance;
- unresolved UNKNOWNs;
- candidate plans;
- predicted intervals;
- selected policy digest.

### Invariants
The compiler cannot invent a budget, relax an immutable rule, or turn missing values into infinity.

### Risks
False precision and policy complexity. Human-readable explanation is mandatory.

### Decisive experiment
Measure constraint-violation rate and operator correction rate across a fixed task corpus.

Status: IDEA.

## P03 — Counterfactual Scheduler Shadow

### Problem
Changing admission policy directly can damage live reliability.

### Idea
Run candidate policies in shadow against the same observed arrival/dependency trace without controlling production. Compare predicted decisions and outcomes.

### Boundaries
Shadow output has no mutation authority. It must be clearly separated from live decisions.

### Metrics
Decision divergence, predicted queue/tail latency, evidence-floor violations, fairness deviation, resource cost.

### Risks
Counterfactual service times are uncertain because alternative decisions change system state.

### Decisive experiment
Backtest against replay traces and quantify prediction error before any controlled canary.

Status: IDEA.

## P04 — Proof-Carrying Cache Artifact

### Problem
Cached content is frequently reused without proving that its authority, scope, version, and evidence still match.

### Idea
Every reusable artifact carries a machine-verifiable envelope containing identity, policy, evidence manifest, authorization scope, dependency versions, and freshness rule.

### Invariants
A consumer must validate the envelope before accessing payload; stronger claims cannot be derived from weaker proof without new evidence.

### Risks
Metadata size and validation cost may outweigh savings for small artifacts.

### Decisive experiment
Inject stale, cross-tenant, policy-mismatched, corrupted, and weak-evidence entries; require zero false hits.

Status: IDEA.

## P05 — Resource Futures for Multi-Stage Tasks

### Problem
A task can reserve current capacity yet fail later because downstream verification/recovery capacity is unavailable.

### Idea
Reserve staged capacity windows (“resource futures”) for critical downstream phases before starting irreversible work.

### Invariants
- futures are bounded and expire;
- admission accounts for outstanding commitments;
- speculative futures cannot starve P0 recovery;
- cancellation releases future claims exactly once.

### Risks
Poor forecasts waste capacity and increase scheduling complexity.

### Decisive experiment
Compare durable-mutation completion and wasted reservation under bursty verification demand.

Status: IDEA.

## P06 — Overload Constitution

### Problem
Ad hoc degradation can silently trade correctness for availability.

### Idea
Create a versioned, machine-readable overload constitution listing:
- priority classes;
- protected resources;
- degradation ladder;
- forbidden degradations;
- fairness guarantees;
- evidence floors;
- authority required for emergency overrides.

### Invariants
Every degraded decision references the governing version and reason. Emergency override is explicit and expires.

### Risks
Rigid policy can block useful work during novel incidents.

### Decisive experiment
Run the scenario matrix against multiple policies and verify no forbidden degradation is reachable.

Status: IDEA.

## P07 — Failure-Domain Budget Ledger

### Problem
Per-task limits do not prevent many individually legal tasks from overwhelming one shared dependency.

### Idea
Maintain budgets simultaneously by task, tenant, workload class, dependency, and failure domain.

### Accounting model
A resource debit is attributed to all applicable ledgers atomically. Admission requires all hard ledgers to allow the debit.

### Invariants
No partial debit; reconciliation detects drift; global recovery reserve is not tenant-borrowable.

### Risks
High-cardinality state, atomic update cost, and deadlock if ledger order is undefined.

### Decisive experiment
Simulate correlated failure across a shared provider and measure retry amplification and unaffected-domain goodput.

Status: IDEA.

## P08 — Capacity Digital Twin with Counterexample Search

### Problem
Hand-authored scenarios miss rare interleavings.

### Idea
Use a deterministic event simulator plus bounded state-space exploration to search for invariant violations, then minimize the failing trace.

### Search dimensions
Arrival order, cancellation timing, dependency delay, policy rotation, cache invalidation, reservation expiry, retry decision.

### Invariants
Every counterexample is reproducible from a compact event trace and version digests.

### Risks
State explosion and false confidence from incomplete bounds.

### Decisive experiment
Seed known concurrency defects and measure detection/minimization success.

Status: IDEA.

## P09 — Uncertainty-Aware Admission

### Problem
Point estimates make optimistic admission decisions when prediction uncertainty is high.

### Idea
Use prediction intervals and a risk budget. Higher mutation risk or weaker observability requires a more conservative percentile.

### Invariants
UNKNOWN is not zero variance; uncertainty policy is versioned; irreversible work uses the strictest allowed bound.

### Risks
Conservatism may reduce throughput and can encode estimator bias.

### Decisive experiment
Compare hard-limit violations and verified-goodput across calibrated and deliberately miscalibrated workloads.

Status: IDEA.

## P10 — Recovery Quarantine Lane

### Problem
Recovered dependencies may immediately receive the full backlog and fail again.

### Idea
Route resumed traffic through a quarantine lane with probes, capped concurrency, schema/authority validation, and gradual promotion.

### Invariants
Backlog cannot bypass quarantine; failed probes reopen containment; old responses cannot overwrite newer generations.

### Risks
Slower recovery and duplicated routing paths.

### Decisive experiment
Inject outage/recovery cycles and compare oscillation count, recovery time, and integrity violations.

Status: IDEA.

## Cross-proposal dependency map

| Proposal | Depends on | Enables |
|---|---|---|
| P01 Evidence Escrow | budget accounting | trustworthy completion |
| P02 Budget Compiler | task contract schema | schedulable intent |
| P03 Shadow Scheduler | trace capture, simulator | safer policy evolution |
| P04 Proof-Carrying Cache | provenance/evidence schema | safe reuse |
| P05 Resource Futures | multi-stage estimator | safer durable work |
| P06 Overload Constitution | authority model | deterministic degradation |
| P07 Failure-Domain Ledger | atomic accounting | bounded correlated load |
| P08 Digital Twin | deterministic event model | counterexample discovery |
| P09 Uncertainty Admission | calibrated estimator | fewer hard-limit breaches |
| P10 Quarantine Lane | breaker/recovery model | stable recovery |

## Recommended evaluation order

1. P06 policy specification and P07 accounting model;
2. P01 evidence escrow;
3. P04 proof-carrying cache;
4. P08 simulator/counterexample search;
5. P03 shadow scheduling;
6. P09 uncertainty admission;
7. P10 recovery quarantine;
8. P02 compiler and P05 futures after measurement data exists.

This order is itself an AI_PROPOSAL and requires authorization.

## Rejection conditions

Reject or redesign any proposal that:

- weakens the evidence floor;
- expands mutation authority;
- requires hidden model behavior;
- cannot expose deterministic failure semantics;
- creates unbounded reservations or retries;
- makes authorization depend on cache presence;
- cannot produce a reproducible audit trail;
- has no decisive falsification experiment.

Status: PROPOSAL_SET_COMPLETE; ALL_ITEMS_UNAUTHORIZED_IDEAS.
