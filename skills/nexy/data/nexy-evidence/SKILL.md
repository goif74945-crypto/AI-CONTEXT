---
name: nexy-evidence
description: Manage NEXY evidence objects with source category, origin, description, verification state and traceability without treating existence as proof.
---

# NEXY Skill

## Identity
- Formal ID: `DATA-002`
- Name: `nexy-evidence`
- Family: DATA / EVIDENCE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Manage Evidence objects and supported source categories such as DOCUMENT, WEB, MODEL, USER_INPUT and INTERNAL.

## Authority
Evidence supports claims; it does not create normative authority or automatically prove a claim.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Actual source/artifact/run identity for each evidence record.

## Scope
### In Scope
Evidence identity, category, origin, description, claim linkage, freshness, verification status and storage references.
### Out of Scope
Fabricated evidence, unbound screenshots/logs treated as current proof, hidden source substitution.

## Inputs
Universal inputs plus claim, evidence source/category, origin, revision/run/environment metadata.

## Outputs
Universal outputs plus evidence_record, claim_links, freshness, verification_state and gaps.

## Workflow
Context → Authority → Claim → Acquire/Identify Evidence → Bind Provenance/Revision → Validate → Record.

## Required Behavior
WHAT → WHERE → HOW → RESULT → EVIDENCE; distinguish static/runtime/test/deployment evidence.

## Forbidden Behavior
No PASS from file existence; no historical evidence represented as current; no source laundering.

## Architecture Constraints
Evidence storage/ingestion does not override system state ownership.

## Security Constraints
Redact secrets/PII and restrict sensitive evidence access.

## Compatibility Constraints
Preserve evidence schema/version and claim linkage.

## Data Integrity
Hash/content integrity is verified when required; otherwise mark unavailable/unverified.

## Failure Handling
Stale/missing/unbound evidence remains insufficient.

## Freeze Conditions
Critical completion/release depends on missing, contradictory or unverifiable evidence.

## Validation
Schema, provenance, freshness, claim binding and evidence-level fitness.

## Completion Criteria
Evidence record is traceable and its verification/freshness limits are explicit.

## Stop Conditions
Source identity unavailable or sensitive evidence cannot be handled safely.

## Checkpoint
Persist evidence ID/source/revision/claim/status.

## Resume
Revalidate freshness and source identity.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A prior test report is STALE for a different HEAD even if the test name is unchanged.

## Non-Goals
This Skill does not by itself make a claim true.

## Version
1.0.0
