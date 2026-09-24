---
name: nexy-web
description: Create or modify the NEXY web application only from source-backed requirements while preserving truthful state, permissions, errors, FREEZE behavior and API contracts.
---

# NEXY Skill

## Identity
- Formal ID: `WEB-001`
- Name: `nexy-web`
- Family: WEB
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Create or modify the NEXY web application according to authoritative source/spec while preserving backend truth and integration contracts.

## Authority
Web mutation requires explicit task authorization and cannot override backend/Core/Law authority or protected security boundaries.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current web/API implementation requires exact repository/branch/HEAD evidence.

## Scope
### In Scope
- authorized web/UI changes;
- route/page/form/state/error/loading/FREEZE behavior;
- API/contract integration;
- permission-aware rendering;
- tests/evidence.

### Out of Scope
- backend contract invention;
- fake/mock success presented as real;
- unauthorized design-system rewrite;
- hidden permission bypass;
- unrelated API/Core mutation.

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
- normalized_requirement
- architecture_context

### Optional
- route spec
- API contracts
- state model
- RBAC rules
- UI baseline
- test/evidence baseline

## Preconditions
Target revision, route/API contract and required permissions/state semantics are known or execution is BLOCKED.

## Outputs
- status
- objective
- scope
- actions
- changed_files
- unchanged_files
- diff
- routes
- UI_state_behavior
- API_integration
- permission_behavior
- tests
- validation
- evidence
- errors
- unknowns
- rollback
- next_action

## Workflow
Context → Authority → Requirement → Architecture/Contract Inspection → Web Change → Validation → Evidence.

## Required Behavior
- Unauthorized UI action → BLOCK.
- Backend FREEZE → UI FREEZE.
- Invalid API response → ERROR.
- Fake success → FAIL.
- Preserve loading/error/success/freeze state truth.
- Validate permissions at authoritative backend boundary and reflect result honestly in UI.

## Forbidden Behavior
- Do not hardcode successful state for unavailable backend behavior.
- Do not expose secrets/provider internals.
- Do not bypass API contracts or RBAC.
- Do not alter unrelated UI/architecture.

## Architecture Constraints
Respect UI → API → Core boundary; frontend does not become source of authoritative backend state.

## Security Constraints
No secret leakage; auth/session/RBAC/CSRF/input/output rules apply as relevant.

## Compatibility Constraints
Preserve route/API/schema compatibility unless explicitly authorized.

## Data Integrity
UI must not imply persistence succeeded until authoritative backend evidence supports it.

## Failure Handling
Surface explicit loading/error/FREEZE states; partial backend failure cannot become UI success.

## Freeze Conditions
Unknown critical route/API/state/permission contract, backend FREEZE, security violation, stale target, or out-of-scope mutation.

## Validation
Type/build, route, API, integration, state, permissions, FREEZE and error behavior as applicable.

## Completion Criteria
Authorized web change is complete only with truthful behavior, required tests and traceable evidence.

## Stop Conditions
Missing critical API/route/permission source, fake-success requirement, forbidden surface, security gate, or stale HEAD.

## Checkpoint
Persist target revision, route/API/state contract, changed files, tests and evidence.

## Resume
Refresh HEAD and API/route contracts before continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- If backend returns FREEZE, the page must display/propagate a FREEZE state rather than “completed”.

## Non-Goals
This Skill does not redefine backend contracts or release the application.

## Version
1.0.0
