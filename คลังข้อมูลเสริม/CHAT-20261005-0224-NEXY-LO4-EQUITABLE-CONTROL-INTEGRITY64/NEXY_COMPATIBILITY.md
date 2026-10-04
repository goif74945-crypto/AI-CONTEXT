# Future NEXY.AI Compatibility Boundary

Status: `DESIGN_COMPATIBILITY_PROPOSAL / NOT_INTEGRATED / NOT_CANON`

## Why it fits the documented direction
The loaded NEXY context emphasizes explicit authority, deterministic/fail-closed control, auditability, provenance, safe FREEZE behavior, and human control. Equitable Control Integrity64 adds a proposed audit plane around those mechanisms without weakening them.

It does not say “do not freeze”. It asks whether the real operational burden of freezing/verification/recovery is distributed differently across evaluator-defined cohorts and surfaces evidence for human/policy review.

## Potential future data adapters
- audit/event log aggregates -> FREEZE_EQ64;
- verification challenge/step metrics -> VERIFY_TAX64;
- retrospective adjudication labels -> UNNECESSARY_FREEZE64;
- recovery workflow records -> RECOVERY_EQ64;
- policy-margin evaluation records -> THRESHOLD_FRAGILITY64.

## Required integration constraints
1. Cohort membership must come from an authorized, privacy-reviewed source; this library must not infer it.
2. Prefer aggregation/minimization so raw sensitive personal data is not copied into this audit package.
3. Burden units and thresholds must be explicit, versioned policy inputs.
4. Cohort definitions, measurement windows, and denominators require provenance.
5. Small-sample privacy/statistical policy must be stricter than this reference `minSample` gate if real sensitive cohorts are used.
6. Audit findings require human/legal/domain interpretation; gap detection alone is not a legal fairness conclusion.
7. Production adoption needs exact runtime integration tests and deployment evidence.

## Non-goals
- demographic inference;
- legal compliance determination;
- causal discrimination proof;
- automatic policy rewriting;
- automatic release/promotion decisions;
- weakening safety controls to equalize a metric.
