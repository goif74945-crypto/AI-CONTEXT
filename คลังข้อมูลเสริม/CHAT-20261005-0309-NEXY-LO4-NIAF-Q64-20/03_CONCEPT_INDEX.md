# NIAF-20 Concept Index

All concepts below are **AI-proposed Lo4 designs**, not Canon.

| ID | System | Purpose | Primary invariant |
|---|---|---|---|
| C01 | Epistemic Entropy Ledger | Aggregate unresolved critical uncertainty | deterministic Q64 ledger only |
| C02 | Marginal Information Gain | Estimate entropy reduction adjusted by reliability | negative gain clamps to zero |
| C03 | Value-of-Information Scorer | Compare expected benefit to acquisition costs | dimension binding required |
| C04 | User Burden Budget | Prevent excessive clarification load | explicit unit budget |
| C05 | Privacy Cost Meter | Accumulate declared privacy exposure | no inferred privacy score |
| C06 | Latency Budget Meter | Bound acquisition latency using explicit ticks | no wall clock |
| C07 | Irreversibility Risk Guard | Bound one-way/high-impact acquisition actions | explicit unit budget |
| C08 | Ambiguity Partition Resolver | Prefer questions that split plausible branches | balanced, relevant, low-burden favored |
| C09 | Question Novelty Filter | Penalize semantically repeated questions | deterministic Jaccard over declared features |
| C10 | Answer Sensitivity Ranker | Prioritize variables whose answer changes output most | score = delta × uncertainty × criticality |
| C11 | Missing Variable Impact | Quantify one unresolved variable's impact | unit-bounded inputs |
| C12 | Evidence Conflict Probe Ranker | Prioritize unresolved conflicting evidence | conflict increases score, coverage reduces urgency |
| C13 | Exact Probe Portfolio Optimizer | Select globally best bounded action set | exact subset search ≤20, no duplicate dimension |
| C14 | Stop-or-Ask Frontier | Decide ASK / DO_NOT_ASK / SUGGEST_FREEZE | only budget-admissible actions compete |
| C15 | Explicit-Tick Staleness Decay | Decay freshness without nondeterministic time | age supplied as ticks |
| C16 | Evidence Saturation Detector | Stop repeated low-gain acquisition | bounded recent-gain window |
| C17 | Calibration Loss Tracker | Measure mismatch between predicted resolution and outcome | deterministic mean absolute loss |
| C18 | Batch Query Composer | Compose a small burden-bounded clarification batch | deterministic rank + budget |
| C19 | Fallback Freeze Evidence Packager | Preserve unresolved dimensions and available actions | proposal only, cannot mutate Core |
| C20 | Acquisition Envelope Compiler | Compose portfolio + recommendation + authority evidence | authority/CANON effect hard locked |

## Why this family is useful
A verify-only system that freezes on ambiguity still needs a disciplined way to reduce ambiguity without asking every possible question. NIAF-20 explores that missing optimization layer while preserving the existing rule that only CORE/JUDGE/LAW can decide state and release.
