---
name: nexy-vault
description: Manage the NEXY Vault as the controlled persistent project/artifact lineage boundary without inventing storage authority, overwriting immutable history, or confusing persistence with semantic truth.
---

# NEXY Skill

## Identity
- Formal ID: `VLT-001`
- Name: `nexy-vault`
- Family: VAULT / STATE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Manage Vault.

## Authority
Vault is a persistence/lineage boundary. This Skill may manage Vault behavior only within established source/spec authority and cannot promote stored content into semantic truth or decision authority by existence alone.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current Vault/storage contracts and pinned implementation/evidence when the task concerns current behavior.

## Scope
### In Scope
Vault state, artifact/revision/commit lineage, persistence ownership, integrity boundaries, concurrency/conflict handling, read/write authorization, recovery evidence and traceability.
### Out of Scope
Invented storage providers, semantic adjudication, hidden overwrites, unapproved migration, destructive history rewrite or treating storage presence as proof of correctness.

## Inputs
Universal inputs plus Vault operation, target object/version, authority/scope, expected lineage/state, integrity/concurrency evidence and pinned target revision when applicable.

## Outputs
Universal outputs plus Vault result, lineage/state status, conflicts, integrity/provenance evidence, persistence effects and next action.

## Workflow
Context → Authority → Vault Contract → Resolve Object/Version → Validate Ownership/Permissions → Inspect Lineage/Integrity/Concurrency → Execute Authorized Operation if allowed → Validate → Evidence.

## Required Behavior
Preserve explicit lineage and state ownership; distinguish read from write; fail closed on critical conflict or unverifiable authoritative state.

## Forbidden Behavior
No silent overwrite, fake commit/revision, invented persistence success, unapproved destructive rewrite, authority escalation or truth claims from storage existence alone.

## Architecture Constraints
Vault remains persistence/lineage infrastructure beneath CORE/LAW/JUDGE authority; callers must respect canonical contracts and state ownership.

## Security Constraints
Validate authorization at write/read boundaries as applicable; minimize sensitive data exposure; preserve auditability for critical mutations.

## Compatibility Constraints
Schema/version/storage contract changes require explicit compatibility and migration analysis before mutation.

## Data Integrity
Critical persisted objects require traceable identity/version/integrity evidence when the governing source requires it.

## Failure Handling
Conflict, corruption, unavailable authoritative state or persistence failure remains explicit; no success masking.

## Freeze Conditions
Critical lineage corruption, unauthorized mutation, irreconcilable commit conflict, evidence falsification or unsafe destructive operation.

## Validation
Structural/storage contract checks, lineage/version checks, integrity/conflict cases, rollback/recovery checks and regression evidence as applicable.

## Completion Criteria
The Vault task is source-aligned, authorized, lineage-safe, integrity-aware and supported by the required current evidence.

## Stop Conditions
Authority/scope ambiguity affecting data ownership, destructive migration without human gate, stale HEAD, missing critical lineage or unverifiable integrity.

## Checkpoint
Persist object identity, version/lineage state, operation class, evidence, unresolved conflicts and resume point without secrets.

## Resume
Refresh target revision, Vault state, lineage/conflict status and relevant source before continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A stored revision is persistence evidence; it does not by itself prove the revision is semantically correct.

## Non-Goals
This Skill does not replace CORE/LAW/JUDGE decision authority.

## Version
1.0.0
