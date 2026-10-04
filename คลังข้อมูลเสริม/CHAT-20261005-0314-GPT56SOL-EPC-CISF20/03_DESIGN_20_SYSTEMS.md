# CISF20 — Design of 20 Lo4 Systems

All systems are advisory. Numeric metrics are Q64.64 unless explicitly described as identifiers/booleans/count metadata.

| # | ID | System | Purpose | Failure / guard behavior |
|---:|---|---|---|---|
| 1 | HLBG64 | Hard-Law Breach Gate | Enumerate hard constraints breached in each scenario and quantify breached scenario mass. | Missing/invalid matrix fails validation; no breach is invented. |
| 2 | CMD64 | Compensation Mirage Detector | Detect when aggregate weighted score passes while at least one hard constraint fails. | Never converts the signal into ACCEPT/REJECT. |
| 3 | SLM64 | Slack Lattice Mapper | Compute signed score-minus-threshold slack for every scenario×constraint cell. | Overflow fails in Q64 substrate. |
| 4 | CFE64 | Critical Frontier Extractor | Find the constraint/scenario frontier with the worst slack. | Canonical tie ordering by IDs. |
| 5 | PFCS64 | Pairwise Failure Coupling Spectrometer | Measure excess co-deficit `E[ab]-E[a]E[b]` for every constraint pair. | Uses validated scenario weights; no float covariance. |
| 6 | TFCS64 | Triple Failure Coupling Spectrometer | Measure excess triple joint deficit over independent marginal product. | Constraint count is bounded to prevent combinatorial denial of service. |
| 7 | CDA64 | Compound Deficit Amplifier | Compare worst scenario risk with weighted mean risk to expose compound spikes. | Mean-zero case returns zero amplification, not divide-by-zero. |
| 8 | TRC64 | Tail Risk Concentrator | Measure how much total weighted risk is concentrated in the worst scenario contribution. | Zero-risk corpus returns zero concentration. |
| 9 | SIRS64 | Simpson Interaction Reversal Sentinel | Detect pairwise coupling whose aggregate sign is opposite to the same-sign coupling inside every eligible context. | Requires ≥2 contexts and ≥2 scenarios/context; zero-sign evidence does not trigger. |
| 10 | FCD64 | Failure Coupling Drift Radar | Measure pairwise coupling range across contexts. | Contexts and pairs are canonically ordered. |
| 11 | CBJM64 | Co-Breach Jaccard Matrix | Quantify scenario-weighted overlap between pairwise breach sets. | Empty union is explicit zero, not fake perfect similarity. |
| 12 | DFCF64 | Deterministic Failure Cluster Forge | Cluster constraints whose co-breach Jaccard meets the configured threshold. | Canonical union-find root selection prevents order-dependent clusters. |
| 13 | CAI64 | Constraint Ablation Influence | Recompute overall score after removing each constraint to reveal leverage/concentration. | Single-constraint case is `applicable:false`, not fabricated. |
| 14 | SAI64 | Scenario Ablation Influence | Recompute overall score after removing each scenario to reveal scenario dominance. | Single-scenario case is `applicable:false`. |
| 15 | PRW64 | Pareto Regression Witness | Compare to an optional compatible baseline; detect when current candidate has regressions and no improvements. | Constraint/scenario ID mismatch blocks comparison. |
| 16 | MRG64 | Minimax Regret Gauge | Compute worst scenario regret `1 - scenarioScore`. | Operates only on validated unit scores. |
| 17 | BRD64 | Behavioral Redundancy Detector | Find constraints with near-identical deficit profiles under weighted absolute distance. | Uses explicit epsilon; does not claim semantic duplication of modules/files. |
| 18 | ICM64 | Interaction Coverage Meter | Measure the fraction of constraint pairs with at least one observed joint breach witness. | With <2 constraints, coverage is vacuously 1 and pair count is 0. |
| 19 | MRCE64 | Minimal Risk Core Extractor | For each scenario, find a deterministic smallest high-contribution prefix that reaches risk budget. | If total risk cannot reach budget, returns `reachesBudget:false`. |
| 20 | ICC64 | Interaction Certificate Compiler | Hash canonical evaluation + baseline + 19 analyzer outputs into a replay certificate. | Certificate is evidence identity only; never an authority token. |

## Shared data model

`Evaluation` contains:

- candidate ID;
- release threshold;
- risk budget;
- redundancy epsilon;
- failure-cluster Jaccard threshold;
- 1–32 constraints with threshold/weight/hard flag;
- 1–256 scenarios with context ID, weight and a complete score vector.

Strict shape bounds are deliberate. PFCS is O(C²S) and TFCS is O(C³S). Unbounded `C` would turn a verifier into a denial-of-service primitive, which would be an impressively inefficient way to prove safety.

## Determinism contract

- constraint and scenario IDs are canonicalized lexicographically;
- no filesystem order participates;
- no random seed participates in production logic;
- no wall-clock value participates;
- certificate hashing uses canonical recursive key ordering and explicit BigInt raw encoding;
- property tests reorder input arrays and require identical certificate hashes.

## Authority contract

Every engine output includes:

- `authorityClass = LO4_AI_PROPOSAL_ONLY`
- `canMutateNexyState = false`
- `canPromote = false`
- `canOverrideCanon = false`
- `canCastEpcVote = false`

These flags are defense-in-depth metadata, not the only defense: the code exports no NEXY transition/promotion function.
