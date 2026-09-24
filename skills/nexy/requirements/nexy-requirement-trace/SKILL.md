---
name: nexy-requirement-trace
description: Trace Requirement → Design → File → Implementation → Test → Evidence; missing test/evidence remains UNVERIFIED.
---

# NEXY Skill

## Identity
- Formal ID: `REQ-003`
- Name: `nexy-requirement-trace`
- Family: REQUIREMENTS
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Trace Requirement → Design → File → Implementation → Test → Evidence; missing test/evidence remains UNVERIFIED.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
requirement IDs, design/entities, implementation paths/symbols, tests, execution status, evidence and version/head binding.
### Out of Scope
Calling implementation/test/evidence complete from name match or file presence, fabricating mapping, or hiding trace gaps.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Requirement → Design/Entity → Code → Test → Executed Result → Evidence → Verdict/Gap.

## Required Behavior
Each trace edge is evidence-backed; missing mapping, execution or evidence remains explicit.

## Forbidden Behavior
Calling implementation/test/evidence complete from name match or file presence, fabricating mapping, or hiding trace gaps.

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
Critical trace cannot be established after reasonable alternate search or source/implementation identity is unresolved.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Trace chain is complete for the claimed verdict or the exact missing edge is recorded.

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
