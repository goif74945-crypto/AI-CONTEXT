---
name: nexy-web-validation
description: Validate type, build, route, API, integration, state, permissions, freeze, and error behavior.
---

# NEXY Skill

## Identity
- Formal ID: `WEB-007`
- Name: `nexy-web-validation`
- Family: WEB
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Validate type, build, route, API, integration, state, permissions, freeze, and error behavior.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
web type/build, routes, API bindings, integration, UI state, permission visibility/action control, freeze/error/loading behavior.
### Out of Scope
Passing on visual render alone, hiding backend error, ignoring unauthorized action, or treating frontend checks as backend authorization proof.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Context → Web Requirements → Type/Build → Route/API → State/Permission → Freeze/Error → Integration/Regression → Evidence.

## Required Behavior
Validate both presentation and truth/authorization behavior; backend remains authority for protected operations.

## Forbidden Behavior
Passing on visual render alone, hiding backend error, ignoring unauthorized action, or treating frontend checks as backend authorization proof.

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
Required backend state/contract unavailable, critical UI truth mismatch, stale target or unsafe action needed.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Applicable web validation layers pass with current evidence and no fake-success/state mismatch.

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
