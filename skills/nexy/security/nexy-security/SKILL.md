---
name: nexy-security
description: Apply NEXY security engineering across trust boundaries, input/output validation, secrets, auth, permissions, isolation, abuse, audit and fail-closed behavior.
---

# NEXY Skill

## Identity
- Formal ID: `SEC-004`
- Name: `nexy-security`
- Family: SECURITY
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
General security engineering.

## Authority
Security constraints cannot be weakened for convenience; security-boundary expansion requires applicable authority/human gate.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current security/trust-boundary implementation/evidence.

## Scope
### In Scope
Trust boundaries, validation, auth/authz, sessions, secrets/logging, tenant isolation, injection, replay, rate/abuse, sandbox/tool/plugin boundaries, audit/incident behavior.
### Out of Scope
Security theater, invented controls, secret extraction, unauthorized penetration activity.

## Inputs
Universal inputs plus security requirement, threat/trust boundaries and target change/system.

## Outputs
Universal outputs plus threats, controls, gaps, severity, tests/evidence and remediation class.

## Workflow
Context → Authority → Threat/Boundary Model → Inspect Controls → Attack/Negative Analysis → Validate → Evidence.

## Required Behavior
Zero-trust external/untrusted input; least privilege; fail closed on critical uncertainty; evidence-backed security claims.

## Forbidden Behavior
No secret leakage, privilege expansion, security bypass, fake “secure” claim or hidden unsafe fallback.

## Architecture Constraints
Security enforced at each real boundary; UI does not replace backend controls.

## Security Constraints
This section is itself normative: authn/authz/input/output/tenant/secret/replay/rate/audit/tool boundaries as applicable.

## Compatibility Constraints
Security fixes preserve contract behavior unless authoritative change requires otherwise.

## Data Integrity
Security review includes unauthorized mutation, replay/idempotency and isolation effects.

## Failure Handling
Critical vulnerability/control absence => FAIL/FREEZE affected path.

## Freeze Conditions
Secret exposure, privilege escalation, cross-tenant access, unauthorized control, fake evidence or critical unresolved security risk.

## Validation
Negative/security tests, abuse cases, injection/replay/isolation and regression as applicable.

## Completion Criteria
Applicable threats/controls are addressed and proven with current evidence.

## Stop Conditions
Unsafe test requires unapproved target/action, critical authority unknown or human gate.

## Checkpoint
Persist threats, controls, findings, tests and evidence without secrets.

## Resume
Refresh threat/control state and target HEAD.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Internal-origin queue payloads still require schema validation at producer/consumer trust boundaries.

## Non-Goals
This Skill does not claim absolute security.

## Version
1.0.0
