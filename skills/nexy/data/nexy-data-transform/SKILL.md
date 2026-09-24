---
name: nexy-data-transform
description: Transform NEXY data through INPUT, TRANSFORM, OUTPUT and PROVENANCE while preserving schema, lineage, integrity and reversibility requirements.
---

# NEXY Skill

## Identity
- Formal ID: `DATA-007`
- Name: `nexy-data-transform`
- Family: DATA / EVIDENCE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Transform data while preserving provenance: INPUT → TRANSFORM → OUTPUT → PROVENANCE.

## Authority
Transformation cannot broaden use rights, erase source constraints or overwrite authoritative data without explicit authority.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Actual input schema/source and authorized transform requirement.

## Scope
### In Scope
Schema-preserving/defined transformation, normalization, conversion, derived data, provenance/integrity/evidence.
### Out of Scope
Unsupported inference inserted as source fact, silent lossy transform, unapproved overwrite.

## Inputs
Universal inputs plus input data/provenance, transform specification, output schema and integrity constraints.

## Outputs
Universal outputs plus output data/reference, transform steps, provenance chain, integrity/validation and rollback/reversibility note.

## Workflow
Context → Authority → Input/Schema Validation → Transform → Output Validation → Provenance/Integrity → Evidence.

## Required Behavior
Record exact transformation and preserve distinction between original and derived content.

## Forbidden Behavior
No silent data loss, no invented fields/facts, no provenance stripping.

## Architecture Constraints
Transform occurs within legal data ownership boundary.

## Security Constraints
Sensitive data minimization and permission constraints survive transformation.

## Compatibility Constraints
Output schema/version validated for consumers.

## Data Integrity
Hash/lineage/invariants checked as required; lossy transforms explicitly authorized.

## Failure Handling
Invalid input/output/provenance => FAIL/BLOCKED.

## Freeze Conditions
Critical integrity loss, unknown destructive transform or unauthorized sensitive-data change.

## Validation
Golden/negative transform cases, schema, round-trip/reversibility where required, provenance and regression.

## Completion Criteria
Output validates and provenance/integrity are traceable.

## Stop Conditions
Transform spec/schema unknown or destructive/sensitive action lacks authority.

## Checkpoint
Persist input identity, transform version, output identity and provenance.

## Resume
Refresh input/version before rerun.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A normalized record must still reference the exact source record and transform.

## Non-Goals
This Skill does not decide whether derived content is verified evidence.

## Version
1.0.0
