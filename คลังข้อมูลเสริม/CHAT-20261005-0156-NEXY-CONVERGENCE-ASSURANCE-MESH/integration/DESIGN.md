# Integration — Convergence Assurance Mesh

Status: `AI_PROPOSED_ADVISORY_PREFLIGHT`

## Order
ICG → CNS → EAP → IEQE → REC.

This sequence first proves that unresolved interpretation variance is non-decision-relevant, then checks excluded-context influence, plans exact verification, validates independent proof quorum, and finally seals restart/handoff equivalence.

## Release semantics
The coordinator's `READY` means only that these five auxiliary checks passed their local contracts. It explicitly emits classification `AI_PROPOSED_ADVISORY_PREFLIGHT_NOT_NEXY_JUDGE` and therefore cannot itself authorize NEXY output.

Every non-passing stage terminates with `FREEZE / MESH_STAGE_BLOCKED` and names the blocked stage.
