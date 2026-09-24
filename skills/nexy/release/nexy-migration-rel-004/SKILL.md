---
name: nexy-migration
description: Gate release/deployment migrations as REL-004 while remaining a distinct formal identity from ENG-006 engineering migration.
---

# NEXY Skill

## Identity
- Formal ID: `REL-004`
- Name: `nexy-migration`
- Family: BUILD / RELEASE
- Version: `1.0.0`
- Status: `MATERIALIZED`
- Identity note: distinct from `ENG-006 nexy-migration`.

## Objective
Migration gate. Gate release/deployment migrations as REL-004 while remaining a distinct formal identity from ENG-006 engineering migration.

## Authority
Release-family Skills act only within explicit task/release authority and established source gates. Production/destructive/security-boundary mutations retain applicable human gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current repository, test, release-policy, environment and evidence state.

## Scope
### In Scope
release-time schema/data/config/state migrations; ordering; backward/forward compatibility; backup/rollback; deploy sequencing; evidence and human/destructive gates.
### Out of Scope
Conflating REL-004 with ENG-006, destructive migration without gate, irreversible mutation without explicit approval, or hiding partial migration.

## Inputs
Universal inputs plus exact candidate/target/environment, release or build requirement, dependencies, gates, evidence, rollback state and approvals where applicable.

## Outputs
Universal outputs plus stage/action status, gate results, artifacts/state changes when authorized, evidence, rollback state, blockers and next action.

## Workflow
Context → Migration Authority → Current/Target State → Dependency/Compatibility → Backup/Rollback → Human Gate if Applicable → Execute Only if Authorized → Verify → Evidence.

## Required Behavior
Migration must be versioned, ordered, observable and reversible where required; partial/failure state remains explicit.

## Forbidden Behavior
Conflating REL-004 with ENG-006, destructive migration without gate, irreversible mutation without explicit approval, or hiding partial migration.

## Architecture Constraints
Respect law→contract→schema→implementation→test→release ordering; release automation cannot override CORE/LAW/JUDGE or source authority.

## Security Constraints
No plaintext secrets, privilege expansion, cross-tenant mutation or production/destructive operation without required controls and approvals.

## Compatibility Constraints
Release/build/migration changes assess consumers, versions, schema/data/state and rollback compatibility before promotion.

## Data Integrity
Artifacts, versions, migrations and deployment state must remain traceable to the exact candidate and evidence; partial mutation is never hidden.

## Failure Handling
Failed gate/action remains FAIL/BLOCKED/PARTIAL with rollback/recovery state explicit; no fake success or automatic unsafe retry.

## Freeze Conditions
Irreversible/destructive change without approval, unknown data ownership, absent rollback for required reversible path, stale state or migration conflict.

## Validation
Validate build/release semantics using positive, negative, stale-artifact, failed-gate, rollback/recovery and evidence-binding cases as applicable.

## Completion Criteria
Release migration reaches the intended version/state with integrity and compatibility evidence, or remains blocked/failed explicitly.

## Stop Conditions
Stale target, missing critical proof, unresolved authority conflict, unsafe secret/destructive operation, required human approval absent or rollback state unknown.

## Checkpoint
Persist exact candidate/head/environment, stage, gates, evidence, approvals, mutations, rollback state, failures and resume point.

## Resume
Refresh candidate, environment, release gates/evidence, approvals and current deployment state before continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A successful build is not a deployment or production-readiness proof.

## Non-Goals
This Skill does not bypass verification or human gates to accelerate release.

## Version
1.0.0
