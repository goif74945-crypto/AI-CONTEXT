---
name: nexy-commit
description: Manage NEXY Vault commit semantics by binding authorized revision state into traceable commit lineage without fabricating success, bypassing integrity checks, or silently resolving concurrency conflicts.
---

# NEXY Skill

## Identity
- Formal ID: `VLT-004`
- Name: `nexy-commit`
- Family: VAULT / STATE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Manage commit semantics.

## Authority
Commit operations require established task authority and Vault contracts. This Skill cannot commit nonexistent/unverified revision state or bypass conflict/integrity gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current commit/revision/Vault implementation and pinned evidence when applicable.

## Scope
### In Scope
Commit preconditions, revision binding, lineage metadata, concurrency/version checks, idempotency where established, persistence result and commit evidence.
### Out of Scope
Invented commit IDs, committing absent revisions, silent conflict override, unauthorized branch/history rewrite or semantic approval outside Vault responsibility.

## Inputs
Universal inputs plus revision identity, expected current version/state, commit intent, concurrency token/precondition when established and integrity/provenance evidence.

## Outputs
Universal outputs plus commit identity/status, bound revision/version, lineage/conflict result, evidence and next action.

## Workflow
Context → Authority → Commit Contract → Resolve Revision/Expected State → Validate Integrity/Concurrency Preconditions → Execute Authorized Commit → Verify Persisted Lineage/Result → Evidence.

## Required Behavior
Bind a real revision to a real commit result under declared preconditions; repeated/stale operations remain explicit according to established idempotency/concurrency rules.

## Forbidden Behavior
No fake commit, no success before persistence proof, no conflict swallowing, no revision substitution and no unauthorized history mutation.

## Architecture Constraints
Commit semantics depend on Vault, Revision and Concurrency boundaries and do not replace them.

## Security Constraints
Commit mutation requires applicable authorization and auditable attribution.

## Compatibility Constraints
Commit schema/version/precondition changes require consumer and migration impact review.

## Data Integrity
Commit must reference the intended revision/version and preserve legal lineage/integrity metadata.

## Failure Handling
Missing revision, stale expected state, integrity failure or persistence error returns explicit failure/conflict without pretending success.

## Freeze Conditions
Critical commit-lineage corruption, unauthorized mutation, evidence fabrication or unsafe forced conflict override.

## Validation
Happy path, missing revision, stale writer, duplicate/idempotent behavior when specified, integrity failure, rollback/recovery and regression checks as applicable.

## Completion Criteria
Commit result is authorized, persisted, correctly bound to revision/version and supported by current evidence.

## Stop Conditions
Revision/expected state is unknown, stale target, conflict requires unapproved force/destructive action or persistence cannot be verified.

## Checkpoint
Persist revision/commit identities, expected/observed version, conflict status, evidence and resume point.

## Resume
Refresh current revision and commit lineage before retrying or continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A stale expected version yields an explicit conflict rather than silently committing against a newer revision.

## Non-Goals
This Skill does not merge concurrent edits by inference.

## Version
1.0.0
