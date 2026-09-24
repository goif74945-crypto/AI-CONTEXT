---
name: nexy-api-integration
description: Validate UI/API/Core integration.
---

# NEXY Skill

## Identity
- Formal ID: `API-004`
- Name: `nexy-api-integration`
- Family: API
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Validate UI/API/Core integration.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
UI/API/Core call chain, contracts, auth context, state transitions, error propagation, persistence/side effects and evidence.
### Out of Scope
Replacing real boundary proof with isolated route tests, hiding downstream failure, or bypassing Core/state authority.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Context → Boundary Chain → Preconditions/Auth → UI/API Call → Core/State Effect → Response/Error Propagation → Evidence.

## Required Behavior
Integration proves contract and authority preservation across UI→API→CORE and applicable persistence edges.

## Forbidden Behavior
Replacing real boundary proof with isolated route tests, hiding downstream failure, or bypassing Core/state authority.

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
Required dependency/environment missing, stale target or boundary mismatch cannot be safely resolved.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Applicable UI/API/Core integration edges pass with state/error behavior and evidence bound to the target.

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
