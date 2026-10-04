# DESIGN LOCK — EPC Human Deliberation Integrity Fabric 20

STATUS: Lo4 proposal design, non-canonical, non-governing.

## Design Thesis
EPC can produce technically strong proposals and still fail the user if the review surface is cognitively hostile. HDIF-20 treats human reviewability as an engineering property without converting human factors into authority. The layer reorganizes and audits already-produced proposal/evidence material. It never creates Canon, casts KEEP/CUT, releases output, or changes NEXY runtime state.

## 20 Mechanisms
1. **Attention Budget Allocator (ABA)** — deterministic risk/irreversibility/uncertainty-weighted review-time allocation under an explicit supplied budget.
2. **Claim Compression Fidelity Gate (CCFG)** — measures weighted claim coverage after digest/compression so summaries cannot silently drop high-criticality claims.
3. **Counterargument Parity Gate (CPG)** — checks that known strong counterarguments remain visible to the reviewer.
4. **Uncertainty Salience Meter (USM)** — measures how much decision-relevant UNKNOWN weight is explicitly surfaced.
5. **Evidence Density Controller (EDC)** — detects evidence-starved and evidence-flooded claims under explicit min/max evidence-count policy.
6. **Cognitive Load Envelope (CLE)** — explicit weighted Q64.64 envelope over structural load factors; thresholds are supplied policy, never hidden constants.
7. **Reversibility Disclosure Gate (RDG)** — requires weighted disclosure coverage for irreversible effects.
8. **Reversible Trial Planner (RTP)** — finds the deterministic maximum-information reversible experiment set within an explicit risk budget and dependency closure.
9. **Decision Surface Pruner (DSP)** — Pareto-prunes dominated options for presentation only; dominance is not CUT/rejection and all candidates remain addressable.
10. **Review Order Neutralizer (RON)** — produces deterministic cyclic review orders to expose reviewers to alternatives under more than one primacy order without randomness.
11. **Dissent Preservation Score (DPS)** — measures weighted preservation of dissent/objections in the human packet.
12. **Human Override Visibility Gate (HOVG)** — measures whether action-level cancel/override/recovery paths that are declared required are visibly represented.
13. **Commitment Boundary Compiler (CBC)** — inserts explicit review checkpoints before committing/irreversible steps in a dependency-safe execution explanation.
14. **Decision Rationale Reconstruction Gate (DRRG)** — verifies that a user-facing rationale references required deciding evidence, assumptions and unresolved objections without storing hidden chain-of-thought.
15. **Reviewer Calibration Monitor (RCM)** — computes deterministic calibration/reliability from prior reviewer confidence against later verified outcomes.
16. **Stop-Review Sufficiency Gate (SRSG)** — non-compensatory gate: critical review dimensions must each satisfy explicit thresholds; a high score elsewhere cannot average away a blind spot.
17. **Dependency Explanation Scheduler (DES)** — stable topological ordering/layering so prerequisites are explained before dependents.
18. **Assumption-to-Question Compiler (AQC)** — turns already-declared assumptions into explicit reviewer questions ordered by Q64.64 decision impact.
19. **Explanation Drift Comparator (XDC)** — detects weighted loss or evidence-hash change across packet revisions.
20. **Deliberation Packet Compiler (DPC)** — deterministically assembles bounded human review surfaces and emits only REVIEWABLE / REPACKAGE_REQUIRED advisory state.

## Invariants
- No function has authority to KEEP, CUT, ACCEPT, REJECT, RELEASE or PROMOTE.
- No function calls NEXY runtime or mutates NEXY state.
- Numeric decision-support math is signed Q64.64 with signed-i128 raw bounds.
- Unit metrics are range checked to [0,1].
- Tie breaks use stable canonical IDs.
- Structural counts may use bounded integers; they never replace Q64.64 scoring.
- Critical malformed input throws/fails closed.
- Human-review thresholds/weights are caller-supplied policy, not invented hidden defaults.
- All pruning is presentation-only.
- Dissent, UNKNOWN and irreversible effects are never silently discarded.
- Rationale reconstruction uses explicit reference IDs, not private reasoning traces.

## Integration Shape
The intended future integration point is a shadow/advisory adapter after a proposal/evidence dossier exists and before human/EPC review UI rendering. Output is metadata suitable for NEXY::VIEW or a review tool. It does not sit in the authoritative CORE/JUDGE transition path and cannot satisfy release policy.

## Verification Plan
- TypeScript strict compile.
- Q64.64 boundary tests.
- Positive + negative/edge case for all 20 mechanisms.
- deterministic replay/permutation tests.
- no-float/no-random/no-wall-clock source scan.
- integration test proving compiled packet exposes advisory states only.
- hash manifest over exact tested source/test/design bytes.
