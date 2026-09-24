---
name: nexy-session
description: Verify and manage the NEXY session lifecycle, expiry, secure cookie behavior and revocation with explicit ownership and replay/security controls.
---

# NEXY Skill

## Identity
- Formal ID: `SEC-002`
- Name: `nexy-session`
- Family: SECURITY
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Verify session lifecycle, expiry, cookie/security and revocation.

## Authority
Session issuance/revocation follows auth/session source authority; client state cannot create or extend a valid session.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current session schema/store/cookie/auth code at pinned HEAD.

## Scope
### In Scope
Creation, lookup, expiry, cookie attributes, revocation/logout, replay/device checks where specified, persistence, tests/evidence.
### Out of Scope
RBAC role policy, invented session mechanism, client-only revocation.

## Inputs
Universal inputs plus session action/token reference, policy, identity, current time source when established and storage/security context.

## Outputs
Universal outputs plus session_status, expiry/revocation state, cookie/security assessment, tests/evidence.

## Workflow
Context → Authority → Session Contract → Inspect State/Store/Cookie → Execute/Validate Lifecycle → Security/Replay Tests → Evidence.

## Required Behavior
Expired/revoked session is invalid; logout must revoke according to source; cookie/security attributes follow current policy.

## Forbidden Behavior
No plaintext token logs, no stale session acceptance, no client-only trust.

## Architecture Constraints
Session authority lives at server/auth boundary and is consumed by protected APIs.

## Security Constraints
Secure cookie/session token handling, replay/device/session fixation controls as applicable.

## Compatibility Constraints
Preserve session cookie/contract names and lifecycle semantics unless authorized.

## Data Integrity
Revocation/expiry state must use authoritative storage when required.

## Failure Handling
Store failure/invalid session returns explicit denial/error.

## Freeze Conditions
Session authority ambiguity, secret exposure, unauthorized session acceptance or integrity compromise.

## Validation
Expiry, revocation, logout, cookie, replay/device and integration regression as applicable.

## Completion Criteria
Session lifecycle is source-aligned and validated with security evidence.

## Stop Conditions
Critical policy/store unknown, secret exposure risk, stale target.

## Checkpoint
Persist policy/version/state/evidence without token secrets.

## Resume
Refresh authoritative session state and policy.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A cookie name must come from current config/contract rather than a hardcoded historical value.

## Non-Goals
This Skill does not define RBAC permissions.

## Version
1.0.0
