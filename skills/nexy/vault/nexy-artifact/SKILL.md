---
name: nexy-artifact
description: Manage NEXY Artifact lifecycle and lineage under Vault rules while preserving ownership, version history, compatibility, integrity evidence, and authorized mutation boundaries.
---

# NEXY Skill

## Identity
- Formal ID: `VLT-002`
- Name: `nexy-artifact`
- Family: VAULT / STATE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Manage Artifact lifecycle.

## Authority
Artifact operations follow established Vault/source contracts and task authorization. This Skill cannot overwrite history, invent ownership, or bypass revision/commit rules.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current artifact/Vault contracts and pinned implementation/evidence when applicable.

## Scope
### In Scope
Artifact identity, creation/read/update intent, linkage to revisions, ownership, metadata, compatibility, persistence status and lifecycle evidence.
### Out of Scope
Silent content overwrite, invented artifact state, unauthorized ownership transfer, commit/revision semantics owned by their dedicated Skills except as dependencies.

## Inputs
Universal inputs plus artifact identity or creation request, owning scope/project, desired operation, expected version/state and applicable integrity/provenance evidence.

## Outputs
Universal outputs plus artifact state, lineage references, version/revision links, conflicts, evidence and next action.

## Workflow
Context → Authority → Artifact Contract → Resolve Ownership/State → Validate Operation → Delegate Revision/Commit/Integrity checks as required → Execute Authorized Change → Validate → Evidence.

## Required Behavior
Preserve artifact identity and lineage; route content changes through revision semantics where required; keep unknown ownership/state explicit.

## Forbidden Behavior
No in-place historical overwrite, fabricated artifact, hidden ownership change, skipped validation or fake persistence success.

## Architecture Constraints
Artifact lifecycle operates inside Vault and depends on revision/commit semantics rather than replacing them.

## Security Constraints
Artifact reads/writes obey applicable authorization and data-minimization boundaries.

## Compatibility Constraints
Artifact metadata/schema changes require consumer and migration impact review when applicable.

## Data Integrity
Artifact state must remain traceable to its current revision/lineage evidence.

## Failure Handling
Missing artifact, invalid state, conflict or persistence failure returns explicit failure/unknown status.

## Freeze Conditions
Unauthorized artifact mutation, lineage corruption, destructive ambiguity or critical integrity conflict.

## Validation
Positive/negative lifecycle cases, missing/conflicting object cases, revision linkage, authorization and regression checks as applicable.

## Completion Criteria
Artifact lifecycle result is authorized, source-aligned, lineage-preserving and supported by required evidence.

## Stop Conditions
Unknown authoritative artifact identity/owner, stale target, required destructive operation without gate or unresolved lineage conflict.

## Checkpoint
Persist artifact ID, owner/scope, operation, current lineage, evidence and unresolved issues.

## Resume
Re-read artifact and current lineage before continuing mutation or verification.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Updating artifact content creates/uses a revision path when the governing contract requires immutable history.

## Non-Goals
This Skill does not redefine revision numbering or commit concurrency rules.

## Version
1.0.0
