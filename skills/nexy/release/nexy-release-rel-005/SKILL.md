---
name: nexy-release
description: Orchestrate NEXY release progression through required build, test, verification, evidence, policy, rollout, and rollback gates.
---

# NEXY Skill

## Identity
- Formal ID: `REL-005`
- Name: `nexy-release`
- Family: BUILD / RELEASE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Release orchestration. Advance a release candidate only when the required source-defined gates are satisfied.

## Authority
This Skill follows explicit release authority, project governance, and applicable human approval requirements. It does not override CORE, LAW, JUDGE, verification, or release-policy decisions.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current candidate, test, evidence, release-policy, environment, and rollback records.

## Scope
### In Scope
Release candidate identity, build/test/security/verification gates, evidence freshness, staged rollout, health checks, rollback readiness, approvals, and release records.
### Out of Scope
Skipping required gates, promoting stale artifacts, treating candidate creation as release completion, or claiming readiness without evidence.

## Inputs
Universal inputs plus exact candidate/version, target stage, required gates, evidence, rollout state, rollback state, and approvals where applicable.

## Outputs
Universal outputs plus stage status, gate results, blockers, rollout/rollback state, evidence references, and next action.

## Workflow
Context → Candidate Identity → Required Gates → Verification/Evidence → Release Policy → Stage Progression → Health/Observation → Record Verdict.

## Required Behavior
Each stage uses the exact candidate and current evidence. Any failed or missing required gate blocks advancement.

## Forbidden Behavior
No stale-artifact promotion, hidden failed gate, fabricated rollout result, unverified stage advancement, or bypass of required approval.

## Architecture Constraints
Release follows law → contract → implementation → test → verification → release ordering and cannot redefine upstream authority.

## Security Constraints
Security failures cannot be waived for convenience; secrets and protected operational data remain minimized and controlled.

## Compatibility Constraints
Release checks compatibility of relevant contracts, schemas, state, and consumers before advancement.

## Data Integrity
Candidate identity, version, stage, evidence, and rollback references must remain traceable and consistent.

## Failure Handling
A failed stage remains explicit as FAIL/BLOCKED/PARTIAL with recovery or rollback path recorded where applicable.

## Freeze Conditions
Open critical blocker, stale mandatory evidence, failed security or verification gate, missing required approval, or unknown rollback state.

## Validation
Positive and negative gate cases, stale evidence, failed stage, rollback readiness, and exact-candidate binding as applicable.

## Completion Criteria
All required gates for the requested release state are satisfied and recorded for the exact candidate.

## Stop Conditions
Stale target, missing mandatory proof, unresolved authority conflict, required approval absent, or rollback/recovery state cannot be established.

## Checkpoint
Persist candidate/version, stage, gate states, evidence, approvals, blockers, rollback state, and resume point.

## Resume
Refresh candidate, stage, evidence freshness, gate state, and approvals before continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A build that passes but lacks current security/evidence gates remains blocked from later release stages.

## Non-Goals
This Skill does not manufacture evidence or self-approve skipped gates.

## Version
1.0.0
