---
name: nexy-ui-truth
description: Ensure NEXY UI surfaces reflect actual backend state and never convert FREEZE, failure, unknown or partial state into fake success.
---

# NEXY Skill

## Identity
- Formal ID: `WEB-005`
- Name: `nexy-ui-truth`
- Family: WEB
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Ensure UI reflects actual backend state; backend FREEZE must be represented as UI FREEZE, not fake success.

## Authority
This Skill checks truth representation. It does not authorize backend state transitions or rewrite backend responses.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Exact backend/API state/error contract at pinned revision.

## Scope
### In Scope
Map backend state/error/permission/result to UI rendering and interaction; test truth surfaces.
### Out of Scope
Backend mutation, state invention, cosmetic redesign unrelated to truth.

## Inputs
Universal inputs plus backend state/error contract, UI target and API response evidence.

## Outputs
Universal outputs plus truth matrix, mismatches, affected UI states, tests/evidence and required correction class.

## Workflow
Context → Authority → State/Contract Requirement → Compare Backend vs UI → Negative Tests → Evidence.

## Required Behavior
- Backend FREEZE → UI FREEZE.
- Backend error → UI error.
- Unknown/unverified result → UI must not show verified success.
- Permission denial → no successful action presentation.
- Stale/pending state remains pending/stale as appropriate.

## Forbidden Behavior
- No fake success.
- No optimistic terminal state without authoritative proof.
- No swallowing backend errors.
- No fabricated evidence/status labels.

## Architecture Constraints
UI is a truth surface downstream of API/Core state.

## Security Constraints
Do not reveal sensitive error details; preserve authorization result without leaking secrets.

## Compatibility Constraints
Truth mapping must follow current backend contract version.

## Data Integrity
Persistent success requires authoritative persistence success when relevant.

## Failure Handling
Any semantic mismatch is FAIL/PARTIAL until corrected and revalidated.

## Freeze Conditions
Critical backend/UI state ambiguity, contract mismatch, or backend FREEZE.

## Validation
Golden and negative state mapping, permission/error/freeze behavior, integration/regression.

## Completion Criteria
Every in-scope authoritative backend state maps to a truthful UI state with no proven fake-success path.

## Stop Conditions
Unknown state contract, stale target, critical mismatch requiring out-of-scope backend change.

## Checkpoint
Persist backend/UI truth matrix and mismatch evidence.

## Resume
Refresh backend contract/HEAD.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A failed save with 500 cannot leave a “Saved” badge unless a later authoritative read proves persistence.

## Non-Goals
This Skill does not decide visual styling or backend state.

## Version
1.0.0
