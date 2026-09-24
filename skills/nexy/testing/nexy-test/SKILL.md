---
name: nexy-test
description: Orchestrate the applicable NEXY test stack without treating test presence as execution or partial PASS as completion.
---

# NEXY Skill

## Identity
- Formal ID: `TEST-001`
- Name: `nexy-test`
- Family: TEST / VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Test orchestration. Orchestrate the applicable NEXY test stack without treating test presence as execution or partial PASS as completion.

## Authority
Testing validates established requirements and implementation behavior. This Skill cannot redefine requirements, weaken acceptance criteria, or self-approve unsupported claims.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current pinned implementation/test/evidence for the target under test.

## Scope
### In Scope
unit, contract, integration, E2E, security, regression, build/typecheck/lint selection; dependency ordering; exact-head evidence binding.
### Out of Scope
Inventing PASS results, skipping required layers, weakening assertions, deleting failing tests, or claiming coverage from file presence.

## Inputs
Universal inputs plus pinned target/version, requirement or change scope, applicable test commands/cases, environment/dependency state and prior evidence.

## Outputs
Universal outputs plus tests selected/run, exact results, failures, evidence bindings, residual gaps and next action.

## Workflow
Context → Requirement/Impact → Select Applicable Test Layers → Pin Target → Execute/Inspect Real Tests → Classify Results → Regression/Evidence.

## Required Behavior
Applicable tests are chosen from requirement/change impact; failures stay visible; exact commands/results/head/environment are recorded.

## Forbidden Behavior
Inventing PASS results, skipping required layers, weakening assertions, deleting failing tests, or claiming coverage from file presence.

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
Test execution unavailable for a required proof, stale target, critical failed prerequisite, or a requested test would require unsafe mutation.

## Validation
V0 file/command integrity; V1 structure; V2 source/spec alignment; V3 behavior; V4 security; V5 architecture impact; V6 integration; V7 regression; V8 evidence; V9 completion proof as applicable.

## Completion Criteria
Required applicable test layers executed and evidence-bound; unresolved failures remain FAIL/PARTIAL rather than VERIFIED.

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
