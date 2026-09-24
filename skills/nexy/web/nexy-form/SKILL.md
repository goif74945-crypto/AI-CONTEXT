---
name: nexy-form
description: Create NEXY forms with source-backed schema validation, authorization, submission, error, loading and state handling without trusting client validation as security.
---

# NEXY Skill

## Identity
- Formal ID: `WEB-004`
- Name: `nexy-form`
- Family: WEB
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Create forms with schema validation, authorization, error, submission and state handling.

## Authority
Client form behavior is presentation/input collection; backend/API remains authoritative for validation and authorization.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Exact request/response schema and API implementation at pinned HEAD.

## Scope
### In Scope
Fields, validation UX, submit behavior, loading/error/freeze/success, API mapping, tests.
### Out of Scope
Invented fields/schema, backend authorization bypass, storing secrets client-side.

## Inputs
Universal inputs plus form schema, endpoint contract, auth/RBAC, state and error semantics.

## Outputs
Universal outputs plus field/schema map, submit flow, error map, permission behavior, tests/evidence.

## Workflow
Context → Authority → Schema/Endpoint Requirement → Inspect → Implement → Negative/Integration Validation → Evidence.

## Required Behavior
- Validate client input for UX and send only contract-valid payloads.
- Backend authorization/validation remains mandatory.
- Preserve explicit error/freeze states.
- Prevent duplicate/fake submit success.

## Forbidden Behavior
- No client-side security as sole enforcement.
- No plaintext secret logging.
- No schema widening without contract authority.
- No silent error swallowing.

## Architecture Constraints
Form → API contract → backend rule boundary must remain explicit.

## Security Constraints
Input validation, auth/RBAC, session/CSRF and secret handling as applicable.

## Compatibility Constraints
Preserve field/request/response contracts unless authorized.

## Data Integrity
Do not report committed state until backend confirms authoritative mutation.

## Failure Handling
Validation/API failure surfaces explicit error; no optimistic final success.

## Freeze Conditions
Unknown critical schema/auth rule, backend FREEZE, security violation, stale target.

## Validation
Valid/invalid input, unauthorized submit, API error, duplicate/retry behavior, loading/freeze/success and regression.

## Completion Criteria
Form matches contract and required positive/negative flows are proven.

## Stop Conditions
Missing schema/API/auth source or forbidden scope.

## Checkpoint
Persist schema/endpoint versions, state flows and evidence.

## Resume
Refresh schema/API/HEAD.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Client-side validation can reject malformed input early but cannot replace backend schema/RBAC checks.

## Non-Goals
This Skill does not define new backend business rules.

## Version
1.0.0
