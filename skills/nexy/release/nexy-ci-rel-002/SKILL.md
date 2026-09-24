---
name: nexy-ci
description: Validate NEXY continuous-integration gates, triggers, reproducibility and evidence binding without assuming a configured workflow ran successfully.
---

# NEXY Skill

## Identity
- Formal ID: `REL-002`
- Name: `nexy-ci`
- Family: BUILD / RELEASE
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Validate CI pipeline. Validate NEXY continuous-integration gates, triggers, reproducibility and evidence binding without assuming a configured workflow ran successfully.

## Authority
Release-family Skills act only within explicit task/release authority and established source gates. Production/destructive/security-boundary mutations retain applicable human gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current repository, test, release-policy, environment and evidence state.

## Scope
### In Scope
CI workflow/config; triggers; required checks; environment/tool versions; test/build/security gates; artifacts/logs; commit/head binding and failure propagation.
### Out of Scope
Calling workflow presence CI PASS, ignoring failed/missing checks, changing required gates merely to pass or fabricating CI status.

## Inputs
Universal inputs plus exact candidate/target/environment, release or build requirement, dependencies, gates, evidence, rollback state and approvals where applicable.

## Outputs
Universal outputs plus stage/action status, gate results, artifacts/state changes when authorized, evidence, rollback state, blockers and next action.

## Workflow
Context → CI Contract → Workflow/Trigger → Required Checks → Exact Commit Run → Result/Artifact Binding → Failure Semantics → Evidence.

## Required Behavior
Separate configured, triggered, executed and passed states; CI evidence must bind to the exact commit and required checks.

## Forbidden Behavior
Calling workflow presence CI PASS, ignoring failed/missing checks, changing required gates merely to pass or fabricating CI status.

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
Required check missing/disabled, exact-head run unavailable for a mandatory claim, security gate bypass or workflow authority conflict.

## Validation
Validate build/release semantics using positive, negative, stale-artifact, failed-gate, rollback/recovery and evidence-binding cases as applicable.

## Completion Criteria
Required CI checks execute and pass for the exact target with current traceable evidence.

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
