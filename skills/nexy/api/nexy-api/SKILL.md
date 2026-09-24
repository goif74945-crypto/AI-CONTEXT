---
name: nexy-api
description: Create or modify NEXY API endpoints through Request, Schema, Auth, RBAC, Validation, Business Rule, Core, Response and Audit gates.
---

# NEXY Skill

## Identity
- Formal ID: `API-001`
- Name: `nexy-api`
- Family: API
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Create/modify API endpoint through Request → Schema → Auth → RBAC → Validation → Business Rule → Core → Response → Audit.

## Authority
API mutation requires explicit scope and cannot bypass Core/Law, auth/RBAC, contract or audit authority.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current API/schema/core implementation at exact HEAD.

## Scope
### In Scope
Authorized endpoint/handler/schema wiring, auth/RBAC, validation, core call, response/error contract, audit, tests.
### Out of Scope
Invented endpoints/providers, direct persistence bypassing architecture, auth/RBAC weakening.

## Inputs
Universal inputs plus route/method, request/response/error schema, auth/RBAC, business rule, core contract and audit obligations.

## Outputs
Universal outputs plus endpoint contract, auth/RBAC behavior, validation map, core integration, response/error/audit behavior, tests/evidence.

## Workflow
Context → Authority → Requirement/Contract → Inspect Consumers/Core/Security → Implement → Contract/Security/Integration Test → Evidence.

## Required Behavior
Follow Request → Schema → Auth → RBAC → Validation → Business Rule → Core → Response → Audit in applicable form; explicit errors; no fake success.

## Forbidden Behavior
No unauthenticated protected path, schema bypass, direct secret exposure, silent error, or contract drift without authority.

## Architecture Constraints
API is a boundary; Core/state ownership remains downstream according to architecture.

## Security Constraints
Authn/authz/RBAC/input/rate/session/CSRF/audit controls apply as source requires.

## Compatibility Constraints
Inspect consumers before changing request/response/error contract.

## Data Integrity
Mutating endpoints must preserve authoritative persistence/transaction/idempotency rules.

## Failure Handling
Boundary validation/security/core failure returns explicit governed error; no success envelope.

## Freeze Conditions
Critical auth/schema/core contract unknown, security violation, state/persistence ambiguity, stale target.

## Validation
Request, response, errors, auth, RBAC, schema, status, abuse, integration and regression as applicable.

## Completion Criteria
Endpoint behavior is source-backed, secure, compatible and evidence-validated.

## Stop Conditions
Missing critical contract/auth/core source, forbidden path, human gate or stale HEAD.

## Checkpoint
Persist endpoint version, schemas, security mapping, changed files and evidence.

## Resume
Refresh route/schema/core consumers/HEAD.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A write endpoint cannot call storage directly if architecture requires Core/service ownership.

## Non-Goals
This Skill does not approve release.

## Version
1.0.0
