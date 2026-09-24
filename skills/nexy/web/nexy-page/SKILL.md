---
name: nexy-page
description: Create or modify a NEXY page only from an authoritative route/page specification with verified data, permissions, state and error behavior.
---

# NEXY Skill

## Identity
- Formal ID: `WEB-003`
- Name: `nexy-page`
- Family: WEB
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Create a page according to route specification and its state, API, permission and evidence obligations.

## Authority
Page creation requires explicit route/scope authority and cannot invent navigation, APIs or protected actions.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current route/app tree at exact HEAD.

## Scope
### In Scope
Route binding, page layout/content required by source, data/API wiring, state/error/freeze behavior, tests.
### Out of Scope
Unrequested routes, backend contract invention, unrelated navigation redesign.

## Inputs
Universal inputs plus route specification, page requirement, API/data contract and permission/state requirements.

## Outputs
Universal outputs plus route mapping, page states, API/data dependencies, tests and evidence.

## Workflow
Context → Authority → Route Requirement → Inspect Router/API/State → Implement → Validate Route/State/Permission → Evidence.

## Required Behavior
Use exact route identity; preserve 404/error/freeze/loading/success truth; verify all page actions against API contracts.

## Forbidden Behavior
No invented route, fake data, placeholder counted as complete, or client-only authorization.

## Architecture Constraints
Respect router/page/component/API boundaries.

## Security Constraints
Protected page actions require backend authorization and safe input/output handling.

## Compatibility Constraints
Preserve existing route semantics and deep links unless authorized.

## Data Integrity
Displayed durable data must come from authoritative source/API.

## Failure Handling
Missing route/API requirement => BLOCKED/UNKNOWN.

## Freeze Conditions
Conflicting route authority, missing critical contract/permission, backend FREEZE, stale HEAD.

## Validation
Route resolution, page build/type, API integration, permissions, state/error/freeze behavior and regression.

## Completion Criteria
Page exists at the authorized route and all required flows are evidence-backed.

## Stop Conditions
Unknown/unauthorized route or dependency, security gate, scope expansion.

## Checkpoint
Persist route, dependency, changed files, test/evidence status.

## Resume
Refresh route tree/API contracts/HEAD.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A new admin page is blocked if the route exists but backend RBAC requirements are unknown.

## Non-Goals
This Skill does not create unspecified APIs or release the app.

## Version
1.0.0
