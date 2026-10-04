# Future NEXY Integration Guide

Status: **AI proposal only. No NEXY.AI integration was performed.**

## Intended insertion points
1. **Directive ingress**: translate already-validated product input into `InputRequirement` plus explicit modality `IntentContract` records.
2. **Before RUN admission**: require Input Cohesion + Multimodal Intent Equivalence PASS.
3. **Task lifecycle**: issue an epoch token when a directive becomes active. A superseding directive or cancel advances the epoch before downstream commit can occur.
4. **Reusable computations**: wrap cache adapters with the provenance namespace. A miss falls back to normal governed recomputation; a foreign/tampered explicit entry freezes.
5. **Candidate result streaming**: route chunks through Completion Boundary Integrity before anything is labeled complete/final.
6. **Downstream authority**: pass only a verified interaction snapshot/release candidate to existing LAW/JUDGE/release logic. This suite never substitutes for those authorities.

## Compatibility constraints
- Do not map a FREEZE here to an automatic retry that changes semantics.
- Do not turn missing input or modality divergence into inferred defaults.
- Do not use wall-clock timestamps as epoch authority.
- Do not log raw secrets merely to make canonical fingerprints reproducible.
- Do not accept cache entries whose namespace/version is only “close enough”.
- Do not treat CBIG PASS as truth/factuality PASS; it proves stream completeness/integrity only.
- Do not copy these modules into NEXY.AI without a separately authorized integration task and an exact requirement crosswalk.

## Suggested adoption phases
### Phase A — shadow observation
Compute decisions/fingerprints alongside existing paths without changing production outcome. Compare false-positive/false-negative behavior.

### Phase B — advisory blocking
Surface divergence/truncation incidents to operators while preserving existing canonical execution authority.

### Phase C — governed gate
Only after requirements, threat model, storage/concurrency semantics and E3/E4 tests are accepted should any gate become release-blocking.

### Phase D — operational proof
Collect target-runtime evidence for crash/retry/concurrency, stale worker cancellation, cache migration, multimodal adapters and real streaming providers. Production claims require evidence beyond this reference lab.
