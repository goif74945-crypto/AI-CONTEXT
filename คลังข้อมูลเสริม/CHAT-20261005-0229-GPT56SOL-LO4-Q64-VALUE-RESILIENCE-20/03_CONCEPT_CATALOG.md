# Lo4 Q64.64 Concept Catalog — 20 AI-Proposed Systems

All entries are **Lo4 AI proposals, NOT CANON, NOT current NEXY implementation**. Each concept is implemented as a deterministic evaluator in `src/lo4q64/engines.py` and uses normalized Q64.64 inputs in `[0,1]`.

| ID | Concept | Primary value | Fail-closed / NEXY fit |
|---|---|---|---|
| L4Q64-01 | Opportunity Cost Router | Routes work by value, reversibility, slack and alternative cost | Confidence below 0.5 freezes; NEXY remains final judge |
| L4Q64-02 | Uncertainty Surface Tomograph | Localizes model/data/policy uncertainty hotspots | Poor observability/coverage reduces confidence and freezes |
| L4Q64-03 | Evidence Value-of-Information Planner | Schedules proof by marginal uncertainty reduction vs cost/latency | Unreliable measurement lowers confidence |
| L4Q64-04 | Freeze Granularity Optimizer | Freezes the smallest safe fault scope | Requires fault attribution + rollback precision |
| L4Q64-05 | Decision Half-Life Estimator | Scores how long decisions remain trustworthy | Change detection/evidence refreshability gate confidence |
| L4Q64-06 | Tool Hedge Portfolio | Quantifies safe provider/tool substitution | Semantic equivalence is a floor, not assumed |
| L4Q64-07 | Interruption Merge Compiler | Merges changed user direction while salvaging verified work | Mutation conflict and intent parse confidence are explicit |
| L4Q64-08 | Outcome SLO Budgeter | Jointly budgets latency, quality, cost, reliability | Minimum margin dominates; degraded-mode quality included |
| L4Q64-09 | Counterexample Reservoir | Maintains diverse replayable failure memory | Replayability and label quality gate trust |
| L4Q64-10 | Regret-Bound Planner | Limits worst-case regret while preserving learning/optionality | Irreversibility/harm/uncertainty dominate downside |
| L4Q64-11 | Human Cognitive Bandwidth Governor | Keeps user-facing control load inside decision bandwidth | Choice/notification overload directly penalize readiness |
| L4Q64-12 | Proof Reuse Graph Optimizer | Reuses proof only when premise/environment/version/lineage still match | Lineage and version mismatch suppress reuse |
| L4Q64-13 | Failure Containment Radius Estimator | Estimates propagation radius before action | Dependency map quality gates confidence |
| L4Q64-14 | Intent Obsolescence Detector | Detects stale user intent under new constraints/context | New-signal conflict lowers readiness; provenance gates confidence |
| L4Q64-15 | Marginal Evidence Gain Scheduler | Stops redundant proof gathering and selects next best evidence | Acquisition reliability and gain-estimate quality gate action |
| L4Q64-16 | Task Optionality Preserver | Penalizes vendor/schema/state lock-in and lost future branches | Migration readiness required |
| L4Q64-17 | Consistency Repair Min-Cut Engine | Removes contradiction with minimum semantic change surface | Invariant/backward compatibility preservation required |
| L4Q64-18 | Semantic Progress Velocity Meter | Measures verified convergence instead of activity volume | Acceptance traceability and measurement coverage gate confidence |
| L4Q64-19 | Value Density Compactor | Reduces UX/control complexity while preserving useful information | User validation and information preservation gate trust |
| L4Q64-20 | Recovery Path Diversity Planner | Requires independent recovery paths and reconstructability | Recovery drills provide evidence; single-path optimism scores poorly |

## Shared contract
- Exact input key set per concept. Missing or extra fields fail.
- All quantitative input must already be Q64.64; float convenience coercion is forbidden.
- Raw Q64 overflow and divide-by-zero are explicit failures.
- Readiness and confidence are Q64.64 in `[0,1]`.
- Candidate decisions are `ACT`, `HOLD`, `ESCALATE`, `FREEZE`.
- Candidate decisions have **no side-effect authority** until NEXY policy/evidence/JUDGE accepts them.
