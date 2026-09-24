---
name: nexy-data
description: Govern the NEXY data lifecycle with explicit authority, provenance, integrity, transformation, persistence and evidence rules.
---

# NEXY Skill

## Identity
- Formal ID: `DATA-001`
- Name: `nexy-data`
- Family: DATA / EVIDENCE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Manage data lifecycle.

## Authority
Data mutation requires explicit ownership/scope; this Skill cannot invent provenance, storage authority or destructive permission.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current storage/state/data contracts at pinned HEAD.

## Scope
### In Scope
Data intake, classification, validation, provenance, transformation, persistence, access, retention/deletion when authorized, integrity and evidence.
### Out of Scope
Unknown-source data promoted to verified truth, unauthorized deletion/migration, provenance fabrication.

## Inputs
Universal inputs plus data object/source, lifecycle requirement, owner, schema and integrity/provenance rules.

## Outputs
Universal outputs plus data_classification, owner, provenance, integrity_status, lifecycle_state, transformations, persistence/evidence and next action.

## Workflow
Context → Authority/Owner → Validate Input/Schema → Provenance/Integrity → Authorized Transform/Persist → Verify → Evidence.

## Required Behavior
Unknown provenance remains UNVERIFIED/UNKNOWN; preserve lineage; explicit destructive gates.

## Forbidden Behavior
No silent overwrite, provenance stripping, fabricated hash/source, or cross-owner mutation.

## Architecture Constraints
Respect state/storage ownership and API/Core boundaries.

## Security Constraints
PII/secrets minimized and protected; tenant/access boundaries enforced.

## Compatibility Constraints
Schema/format/version changes require compatibility/migration analysis.

## Data Integrity
Integrity is first-class; invalid hash/content contradiction blocks verified use.

## Failure Handling
Missing provenance → UNVERIFIED; invalid integrity → FAIL; contradiction → BLOCK; unknown source → UNKNOWN.

## Freeze Conditions
Critical data-integrity/security/ownership uncertainty or destructive operation without gate.

## Validation
Schema, provenance, integrity, permissions, transformation, persistence/recovery and regression as applicable.

## Completion Criteria
Lifecycle action complete only with valid ownership, provenance/integrity and required evidence.

## Stop Conditions
Unknown owner/provenance for critical mutation, integrity failure, human gate or stale target.

## Checkpoint
Persist data identity, owner, provenance/integrity, lifecycle state and evidence.

## Resume
Refresh source/version/integrity before continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Data with unknown origin cannot be upgraded to VERIFIED because its format parses successfully.

## Non-Goals
This Skill does not invent storage or retention policy.

## Version
1.0.0
