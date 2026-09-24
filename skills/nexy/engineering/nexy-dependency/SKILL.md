---
name: nexy-dependency
description: Govern NEXY dependency additions and changes by proving need, source, version, license, placement, security, compatibility, build impact and lockfile effects before authorization.
---

# NEXY Skill

## Identity
- Formal ID: `ENG-007`
- Name: `nexy-dependency`
- Family: ENGINEERING
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Govern dependency additions/changes by evaluating why it is needed, authoritative source, version, license, required location, security, compatibility, build impact and lockfile impact.

## Authority
This Skill analyzes and gates dependency changes; it cannot add/update/remove a dependency unless the task explicitly authorizes that mutation.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current manifests/lockfiles/build configuration are revision-bound implementation evidence.

## Scope
### In Scope
- determine necessity;
- inspect existing alternatives;
- evaluate package/source/version/license/security;
- evaluate compatibility/build/runtime/transitive impact;
- determine manifest and lockfile surfaces;
- define validation and rollback.

### Out of Scope
- speculative dependency addition;
- automatic version selection without authoritative/current evidence;
- bypassing license/security policy;
- unrelated dependency upgrades.

## Inputs
### Required
- task
- authority
- scope
- repository
- branch
- head
- source_of_truth
- constraints
- expected_output
- validation_requirements
- dependency_request

### Optional
- manifests
- lockfile
- architecture-impact
- security advisories/evidence
- license policy
- existing dependency inventory

## Preconditions
Need and target location are established; source/version/security data is available or marked UNKNOWN.

## Outputs
- status
- dependency
- need
- alternatives
- source
- version
- license
- target_location
- transitive_impact
- compatibility
- security
- build_impact
- lockfile_impact
- allowed_changes
- validation
- rollback
- evidence
- unknowns
- next_action

## Workflow
Context → Authority → Requirement → Inspect Existing Dependencies → Evaluate Candidate → Impact/Security/Compatibility → Validate → Evidence.

## Required Behavior
- Prove why existing dependencies are insufficient.
- Bind version/source to current evidence; do not guess “latest”.
- Include transitive and lockfile effects.
- Require explicit mutation scope for manifest/lockfile changes.

## Forbidden Behavior
- Do not silently install packages.
- Do not invent license/security status.
- Do not upgrade unrelated dependencies.
- Do not use dependency changes to bypass architecture.

## Architecture Constraints
Dependency must fit legal module/runtime boundary.

## Security Constraints
Unknown critical supply-chain provenance/security blocks mutation.

## Compatibility Constraints
Check runtime/toolchain/API/version compatibility and lockfile determinism.

## Data Integrity
Dependency changes must not silently alter migrations/data formats without separate analysis.

## Failure Handling
If source/version/license/security/compatibility is unknown and material, return BLOCKED/UNKNOWN.

## Freeze Conditions
Untrusted/unknown critical source, incompatible license/policy, security risk, unauthorized manifest/lockfile surface, or destructive transitive effect.

## Validation
Manifest/lockfile diff, install/build/typecheck/test/security checks as applicable; all must be evidence-bound.

## Completion Criteria
Dependency decision complete when need, candidate identity/version/source, security/license/compatibility, impact, validation and rollback are established.

## Stop Conditions
Critical provenance/security/license/version uncertainty or missing authorization.

## Checkpoint
Persist candidate identity, version/source evidence, impact, decision and validation plan.

## Resume
Refresh current registry/security/version evidence before acting on a stale decision.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A new package request is BLOCKED if the repository already provides the required capability and no authoritative need for another dependency exists.

## Non-Goals
This Skill does not independently install, commit or release dependencies.

## Version
1.0.0
