# FSM Registry Validation

## Result
**PASS — namespace/structure registry**

FSM/state models: **8**

Namespaces are intentionally separated:
- DOC_C_EXECUTION
- KERNEL_RISK
- PIPELINE_RUN
- QUEUE_JOB
- CAPABILITY_GOVERNANCE
- CREATOR_PUBLICATION
- ANCHOR_PUBLICATION
- APP_LIFECYCLE

## Critical rule
Identical state labels across namespaces are not aliases automatically.

Examples:
- `FREEZE` in DOC-C execution != `FAILSAFE` kernel state != per-run `FREEZE`.
- `ACTIVE` in App lifecycle != capability `ACTIVE`.

## Observed implementation review points
1. DOC-C event set includes `cancel`, but current `VNEXT_TRANSITIONS` inspected has no cancel transition.
2. Capability source FSM contains `QUORUM_SIGNED` and `ACTIVE`; observed `CapabilityNodeStatus` currently has only PROPOSED/REVIEWED/ANCHORED/DEPRECATED.
3. App source lifecycle includes BUILT/SEALED; observed AppSpec status is DRAFT/ACTIVE/SUSPENDED/DEPRECATED and register() creates ACTIVE.
4. PipelineRun model does not itself expose a legal transition table in the inspected file.

These are **REVIEW points, not automatic final FAIL verdicts**.
