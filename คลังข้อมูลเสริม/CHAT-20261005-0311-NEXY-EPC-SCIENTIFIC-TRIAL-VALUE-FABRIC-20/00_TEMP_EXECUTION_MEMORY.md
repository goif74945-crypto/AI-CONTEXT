# Temporary Execution Memory — NEXY EPC Scientific Trial Value Fabric 20

CHAT_ID: `CHAT-20261005-0311-NEXY-EPC-SCIENTIFIC-TRIAL-VALUE-FABRIC-20`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
STATUS: `IN_PROGRESS`
CLASSIFICATION: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`

## Frozen objective
Design, implement, execute, repair, verify, and persist exactly 20 deterministic Q64.64 mechanisms that improve how EPC chooses and evaluates reversible experiments **before** any KEEP/CUT adjudication. The system optimizes evidence-learning value, falsification power, uncertainty reduction, trial ordering, and portfolio efficiency. It never adjudicates Canon, never spends another chat's vote rights, never changes NEXY state, and never promotes itself.

## Immutable scope
- Writable repository: `goif74945-crypto/AI-CONTEXT` only.
- Writable namespace: `คลังข้อมูลเสริม/CHAT-20261005-0311-NEXY-EPC-SCIENTIFIC-TRIAL-VALUE-FABRIC-20/**` plus one append-only unique vote record under `คลังข้อมูลเสริม/VOTES/**` after evidence is sufficient.
- Protected repositories: every repository whose name contains `NEXY.AI`; read-only inspection only.
- NEXY inspected repo/branch/commit: `goif74945-crypto/NEXY.AI-` / `NEXY.ai` / `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
- AI-CONTEXT observed pre-work HEAD for this mission: `40d254e297a724d7f379ad28c1c11ad1758ae336`.
- Canon promotion: forbidden.
- NEXY CORE/JUDGE/LAW/SWARM state mutation: forbidden.
- NEXY repository writes: forbidden.

## Authority pins
- Spec ID: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Spec SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- Current normalized source matrix: 837 requirement rows; the historical 215-entry registry is deprecated for current counting.
- Direct NEXY source observation: `packages/core/vnext-state-matrix.ts` assigns boot/execute to CORE, agents_done to SWARM, verified/accepted/rejected to JUDGE.
- Direct NEXY source observation: `core-kernel/src/engine/fixed128_math.rs` implements signed Q64.64 with i128 raw state and fail-closed overflow/divide-by-zero.
- Direct NEXY source observation: `packages/phase-f/lo3/governor.ts` carries Q64 in bigint with i128 range checks.

## Numeric compatibility conflict
- Rust core Fixed128 multiplication applies sign after magnitude truncation (toward zero).
- TypeScript Lo3 `q64Mul` uses signed bigint right shift `>> 64n`, which rounds negative fractional products toward negative infinity.
- STVF multiplicative metric domains are therefore constrained to non-negative `[0,1]` or non-negative cost/value quantities; signed outputs are produced by subtraction after non-negative products. This avoids claiming parity where direct source shows a signed rounding difference.

## Collision exclusions
Do NOT duplicate:
- NEXY Proposal Forge parsing/fingerprint/overlap/evidence pre-screen.
- Lo4 Promotion Gate readiness scoring.
- EPC Causal Proof 20: authority attestation, spec pinning, semantic duplicate proof, WIP gate, evidence coverage/depth, replay, Q64 conformance, impact/regression/dependency audit, promotion lattice, Canon collision, vote ledger/non-override/CUT/revision/freshness/novelty/dossier.
- EPC Court Foundry 20: vote-right enforcement, ballot lineage, commit pinning, court replay, disposition semantics, adjudication.
- EPC Verified Adjudication Calculus 20: evidence-gated adjudication package and vote machinery.

## STVF-20 frozen mechanism surface
1. Expected Value of Information
2. Minimax Regret Envelope
3. Reversibility Premium
4. Falsification Priority
5. Hypothesis Separation Distance
6. Gini Uncertainty Reduction
7. Evidence Independence Yield
8. Marginal Coverage Gain
9. Exact Trial Portfolio Knapsack
10. Multi-objective Trial Pareto Frontier
11. Sequential Evidence Stop Rule
12. Robustness Flip Radius
13. Sensitivity Bound Estimator
14. Control Contamination Index
15. Counterexample Yield
16. Replication Consistency
17. Forecast Calibration (Brier)
18. Holdout Leakage Guard
19. Option Value of Deferral
20. Deterministic Trial Schedule Compiler

## Vote budget for this CHAT_ID
- KEEP remaining: 1.
- CUT remaining: 1.
- DEFER / INSUFFICIENT_EVIDENCE / WIP do not consume either.
- Existing vote records are immutable; revisions are append-only evidence and never restore voting rights.

## Resume rule
Refresh AI-CONTEXT HEAD, read this file, inspect any newly-created competing work for semantic collision, continue from the latest verified artifact set, and never claim PASS without executed evidence.