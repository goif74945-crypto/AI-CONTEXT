# NEXY Frontier Assurance Lab — Design

**Classification: AI-PROPOSED / EXPERIMENTAL / NOT CANON**

## Objective
Add five standalone assurance mechanisms that can integrate through explicit adapters while preserving NEXY authority and fail-closed semantics.

## 1. MUSCLE — Minimal Unsatisfiable Constraint Locator Engine
Computes an exact minimum-cardinality unsatisfiable core over finite enumerated domains using ALLOW/DENY/EQ/NEQ. It never relaxes rules and freezes if the exact-search bound is exceeded. Use: explain the smallest real conflict instead of dumping every active rule.

## 2. PAREX — Pareto Execution Candidate Pruner
Removes only objectively Pareto-dominated candidate plans across benefit/evidence (maximize) and cost/latency/risk (minimize). Equal/trade-off plans survive. PAREX never selects the final winner. Use: reduce SWARM/JUDGE load without hiding policy in ranking.

## 3. GHOSTEDGE — Hidden Dependency Perturbation Detector
Consumes controlled perturbation experiments and emits undeclared dependency candidates when perturbing A repeatedly causes observed B to fail above deterministic hit/ratio thresholds. Result is a candidate, not causal proof. Use: reveal missing graph edges before change-impact analysis reuses evidence incorrectly.

## 4. RECERT — Recovery Equivalence Certifier
Compares pre-failure and post-recovery state under explicit per-path modes EXACT/NONDECREASING/PRESENT/ABSENT/ANY. Default is strict EXACT. Use: prove semantic recovery rather than “process restarted”.

## 5. OBSURE — Observability Sufficiency Gate
Pre-execution admission gate over side-effect telemetry. Baseline phases: INTENT, START, SUCCESS, FAILURE. Reversible effects also require COMPENSATION_START/COMPENSATION_RESULT. Baseline fields: trace_id/action_id/effect_id/timestamp. HIGH/CRITICAL adds authority_ref/evidence_ref; CRITICAL adds state_digest.

## Composition
FrontierAssurancePipeline returns READY or FREEZE only and executes no external action. Default freeze reasons: unsat constraints, no eligible plan, hidden dependency candidate, failed recovery equivalence, insufficient observability.

## Security boundary
Pure-data reference code. No network, subprocess, credentials, external mutation, or NEXY.AI import.

## Complexity
- MUSCLE: linear normal filtering; bounded exact combinatorial search only on conflicting per-variable constraints.
- PAREX: O(n²).
- GHOSTEDGE: O(experiments × observed components).
- RECERT: O(flattened leaves).
- OBSURE: O(effects + telemetry event specs) plus deterministic sorting.

## Known limitations
Finite-domain MUSCLE only. PAREX trusts normalized metrics. GHOSTEDGE is correlation from controlled perturbation, not causality proof. RECERT is structural, not theorem proving. OBSURE validates telemetry specification, not actual runtime emission.
