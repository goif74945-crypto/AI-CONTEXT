# NEXY Lo4 Equitable Control Integrity64 — Design

**Classification:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANON / AUDIT_ONLY`

## Design premise
A verify-first control system can still create unequal operational burden even when its core safety rules are internally consistent. If one cohort is frozen more often, challenged with more verification steps, recovers more slowly, or clusters closer to policy thresholds, the system should surface that evidence rather than assume “same rule” means “same practical treatment”.

This package audits aggregate outcomes. It does not infer protected attributes, determine legal fairness, establish causation, or choose policy thresholds.

## Shared Q64.64 substrate
- signed 128-bit raw domain;
- exactly 64 fractional bits;
- string/rational decimal construction;
- binary `Number` rejected at Q64 construction boundaries;
- integer BigInt host arithmetic;
- explicit overflow/division errors;
- deterministic truncation toward zero for fixed-point mul/div;
- no silent saturation.

Counts are nonnegative BigInt. Rates and averages are converted into Q64.64 before comparison.

## 1. FREEZE_EQ64 — Freeze Burden Disparity Auditor
### Question
Are valid evaluation cohorts experiencing materially different FREEZE rates?

### Inputs
Per cohort: `total`, `freezes`. Policy: `minSample`, Q64.64 `maxFreezeRateGap`.

### Output
Per-cohort freeze rates plus max-minus-min gap. Emits `PARITY_WITHIN_LIMIT` or `FREEZE_FAIRNESS_REVIEW`.

### Failure semantics
Insufficient sample freezes the audit. Impossible counts throw. It does not smooth or impute missing cohorts.

## 2. VERIFY_TAX64 — Verification Burden Disparity Auditor
### Question
Does one cohort have to pay substantially more evidence/verification burden per request?

### Inputs
Per cohort: `total`, Q64.64 `evidenceBurdenTotal`. The burden unit must be defined by the evaluator (for example normalized challenge-step cost, human effort, or verified latency-equivalent cost).

### Output
Per-cohort average burden and gap against explicit Q64.64 policy.

### Authority boundary
The library never invents burden weights. Weighting semantics are external policy and must be documented before use.

## 3. UNNECESSARY_FREEZE64 — Avoidable Freeze Disparity Auditor
### Question
After later evidence establishes that some freezes were avoidable, is that avoidable-freeze rate concentrated in one cohort?

### Inputs
`total`, `freezes`, `avoidableFreezes` per cohort.

### Output
Avoidable-freeze rate per total requests and disparity gap.

### Truth boundary
“avoidable” must come from a separately verified retrospective label. This system does not infer that label.

## 4. RECOVERY_EQ64 — Recovery Opportunity / Time Disparity Auditor
### Question
After a freeze/failure state, are cohorts similarly able to recover, and with similar recovery time?

### Inputs
`recoveryEligible`, `recovered`, Q64.64 `recoveryDurationTotal`, plus cohort total and explicit rate/time gap limits.

### Output
Recovery-rate gap and average-recovery-time gap.

### Failure semantics
No recovered observation means average recovery time is unobservable, so the audit freezes rather than pretending zero time.

## 5. THRESHOLD_FRAGILITY64 — Policy-Boundary Fragility Auditor
### Question
Is one cohort disproportionately concentrated near a freeze/verification threshold, making small policy changes likely to affect it more?

### Inputs
`total`, `nearBoundary`, and explicit Q64.64 allowed gap. The evaluator defines what numeric margin counts as “near boundary” before data collection.

### Output
Near-boundary rate and disparity gap.

### Non-claim
This is sensitivity evidence, not proof that the threshold is unfair or wrong.

## Integrated suite
`auditEquitableControlPack()` executes all five audits over the same evaluator-supplied cohort aggregates. The integrated output can be `READY_FOR_HUMAN_REVIEW` only when every audit is inside policy. Any failed audit yields `FREEZE_FAIRNESS_REVIEW`.

The suite has no release, deployment, Canon, user-law, or promotion method.
