---
name: nexy-e2e-test
description: Validate complete NEXY user/system flows through real applicable layers, preserving UI/API/state/failure truth.
---

# NEXY Skill

## Identity
- Formal ID: `TEST-005`
- Name: `nexy-e2e-test`
- Family: TEST / VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Validate real flows. Validate complete NEXY user/system flows through real applicable layers, preserving UI/API/state/failure truth.

## Authority
Testing validates established requirements and implementation behavior. This Skill cannot redefine requirements, weaken acceptance criteria, or self-approve unsupported claims.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current pinned implementation/test/evidence for the target under test.

## Scope
### In Scope
real journey from entry point through API/core/state/persistence and back; auth; freeze/error; final visible state; deployment-like environment where applicable.
### Out of Scope
Faking backend success, bypassing real auth/state boundaries, asserting only page rendering, or masking FREEZE/error as success.

## Inputs
Universal inputs plus pinned target/version, requirement or change scope, applicable test commands/cases, environment/dependency state and prior evidence.

## Outputs
Universal outputs plus tests selected/run, exact results, failures, evidence bindings, residual gaps and next action.

## Workflow
Context → User/System Flow → Preconditions → Execute End-to-End → Observe State/Output → Negative/Recovery Cases → Evidence.

## Required Behavior
Visible result must match authoritative backend/system state; critical side effects and persistence are checked.

## Forbidden Behavior
Faking backend success, bypassing real auth/state boundaries, asserting only page rendering, or masking FREEZE/error as success.

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
Required environment unavailable, destructive production mutation required without human gate, or flow cannot be safely reproduced.

## Validation
V0 file/command integrity; V1 structure; V2 source/spec alignment; V3 behavior; V4 security; V5 architecture impact; V6 integration; V7 regression; V8 evidence; V9 completion proof as applicable.

## Completion Criteria
Complete applicable flow passes with truthful output/state and current reproducible evidence.

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
