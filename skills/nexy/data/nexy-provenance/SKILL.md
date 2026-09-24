---
name: nexy-provenance
description: Ensure important NEXY evidence and data record source, origin, description, hash when real, revision and verification without invented lineage.
---

# NEXY Skill

## Identity
- Formal ID: `DATA-003`
- Name: `nexy-provenance`
- Family: DATA / EVIDENCE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Ensure important evidence records source, origin, description, hash and verification.

## Authority
Provenance records lineage; it cannot invent source/history or convert unknown lineage into trusted lineage.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Actual source/commit/run/artifact metadata.

## Scope
### In Scope
Source identity, origin, description, revision/time source, transformations, hash when genuinely computed, verification status.
### Out of Scope
Synthetic hashes, assumed origin, retroactive unverifiable lineage.

## Inputs
Universal inputs plus object/evidence and source/transform metadata.

## Outputs
Universal outputs plus provenance_chain, hash_status, source_refs, transformation_chain and verification.

## Workflow
Context → Identify Source → Capture Origin/Revision → Record Transform Chain → Integrity Check → Verify/Mark Unknown → Evidence.

## Required Behavior
Use HASH_UNAVAILABLE when hash is not actually available; preserve every material transformation.

## Forbidden Behavior
No fake cryptographic proof, no dropping intermediate lineage, no source substitution.

## Architecture Constraints
Provenance follows data/evidence ownership boundaries.

## Security Constraints
Do not embed secrets/credentials in provenance metadata.

## Compatibility Constraints
Preserve stable identifiers/version lineage.

## Data Integrity
Chain gaps remain explicit.

## Failure Handling
Missing lineage => UNVERIFIED/PARTIAL.

## Freeze Conditions
Critical release/data trust depends on unresolvable provenance.

## Validation
Source identity, revision, transform chain and real hash verification where applicable.

## Completion Criteria
Provenance is complete enough for the claim/use case and unresolved gaps are explicit.

## Stop Conditions
Critical source identity unavailable or unsafe sensitive metadata.

## Checkpoint
Persist chain and verification state.

## Resume
Revalidate source/revision/hash.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- “Generated from source file X” requires the exact source version and transformation, not just the filename.

## Non-Goals
This Skill does not guarantee content correctness.

## Version
1.0.0
