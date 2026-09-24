---
name: nexy-build
description: Orchestrate the NEXY build pipeline only from authorized source-aligned inputs and preserve distinct build, test, verification and release gates.
---

# NEXY Skill

## Identity
- Formal ID: `REL-001`
- Name: `nexy-build`
- Family: BUILD / RELEASE
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Build orchestration. Orchestrate the NEXY build pipeline only from authorized source-aligned inputs and preserve distinct build, test, verification and release gates.

## Authority
Release-family Skills act only within explicit task/release authority and established source gates. Production/destructive/security-boundary mutations retain applicable human gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current repository, test, release-policy, environment and evidence state.

## Scope
### In Scope
build inputs; dependency/toolchain state; compile/typecheck/lint/build sequencing; produced artifacts; test/verification handoff and build evidence.
### Out of Scope
Treating build success as behavioral correctness or release approval, weakening build gates, fabricating artifacts or building from stale/unauthorized state.

## Inputs
Universal inputs plus exact candidate/target/environment, release or build requirement, dependencies, gates, evidence, rollback state and approvals where applicable.

## Outputs
Universal outputs plus stage/action status, gate results, artifacts/state changes when authorized, evidence, rollback state, blockers and next action.

## Workflow
Context → Authority/Target → Dependencies/Toolchain → Build Plan → Compile/Typecheck/Lint/Build → Artifact Check → Test/Verification Handoff → Evidence.

## Required Behavior
Use canonical project commands and exact target state; failures remain explicit and produced artifacts are traceable.

## Forbidden Behavior
Treating build success as behavioral correctness or release approval, weakening build gates, fabricating artifacts or building from stale/unauthorized state.

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
Canonical build requirements/toolchain unavailable, stale target, failed mandatory prerequisite or unsafe config weakening required.

## Validation
Validate build/release semantics using positive, negative, stale-artifact, failed-gate, rollback/recovery and evidence-binding cases as applicable.

## Completion Criteria
Applicable build pipeline succeeds and hands current evidence to later verification/release gates; no release claim is implied.

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
