---
name: nexy-api-validation
description: Validate request, response, errors, auth, RBAC, schema, and status.
---

# NEXY Skill

## Identity
- Formal ID: `API-003`
- Name: `nexy-api-validation`
- Family: API
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Validate request, response, errors, auth, RBAC, schema, and status.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
request/response schemas, status/error semantics, authn/authz/RBAC, validation, headers/cookies where applicable and tests/evidence.
### Out of Scope
Approving shape drift, missing negative cases, client-only permission checks, or calling route presence valid API behavior.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Context → API Contract → Request Cases → Auth/RBAC → Business/Schema → Response/Error/Status → Evidence.

## Required Behavior
Positive and negative requests obey exact contract and authorization with deterministic error/status behavior.

## Forbidden Behavior
Approving shape drift, missing negative cases, client-only permission checks, or calling route presence valid API behavior.

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
Contract authority conflict, auth boundary unresolved or current execution proof required but unavailable.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
API validation covers applicable request/response/error/auth/RBAC/schema/status obligations with evidence.

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
