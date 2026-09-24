---
name: nexy-ui
description: Build NEXY UI surfaces that accurately represent backend state, permissions, loading, errors, FREEZE and success without inventing authoritative state.
---

# NEXY Skill

## Identity
- Formal ID: `WEB-002`
- Name: `nexy-ui`
- Family: WEB
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Create UI while preserving state truth, permissions, loading, error, FREEZE and success behavior.

## Authority
UI may render and request actions but cannot become the authority for protected backend state or permissions.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current UI/API behavior requires exact revision evidence.

## Scope
### In Scope
- components/views;
- state representation;
- permission-aware affordances;
- loading/error/freeze/success behavior;
- accessibility/interaction where specified;
- tests/evidence.

### Out of Scope
- backend authorization;
- contract invention;
- visual redesign beyond scope;
- fake client-side authority.

## Inputs
Required universal Skill inputs plus UI requirement, state model, permissions and API/route contract as applicable.

## Outputs
Universal outputs plus UI states, interaction map, permission representation, tests, diff and evidence.

## Workflow
Context → Authority → Requirement → Inspect State/API/Permissions → Implement UI → Validate Truth/Interaction → Evidence.

## Required Behavior
- Represent backend state exactly.
- Disable/hide actions only as presentation; backend remains authoritative.
- Show loading/error/FREEZE explicitly.
- Do not display success before authoritative success exists.

## Forbidden Behavior
- No fake success.
- No client-only authorization.
- No swallowing invalid API/error states.
- No secret/provider exposure.

## Architecture Constraints
UI remains downstream of API/Core truth.

## Security Constraints
Do not use visibility as authorization; preserve session/RBAC/CSRF requirements.

## Compatibility Constraints
Preserve component/route/API expectations unless authorized.

## Data Integrity
Do not optimistically claim durable mutation without backend confirmation where authoritative truth matters.

## Failure Handling
Invalid/unknown API response becomes explicit ERROR/UNKNOWN, not success.

## Freeze Conditions
Backend FREEZE, unknown critical state/permission, or security/scope conflict.

## Validation
State matrix, permission states, loading/error/freeze/success flows, type/build and integration tests as applicable.

## Completion Criteria
UI is source-aligned, truthful and validation-backed.

## Stop Conditions
Missing critical state/API contract, unauthorized action model, stale target or security gate.

## Checkpoint
Persist UI state/permission matrix and evidence.

## Resume
Refresh backend/API state semantics before reuse.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A button may be hidden for a user role, but the API must still enforce authorization.

## Non-Goals
This Skill does not implement backend authorization or release.

## Version
1.0.0
