---
name: nexy-revision
description: Enforce NEXY revision semantics: no overwrite, new content creates a new revision, and monotonic revision/hash lineage is preserved and evidenced.
---

# NEXY Skill

## Identity
- Formal ID: `VLT-003`
- Name: `nexy-revision`
- Family: VAULT / STATE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
No overwrite; new content creates a new revision with monotonic revision/hash semantics.

## Authority
Revision rules are governed by the Skill specification and applicable Vault/source contracts. This Skill cannot rewrite existing revision history or invent revision/hash values.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current revision/Vault implementation and evidence at the pinned target when applicable.

## Scope
### In Scope
Revision creation, monotonic ordering, parent/lineage linkage, content identity/hash evidence, immutable-history checks and conflict reporting.
### Out of Scope
In-place overwrite, fabricated hashes, arbitrary renumbering, destructive compaction or commit authorization owned by `VLT-004`.

## Inputs
Universal inputs plus artifact ID, prior revision/version when required, new content identity, expected revision state and integrity/provenance evidence.

## Outputs
Universal outputs plus revision identity/number, lineage link, integrity/hash status, conflicts, persistence evidence and next action.

## Workflow
Context → Authority → Resolve Artifact/Current Revision → Validate No-Overwrite Rule → Determine Legal Next Revision → Verify Content Identity Rule → Create/Inspect Revision if authorized → Validate Monotonic Lineage → Evidence.

## Required Behavior
Existing revision content remains immutable; new content becomes a new revision; monotonic numbering/lineage and hash semantics follow the established contract.

## Forbidden Behavior
No revision overwrite, gap masking, fabricated revision number/hash, reuse of stale parent state or silent conflict resolution.

## Architecture Constraints
Revision lifecycle is subordinate to Vault ownership and interoperates with commit/concurrency controls.

## Security Constraints
Only authorized writers may create revisions; revision evidence must not expose protected content unnecessarily.

## Compatibility Constraints
Revision schema/hash/version changes require explicit compatibility and migration analysis.

## Data Integrity
Revision identity, ordering, content hash/identity and lineage must be internally consistent according to the governing contract.

## Failure Handling
Version conflict, invalid predecessor, hash mismatch or persistence failure is explicit and does not mutate prior history.

## Freeze Conditions
Critical revision corruption, unauthorized rewrite, irreconcilable lineage conflict or fabricated integrity evidence.

## Validation
Create-next-revision, repeated/stale writer, immutable prior revision, monotonic ordering, hash mismatch and regression cases as applicable.

## Completion Criteria
The resulting revision state preserves immutable history, monotonic lineage and required integrity evidence.

## Stop Conditions
Current revision cannot be established, critical conflict is unresolved, target is stale or requested operation requires rewriting history.

## Checkpoint
Persist artifact/revision IDs, prior/current version, lineage status, integrity evidence, conflict state and resume point.

## Resume
Refresh current artifact revision and conflict state before any new revision action.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Editing existing content creates revision N+1 rather than mutating revision N.

## Non-Goals
This Skill does not authorize final commit semantics or merge concurrent writers by guessing.

## Version
1.0.0
