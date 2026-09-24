---
name: nexy-migration
description: Gate schema/data/API/dependency/module/architecture migrations with migration and applicable rollback/evidence.
---

# NEXY Skill

## Identity
- Formal ID: `ENG-006`
- Name: `nexy-migration`
- Family: ENGINEERING
- Version: `1.0.0`
- Status: `MATERIALIZED`
- Identity note: distinct from `REL-004 nexy-migration`.

## Objective
Gate schema/data/API/dependency/module/architecture migrations with migration and applicable rollback/evidence.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
migration source/target state, affected schemas/data/APIs/dependencies/modules, compatibility, ordering, backup/rollback, tests/evidence.
### Out of Scope
Conflating with REL-004 release migration, destructive mutation without gate, silent data loss, skipped compatibility or fake migration success.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Context → Migration Requirement → Current/Target State → Impact/Compatibility → Plan/Rollback → Authorized Execution or Plan → Validate → Evidence.

## Required Behavior
Engineering migration preserves data/contract integrity and records compatibility/rollback requirements before mutation.

## Forbidden Behavior
Conflating with REL-004 release migration, destructive mutation without gate, silent data loss, skipped compatibility or fake migration success.

## Architecture Constraints
Respect declared layers, contracts, state ownership, dependency direction and source authority; do not create hidden bypasses.

## Security Constraints
Validate applicable trust boundaries, permissions, secret handling and unsafe side effects; fail closed on critical uncertainty.

## Compatibility Constraints
Assess contract/version/consumer/data compatibility when the task can affect them.

## Data Integrity
Preserve authoritative data/state/provenance and do not mutate or reinterpret protected state without explicit authority.

## Failure Handling
Failure, unknown, conflict, missing proof or unavailable dependency remains explicit; no fabricated fallback success.

## Freeze Conditions
Destructive/irreversible ambiguity, authority missing, rollback required but unavailable, or stale source state.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Engineering migration is safely specified/executed within authority with required validation and evidence.

## Stop Conditions
Stale target, material authority/scope conflict, missing critical proof, unsafe mutation, required human gate or unresolved dependency that affects correctness.

## Checkpoint
Persist exact target/version, inputs, claims/proofs, decisions, validation state, unresolved gaps and resume point.

## Resume
Refresh source authority, target state and evidence freshness before continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Presence or naming similarity alone is never sufficient proof of implementation or compliance.

## Non-Goals
This Skill does not self-approve unsupported completion.

## Version
1.0.0
