---
name: nexy-integrity
description: Verify NEXY data or evidence hash and content integrity as DATA-004 without conflating this identity with VLT-005 vault integrity.
---

# NEXY Skill

## Identity
- Formal ID: `DATA-004`
- Name: `nexy-integrity`
- Family: DATA / EVIDENCE
- Version: `1.0.0`
- Status: `MATERIALIZED`
- Identity note: distinct from `VLT-005 nexy-integrity`.

## Objective
Verify hash/content integrity.

## Authority
Integrity verification observes content consistency; it cannot repair or overwrite corrupted data without separate authority.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Actual bytes/content and real expected digest/version when available.

## Scope
### In Scope
Hash comparison, content identity, corruption/tamper detection and integrity evidence.
### Out of Scope
Invented expected hash, automatic repair, vault lifecycle semantics owned by VLT-005.

## Inputs
Universal inputs plus content/artifact, expected hash/version and algorithm when established.

## Outputs
Universal outputs plus integrity_status, observed/expected identity metadata, mismatch evidence and next action.

## Workflow
Context → Authority → Identify Expected Integrity Rule → Compute/Compare if Possible → Classify → Evidence.

## Required Behavior
If hash cannot actually be computed/verified, report HASH_UNAVAILABLE/UNKNOWN.

## Forbidden Behavior
No fabricated digest, no PASS from filename/size only, no silent corruption repair.

## Architecture Constraints
Respect data ownership; integrity check does not authorize mutation.

## Security Constraints
Use approved cryptographic mechanisms when source requires them; do not expose sensitive content unnecessarily.

## Compatibility Constraints
Algorithm/version changes require explicit provenance/compatibility.

## Data Integrity
Mismatch = FAIL/CONTRADICTED for the checked identity.

## Failure Handling
Unavailable expected hash/content => NOT_VERIFIED rather than PASS.

## Freeze Conditions
Critical authoritative data/evidence fails integrity or cannot be safely resolved.

## Validation
Known-good/known-bad hash/content cases and provenance binding.

## Completion Criteria
Integrity result is based on actual content and established expected identity.

## Stop Conditions
Missing critical expected identity or unsafe access.

## Checkpoint
Persist object/version, algorithm, observed/expected status and evidence.

## Resume
Re-read content/version before recheck.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Matching file size does not prove content integrity.

## Non-Goals
This Skill does not manage Vault revisions or commits.

## Version
1.0.0
