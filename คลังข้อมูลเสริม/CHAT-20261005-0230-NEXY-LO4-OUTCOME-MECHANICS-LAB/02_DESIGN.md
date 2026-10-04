# Design — Deterministic Outcome Mechanics

Status: Lo4_AI_PROPOSAL_ONLY / NON_CANONICAL.

Architecture:
Human objective/task state -> validated Q64.64 DTOs -> independent outcome engines -> Lo4 proposal capsule -> future NEXY LAW/JUDGE/promotion boundary.

Numeric substrate:
- TypeScript bigint raw Q64.64
- signed-128 raw range
- checked overflow, no wrap/saturation
- deterministic half-even decimal parsing/rendering
- no binary floating-point decision API
- deterministic canonical serialization

Failure law:
Invalid numeric domain, overflow, divide-by-zero, shape mismatch, violated hard constraint, or empty mandatory candidate set produces Lo4Freeze. The adapter converts it to an explicit FREEZE proposal instead of guessing.

Twenty engines:
1. Goal Distance Integrator — weighted residual distance.
2. Marginal Value Curve — diminishing marginal progress value.
3. Opportunity Cost Balancer — net value after resource/delay/risk costs.
4. Evidence Value of Information — expected value of another evidence action.
5. Reversibility Option Value — option value of reversible commitment.
6. Attention Return Optimizer — user value per attention unit.
7. Explanation Bandwidth Allocator — risk/evidence/novelty-aware explanation budget.
8. Progressive Disclosure Planner — brief/standard/staged depth.
9. Interruption Recovery Cost — urgency versus checkpoint/recovery loss.
10. Query Burden Minimizer — minimum high-yield clarification set.
11. Deadline Decay Engine — urgency/value amplification as deadlines approach.
12. Cost-of-Delay Scheduler — benefit density per duration.
13. Constraint Slack Meter — remaining budget and bottleneck detection.
14. Action Batch Cohesion — batching savings versus interference/coordination cost.
15. Context Switch Tax Estimator — switch benefit minus reorientation/error tax.
16. Utility Dominance Filter — Pareto frontier without forced scalarization.
17. Minimax Regret Engine — minimum worst-scenario regret.
18. Robust Lower-Bound Selector — strongest conservative outcome.
19. Recovery Leverage Ranker — expected unblock value per recovery effort.
20. Residual Work Mass Gate — prevents false completion while work/evidence mass remains.

Authority invariant:
Every adapter envelope is layer=Lo4, authority=PROPOSAL_ONLY, promotionRequired=true, canonical=false. No engine can promote itself, execute side effects, call providers, or mutate NEXY state.
