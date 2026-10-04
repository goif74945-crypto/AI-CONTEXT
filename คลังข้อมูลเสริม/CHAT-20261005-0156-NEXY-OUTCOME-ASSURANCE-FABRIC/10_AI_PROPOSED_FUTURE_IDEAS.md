# AI-Proposed Future Ideas

Everything in this file is **CONCEPT ONLY / NOT IMPLEMENTED / NOT NEXY REQUIREMENT**.

## 1. Provenance-Bound Outcome Observation
Bind every observed field to evidence identity, collection method, freshness window, and authority. ODV could then distinguish `value known` from `value supplied by an untrusted worker` instead of treating JSON presence as observation trust.

## 2. Causal Outcome Attribution
Given an execution trace plus outcome deltas, compute a conservative contribution graph showing which authorized steps are consistent with each outcome change. This must avoid claiming causality from correlation without intervention evidence.

## 3. Outcome Contract Temporal Persistence
Some outcomes must remain true for a duration, not just one checkpoint. Add explicit persistence windows and repeated observation capsules without turning current-time access into hidden core behavior.

## 4. Verified Approximate Recovery Solver
For >16 actions, use an external ILP/SAT/SMT solver adapter that emits a proof/checkable certificate. The core should independently verify the selected plan against the exact outcome contract.

## 5. Multi-Principal Outcome Negotiation
Compile outcome contracts where multiple authorized humans/roles control different criteria. Conflicts should remain explicit instead of averaging incompatible authority.

## 6. Outcome Explanation Surface
Generate a minimal human-facing explanation: which outcomes passed, which failed, what is unknown, and what repair would close the gap. Explanation generation must be downstream of the deterministic result and must not alter it.
