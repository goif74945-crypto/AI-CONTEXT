# 01 TASK CONTRACT — EPC Preregistration Integrity Fabric 20 (PIF20)

> This contract narrows the initial mission after a fresh collision scan found concurrent `Scientific Trial Value Fabric 20` work covering trial value, falsification priority, stop rules, contamination, replication and holdout leakage. PIF20 therefore owns **protocol preregistration integrity / anti-post-hoc manipulation**, not trial-value optimization.

## OBJECTIVE
Create a standalone deterministic reference package with exactly 20 executable mechanisms that prevent post-hoc manipulation of experimental protocols before evidence is handed to EPC. PIF20 cannot vote, promote, mutate Canon, or change NEXY state.

## AUTHORITY
1. Current user directive defining EPC, Lo4, vote law and the absolute NEXY.AI no-write boundary.
2. NEXY-IGNIS canonical identity: SHA-256 `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
3. AI-CONTEXT execution/security/verification law.
4. Exact NEXY implementation read-only baseline `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
5. Executed evidence for PIF20.
6. PIF20 Lo4 design, advisory only.

## COLLISION EXCLUSIONS
PIF20 MUST NOT implement:
- KEEP/CUT ledger mechanics, immutable ballot rights, WIP-CUT law or court replay;
- promotion readiness, Canon collision scoring or proposal novelty scoring;
- generic adversarial/fault/metamorphic testing;
- formal verification of EPC's constitutional state machine;
- jurisprudence/precedent/recusal/burden-of-proof;
- social-choice ranking/manipulation analysis;
- scientific trial value / expected information / trial portfolio selection / falsification priority / holdout leakage / replication-value optimization;
- integration ecology / migration/blast-radius planning.

## EXACT 20 SYSTEMS
1. Hypothesis Precommit Seal (HPS)
2. Primary Metric Lock (PML)
3. Secondary Metric Declaration Registry (SMDR)
4. Slice Precommit Guard (SPG)
5. Analysis Plan Canonicalizer (APC)
6. Stopping Rule Precommit (SRP)
7. Protocol Amendment Ledger (PAL)
8. Outcome-Blind Amendment Gate (OBAG)
9. Result Peeking Detector (RPD)
10. Metric Substitution Detector (MSD)
11. Hypothesis Drift Detector (HDD)
12. Multiple-Comparison Declaration Gate (MCDG)
13. Selective Reporting Completeness Gate (SRCG)
14. Missing-Outcome Handling Lock (MOHL)
15. Negative Result Preservation Ledger (NRPL)
16. Exclusion Criteria Precommit Guard (ECPG)
17. Unblinding Boundary Gate (UBG)
18. Protocol Deviation Classifier (PDC)
19. Analysis Reproducibility Hash Gate (ARHG)
20. Research Integrity Dossier Compiler (RIDC)

## HARD INVARIANTS
- protocol decisions are based on logical sequence counters, never wall clock;
- all sealed set-like fields canonicalize before hashing;
- sealed hypothesis/primary metric/secondary metrics/slices/analysis plan/stopping rule cannot be silently changed after outcome visibility;
- amendments are append-only and parent-hash chained;
- post-outcome amendments fail closed;
- verdict-relevant metric/slice/comparison/exclusion not preregistered => fail;
- missing-outcome policy and unblinding boundary must match preregistration;
- negative outcomes cannot be omitted from the supplied result ledger;
- quantitative compliance ratios use checked signed Q64.64 only;
- binary floating point, random state and locale-dependent ordering are forbidden from authoritative source;
- RIDC emits only `READY_FOR_EPC_REVIEW` or `INSUFFICIENT_EVIDENCE`, with `canVote=false`, `canPromote=false`, `authoritative=false`;
- no score can override a failed hard gate, Canon/Law/JUDGE, or promotion authority.

## ACCEPTANCE CRITERIA
- TDD RED captured before implementation.
- strict TypeScript compile PASS.
- 20/20 system registry PASS.
- Q64 overflow/divide-zero/range negative paths PASS.
- preregistration immutability/post-outcome mutation negative paths PASS.
- deterministic canonicalization/permutation/replay PASS.
- property/stress checks PASS.
- authoritative-source scan finds no floating/random/wall-clock path.
- exact tested source manifest captured.
- GitHub persisted bytes read back after publication.
- protected NEXY repo receives zero write calls and its final head is re-observed.
- NEXY runtime integration remains NOT_VERIFIED unless separately executed under explicit authority.

## VOTE RIGHTS
KEEP=UNUSED; CUT=UNUSED. PIF20 test success alone does not spend either round. WIP/DEFER/INSUFFICIENT_EVIDENCE consume neither.

## STOP CONDITIONS
Freeze if correctness would require touching NEXY.AI, if a new collision makes the system materially duplicate, if tested bytes diverge from published bytes, or if a required PASS lacks matching executed evidence.
