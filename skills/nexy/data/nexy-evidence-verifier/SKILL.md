---
name: nexy-evidence-verifier
description: Classify NEXY evidence as VERIFIED, UNVERIFIED, CONTRADICTED or UNKNOWN by testing claim fit, provenance, freshness and integrity.
---

# NEXY Skill

## Identity
- Formal ID: `DATA-005`
- Name: `nexy-evidence-verifier`
- Family: DATA / EVIDENCE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Classify evidence as VERIFIED, UNVERIFIED, CONTRADICTED or UNKNOWN.

## Authority
Evidence verification evaluates support for a claim; it does not redefine the claim/requirement.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Actual claim and evidence/provenance records.

## Scope
### In Scope
Claim-evidence fit, provenance, integrity, freshness, environment/HEAD binding and contradiction.
### Out of Scope
Generating missing evidence and calling it verified.

## Inputs
Universal inputs plus claim, evidence set and required evidence class.

## Outputs
Universal outputs plus classification, supporting/contradicting evidence, freshness, proof gaps and next proof.

## Workflow
Context → Authority/Claim → Evidence Inventory → Provenance/Integrity/Freshness → Claim Fit → Classification → Evidence.

## Required Behavior
No verification from existence alone; current-state claim needs current-state evidence.

## Forbidden Behavior
No cherry-picking around contradiction, no stale PASS as current PASS, no inferred execution.

## Architecture Constraints
Evidence class must match the boundary being claimed.

## Security Constraints
Sensitive evidence remains access-controlled/redacted.

## Compatibility Constraints
Claim/evidence schema/version identity preserved.

## Data Integrity
Integrity failures invalidate evidence fitness.

## Failure Handling
Missing proof = UNVERIFIED; conflicting proof = CONTRADICTED/UNKNOWN according to evidence.

## Freeze Conditions
Release/completion depends on unresolved critical evidence contradiction/gap.

## Validation
Golden verified/unverified/contradicted/unknown cases.

## Completion Criteria
Every evaluated claim has an evidence classification and traceable basis.

## Stop Conditions
Claim undefined or evidence inaccessible in a way that prevents safe classification.

## Checkpoint
Persist claim, evidence IDs, classification and gaps.

## Resume
Refresh evidence freshness/version.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A test file present but not run is UNVERIFIED execution evidence.

## Non-Goals
This Skill does not execute all missing tests.

## Version
1.0.0
