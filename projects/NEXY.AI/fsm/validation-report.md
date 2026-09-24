# FSM Registry Validation

## Result
**PASS — namespace/source-structure registry**

FSM/state models: **8**

Namespaces:
- `DOC_C_EXECUTION` → `FSM-EXECUTION`
- `KERNEL_RISK` → `FSM-RISK-INTELLIGENCE`
- `PIPELINE_RUN` → `FSM-PIPELINE-RUN-OBSERVED`
- `QUEUE_JOB` → `FSM-QUEUE-JOB`
- `CAPABILITY_GOVERNANCE` → `FSM-CAPABILITY-REGISTRY`
- `CREATOR_PUBLICATION` → `FSM-CREATOR-PUBLICATION`
- `ANCHOR_PUBLICATION` → `FSM-ANCHOR-PUBLICATION`
- `APP_LIFECYCLE` → `FSM-APP-LIFECYCLE`

## Critical rule
Identical state labels across namespaces are not aliases automatically.

Examples:
- `FREEZE` in DOC-C execution != kernel `FAILSAFE` != per-run `FREEZE`.
- `ACTIVE` in App Lifecycle != capability admission `ACTIVE`.

## Observed implementation review points
1. DOC-C event set includes `cancel`, but current inspected `VNEXT_TRANSITIONS` has no cancel transition row.
2. Capability canonical admission FSM is PROPOSED→REVIEWED→QUORUM_SIGNED→ANCHORED→ACTIVE; observed `CapabilityNodeStatus` omits QUORUM_SIGNED/ACTIVE and includes DEPRECATED.
3. Canonical App Lifecycle is CREATED→BUILT→SEALED→DEPLOYED→ACTIVE with later FROZEN/ARCHIVED/TERMINATED paths; observed `AppSpec.status` is a separate implementation model using DRAFT/ACTIVE/SUSPENDED/DEPRECATED.
4. PipelineRun remains an implementation-only state model and is not merged into the global execution FSM.

These are review points, not automatic final FAIL verdicts.
