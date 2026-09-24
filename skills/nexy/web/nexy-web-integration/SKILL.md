---
name: nexy-web-integration
description: Integrate UI → API → contracts and verify response, error, loading, authorization.
---

# NEXY Skill

## Identity
- Formal ID: `WEB-006`
- Name: `nexy-web-integration`
- Family: WEB
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Integrate UI → API → contracts and verify response, error, loading, authorization.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
UI actions/state, API route/contracts, auth/RBAC, loading/error/freeze/success semantics and integration evidence.
### Out of Scope
Fake UI success, client-only authorization, swallowing API/FREEZE errors, or bypassing canonical contract.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Context → UI Intent → API Contract/Auth → Integration → Loading/Error/Freeze/Success Paths → Validation → Evidence.

## Required Behavior
UI reflects backend truth and authorization; contract/error/state transitions are preserved end to end.

## Forbidden Behavior
Fake UI success, client-only authorization, swallowing API/FREEZE errors, or bypassing canonical contract.

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
Backend contract/authority unresolved, critical state mismatch, or integration would require bypassing protected boundary.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Applicable UI↔API integration paths truthfully represent real response/auth/error/state behavior.

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
