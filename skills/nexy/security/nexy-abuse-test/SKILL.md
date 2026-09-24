---
name: nexy-abuse-test
description: Test NEXY abuse and negative security scenarios within authorized safe scope, including unauthorized access, invalid input, replay, rate, injection and isolation failures as applicable.
---

# NEXY Skill

## Identity
- Formal ID: `SEC-008`
- Name: `nexy-abuse-test`
- Family: SECURITY
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Test abuse scenarios.

## Authority
Abuse testing is limited to authorized target/scope and cannot perform destructive or unauthorized real-world actions.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current threat model/contracts/security requirements at pinned target.

## Scope
### In Scope
Unauthorized access, invalid/malformed input, rate abuse, CSRF/session/RBAC where applicable, replay/idempotency, prompt/tool injection, tenant isolation and error leakage.
### Out of Scope
Credential theft, destructive exploitation, production abuse without explicit human gate.

## Inputs
Universal inputs plus abuse target, threat cases, environment and safety constraints.

## Outputs
Universal outputs plus cases, results, findings, proof, impacted controls, severity and next action.

## Workflow
Context → Authority/Safety Scope → Threat Cases → Execute Safe Negative Tests → Observe → Reproduce → Evidence.

## Required Behavior
Use safe bounded cases; prove boundary failure without unnecessary data exposure/damage.

## Forbidden Behavior
No unapproved production/destructive tests, no secret harvesting, no persistence outside authorized test scope.

## Architecture Constraints
Test actual trust/security boundaries.

## Security Constraints
Least privilege, isolated fixtures, sanitized evidence and rate/resource bounds.

## Compatibility Constraints
Tests must not modify specification to pass.

## Data Integrity
Use reversible/non-destructive fixtures; clean up authorized test state.

## Failure Handling
Unsafe environment/test => BLOCKED rather than executed.

## Freeze Conditions
Test exposes active S5-like defect or continued testing risks harm/data loss.

## Validation
Reproducible negative results, control assertions and regression mapping.

## Completion Criteria
Applicable authorized abuse cases executed and results evidenced, or explicitly blocked with reason.

## Stop Conditions
Production/destructive/human gate, insufficient isolation or secret risk.

## Checkpoint
Persist test IDs, sanitized inputs/results and findings.

## Resume
Refresh target/control state and ensure fixtures remain safe.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Attempt a protected endpoint as PUBLIC_USER in an isolated test and verify backend denial; do not treat hidden UI as proof.

## Non-Goals
This Skill does not conduct unrestricted penetration testing.

## Version
1.0.0
