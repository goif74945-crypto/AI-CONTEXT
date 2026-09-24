---
name: nexy-security-test
description: Execute authorized NEXY security tests across applicable trust boundaries, misuse cases and negative controls without expanding attack scope.
---

# NEXY Skill

## Identity
- Formal ID: `TEST-006`
- Name: `nexy-security-test`
- Family: TEST / VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Security regression testing. Execute authorized NEXY security tests across applicable trust boundaries, misuse cases and negative controls without expanding attack scope.

## Authority
Testing validates established requirements and implementation behavior. This Skill cannot redefine requirements, weaken acceptance criteria, or self-approve unsupported claims.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current pinned implementation/test/evidence for the target under test.

## Scope
### In Scope
authn/authz/RBAC, secret leakage, input/output validation, injection, replay, rate/abuse, tenant/ownership boundaries, tool/plugin boundaries and security regressions.
### Out of Scope
Unauthorized penetration, secret extraction, cross-tenant testing without authority, disabling controls, or calling absence of an observed exploit secure.

## Inputs
Universal inputs plus pinned target/version, requirement or change scope, applicable test commands/cases, environment/dependency state and prior evidence.

## Outputs
Universal outputs plus tests selected/run, exact results, failures, evidence bindings, residual gaps and next action.

## Workflow
Context → Authority/Target → Threat Boundary → Safe Negative Cases → Execute → Inspect Logs/State → Regression → Evidence.

## Required Behavior
Use least privilege and approved targets; prove both blocked abuse and preserved legitimate behavior; redact secrets.

## Forbidden Behavior
Unauthorized penetration, secret extraction, cross-tenant testing without authority, disabling controls, or calling absence of an observed exploit secure.

## Architecture Constraints
Test scope follows real dependency/boundary ownership and must not replace architecture authority with test convenience.

## Security Constraints
Tests use only authorized targets/actions, redact secrets, preserve isolation and never expand privileges merely to obtain evidence.

## Compatibility Constraints
Validation includes compatibility effects when the tested contract/change can affect consumers, versions or stored state.

## Data Integrity
Test fixtures/results must not silently corrupt authoritative state; destructive cases require isolated/reversible environments and proper gates.

## Failure Handling
Any failed required test remains explicit; infrastructure/tool failure is distinguished from product failure and from NOT_RUN.

## Freeze Conditions
Unsafe target/action, missing authorization, human-gated boundary expansion, discovered secret, or destructive security test.

## Validation
V0 file/command integrity; V1 structure; V2 source/spec alignment; V3 behavior; V4 security; V5 architecture impact; V6 integration; V7 regression; V8 evidence; V9 completion proof as applicable.

## Completion Criteria
Applicable security tests pass with no unresolved critical finding and exact evidence is recorded.

## Stop Conditions
Stale HEAD, missing critical authority/environment, unsafe/destructive execution without gate, unresolved requirement conflict or unverifiable evidence.

## Checkpoint
Persist exact target/head, selected tests, command/result class, failures, evidence refs, remaining work and resume point.

## Resume
Refresh target HEAD, requirements/change impact, dependencies and previous test status before continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A test file that exists but has not been executed is `TEST_PRESENT`, not `TEST_PASS`.

## Non-Goals
This Skill does not convert a passing subset into whole-project verification.

## Version
1.0.0
