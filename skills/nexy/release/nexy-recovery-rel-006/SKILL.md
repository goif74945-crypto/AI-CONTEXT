---
name: nexy-recovery
description: Manage release/deployment recovery as REL-006 while remaining distinct from CORE-006 runtime FREEZE recovery.
---

# NEXY Skill

## Identity
- Formal ID: `REL-006`
- Name: `nexy-recovery`
- Family: BUILD / RELEASE
- Version: `1.0.0`
- Status: `MATERIALIZED`
- Identity note: distinct from `CORE-006 nexy-recovery`.

## Objective
Deployment/release recovery. Manage release/deployment recovery as REL-006 while remaining distinct from CORE-006 runtime FREEZE recovery.

## Authority
Release-family Skills act only within explicit task/release authority and established source gates. Production/destructive/security-boundary mutations retain applicable human gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current repository, test, release-policy, environment and evidence state.

## Scope
### In Scope
failed rollout; degraded deployment; rollback target; release state restoration; migration interaction; health/evidence; incident linkage and human gates.
### Out of Scope
Conflating with CORE-006, blind retry, restoring unverified artifact, destructive recovery without approval, or calling restart successful recovery.

## Inputs
Universal inputs plus exact candidate/target/environment, release or build requirement, dependencies, gates, evidence, rollback state and approvals where applicable.

## Outputs
Universal outputs plus stage/action status, gate results, artifacts/state changes when authorized, evidence, rollback state, blockers and next action.

## Workflow
Context → Incident/Release State → Last Known Good → Recovery Authority → Rollback/Forward-Fix Decision → Human Gate if Needed → Execute Authorized Recovery → Verify Health/State → Evidence.

## Required Behavior
Recovery returns to a proven legal deployment/release state and records what was restored; restart alone is never accepted as recovery proof.

## Forbidden Behavior
Conflating with CORE-006, blind retry, restoring unverified artifact, destructive recovery without approval, or calling restart successful recovery.

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
Last known good cannot be proven, recovery is destructive/ambiguous without approval, migration state is inconsistent, or security boundary risk expands.

## Validation
Validate build/release semantics using positive, negative, stale-artifact, failed-gate, rollback/recovery and evidence-binding cases as applicable.

## Completion Criteria
Deployment/release state is restored or advanced to a proven valid state with current evidence and residual risks documented.

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
