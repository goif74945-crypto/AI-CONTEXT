---
name: nexy-auth
description: Govern NEXY authentication according to the current implementation/spec, including OTAC, session and logout where applicable, without inventing identity mechanisms or leaking secrets.
---

# NEXY Skill

## Identity
- Formal ID: `SEC-001`
- Name: `nexy-auth`
- Family: SECURITY
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Support authentication according to implementation/spec, including OTAC, session and logout where applicable.

## Authority
Authentication behavior is governed by current source/implementation. This Skill cannot invent MFA, providers, credentials or bypass authentication gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current auth/session source and tests at pinned HEAD.

## Scope
### In Scope
Auth request/verify/logout flows, OTAC where applicable, session creation/revocation, error/lock/rate behavior, secret-safe delivery/logging, tests/evidence.
### Out of Scope
Invented providers, credential exposure, auth bypass, RBAC decisions beyond authentication identity.

## Inputs
Universal inputs plus auth action, identity input, auth/session policy, delivery mechanism if established and security constraints.

## Outputs
Universal outputs plus auth_result, identity/session state, errors, security events, tests/evidence and next action.

## Workflow
Context → Authority → Auth Contract → Validate Input → Execute Established Auth Mechanism → Session/Incident Handling → Negative/Security Validation → Evidence.

## Required Behavior
Fail closed; single-use/expiry/lockout semantics when source requires; no plaintext OTAC/credential logging; logout/revocation explicit.

## Forbidden Behavior
No fake delivery success, raw secret/code/email logging where prohibited, auth bypass, hardcoded credentials or unapproved provider fallback.

## Architecture Constraints
Auth remains server-side authority and feeds session/RBAC boundaries.

## Security Constraints
Rate/guess controls, secure secret handling, session/cookie controls and incident logging as applicable.

## Compatibility Constraints
Preserve auth/error/session contract unless explicitly authorized.

## Data Integrity
Auth/session state ownership and revocation persistence must be respected.

## Failure Handling
Invalid/expired/locked/unavailable delivery paths return explicit error; no success.

## Freeze Conditions
Secret exposure, authority bypass, compromised auth state, critical security uncertainty.

## Validation
Positive/negative auth, expired/replay, lock/rate, logout/session, secret-log leakage and regression tests as applicable.

## Completion Criteria
Auth change/analysis is source-aligned and required security/test evidence passes.

## Stop Conditions
Unknown critical auth mechanism, secret/credential handling risk, protected scope, human gate or stale HEAD.

## Checkpoint
Persist auth flow/version, security state, tests and evidence without secrets.

## Resume
Refresh auth/session policy and target revision.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Console development delivery cannot log a raw OTAC and then report successful delivery if no secure delivery occurred.

## Non-Goals
This Skill does not decide application authorization roles.

## Version
1.0.0
