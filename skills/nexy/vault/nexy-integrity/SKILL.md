---
name: nexy-integrity
description: Verify NEXY Vault artifact/revision/commit integrity as formal identity VLT-005, preserving lineage and storage-integrity semantics without conflating this Skill with DATA-004 evidence/data integrity.
---

# NEXY Skill

## Identity
- Formal ID: `VLT-005`
- Name: `nexy-integrity`
- Family: VAULT / STATE
- Version: `1.0.0`
- Status: `MATERIALIZED`
- Identity note: distinct from `DATA-004 nexy-integrity`.

## Objective
Verify artifact integrity.

## Authority
Vault-integrity verification follows the established Vault, Artifact, Revision, and Commit contracts. This Skill observes and validates integrity; it does not authorize silent repair, history rewrite, or semantic truth claims.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current Vault/revision/commit implementation and pinned evidence when applicable.

## Scope
### In Scope
Vault object identity, revision/commit lineage integrity, expected-versus-observed content/hash/version checks, chain consistency, corruption/tamper detection and integrity evidence.
### Out of Scope
Generic DATA-004 evidence integrity, invented expected hashes, automatic repair, destructive history rewrite, semantic adjudication or unauthorized mutation.

## Inputs
Universal inputs plus Vault object/revision/commit identity, expected hash/version/lineage when established, observed content/state and applicable provenance.

## Outputs
Universal outputs plus integrity verdict, expected/observed identity metadata, lineage/chain status, mismatch/corruption evidence and next action.

## Workflow
Context → Authority → Resolve Vault Object/Version → Establish Expected Integrity Rule → Verify Content/Hash/Lineage if Possible → Classify → Cross-check Revision/Commit Chain → Evidence.

## Required Behavior
Use actual object/version/content/lineage evidence; keep unavailable expected identity as UNKNOWN/NOT_VERIFIED; treat proven mismatch as explicit integrity failure.

## Forbidden Behavior
No fabricated digest, no PASS from filename/size/presence alone, no silent corruption repair, no history rewrite, no identity merge with DATA-004.

## Architecture Constraints
VLT-005 is specific to Vault Artifact/Revision/Commit integrity and depends on their state ownership; it does not replace DATA-004 or CORE/LAW/JUDGE authority.

## Security Constraints
Use established cryptographic mechanisms when required; avoid exposing protected content; unauthorized or tampered state fails closed.

## Compatibility Constraints
Hash/serialization/version/lineage rule changes require explicit compatibility and migration analysis.

## Data Integrity
Expected and observed content identity, revision ordering, commit reference and chain linkage must agree with the governing contract.

## Failure Handling
Hash mismatch, broken chain, missing expected identity, corrupted state or unverifiable critical object remains FAIL/UNKNOWN/NOT_VERIFIED as appropriate; never success.

## Freeze Conditions
Critical Vault corruption, tamper evidence, authoritative-chain mismatch, fabricated proof, unauthorized repair request or destructive ambiguity.

## Validation
Known-good/known-bad content hashes, broken predecessor/chain, mismatched revision/commit reference, corruption/tamper and regression cases as applicable.

## Completion Criteria
Vault integrity result is based on actual pinned state and established expected identity/lineage rules with required evidence.

## Stop Conditions
Critical expected identity is unavailable, target is stale, repair would require unauthorized mutation, or lineage conflict cannot be safely resolved.

## Checkpoint
Persist Vault object/version identifiers, expected/observed integrity metadata, chain status, evidence and unresolved gaps without sensitive content.

## Resume
Re-read current Vault object/version/lineage before re-verification.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A matching artifact filename does not prove the revision content hash or commit chain is valid.

## Non-Goals
This Skill does not perform generic evidence/data integrity work owned by DATA-004.

## Version
1.0.0
