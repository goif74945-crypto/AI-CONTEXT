---
name: nexy-rbac
description: Verify NEXY OWNER, OPERATOR, AUDITOR, SYSTEM and PUBLIC_USER authorization rules and enforce protected decisions at the backend rather than UI-only.
---

# NEXY Skill

## Identity
- Formal ID: `SEC-003`
- Name: `nexy-rbac`
- Family: SECURITY
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Verify OWNER, OPERATOR, AUDITOR, SYSTEM, PUBLIC_USER and enforce RBAC at backend.

## Authority
Roles/permissions come from authoritative source. This Skill cannot create new privileges or infer role rights from UI visibility.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current permission matrix/backend guards at pinned HEAD.

## Scope
### In Scope
Role/action/resource matrix, backend authorization, denied paths, owner/system gates, tests/evidence.
### Out of Scope
Authentication identity proof, invented roles, client-only enforcement.

## Inputs
Universal inputs plus actor/role, action/resource, permission matrix and backend guard context.

## Outputs
Universal outputs plus authorization verdict, governing rule, enforcement location, denied/allowed evidence and gaps.

## Workflow
Context → Authority → Permission Rule → Inspect Backend Enforcement → Positive/Negative Test → Evidence.

## Required Behavior
Backend is authoritative; least privilege; explicit deny for unauthorized operations; protected/human gates preserved.

## Forbidden Behavior
No UI-only authorization, privilege inference, role escalation or cross-tenant bypass.

## Architecture Constraints
RBAC gates protected API/Core/state operations at legal boundary.

## Security Constraints
Tenant isolation, owner/system privilege, session identity and audit obligations as applicable.

## Compatibility Constraints
Permission changes require affected consumer/role analysis.

## Data Integrity
Unauthorized actor cannot write authoritative state.

## Failure Handling
Unknown/absent critical rule => BLOCKED; unauthorized => explicit deny.

## Freeze Conditions
Privilege escalation, cross-tenant access, unauthorized control, permission conflict.

## Validation
Role × action negative/positive tests, backend enforcement, session integration, audit and regression.

## Completion Criteria
All in-scope protected actions have source-backed backend enforcement evidence.

## Stop Conditions
Permission source unresolved, human gate, security boundary expansion or stale target.

## Checkpoint
Persist role/action/resource/rule/enforcement evidence.

## Resume
Refresh role matrix and guards.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Hiding an OWNER button from PUBLIC_USER is insufficient if the API still accepts the request.

## Non-Goals
This Skill does not authenticate the user by itself.

## Version
1.0.0
