---
name: nexy-integration-test
description: Validate NEXY interactions across real subsystem boundaries and dependency edges rather than isolated module presence.
---

# NEXY Skill

## Identity
- Formal ID: `TEST-004`
- Name: `nexy-integration-test`
- Family: TEST / VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Validate module boundaries. Validate NEXY interactions across real subsystem boundaries and dependency edges rather than isolated module presence.

## Authority
Testing validates established requirements and implementation behavior. This Skill cannot redefine requirements, weaken acceptance criteria, or self-approve unsupported claims.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current pinned implementation/test/evidence for the target under test.

## Scope
### In Scope
API→CORE, CORE→REPO/QUEUE, QUEUE→WORKER, AUTH→protected operations, STATE→persistence, RECOVERY→state and other applicable integration edges.
### Out of Scope
Replacing integration proof with mocks that remove the boundary under claim, ignoring dependency failures, or calling unit PASS integration PASS.

## Inputs
Universal inputs plus pinned target/version, requirement or change scope, applicable test commands/cases, environment/dependency state and prior evidence.

## Outputs
Universal outputs plus tests selected/run, exact results, failures, evidence bindings, residual gaps and next action.

## Workflow
Context → Boundary Graph → Preconditions → Exercise Real Edge → Negative/Failure Edge → State/Evidence Checks → Execute → Evidence.

## Required Behavior
Validate both sides of each applicable boundary, schema/state/authority handoff and failure propagation.

## Forbidden Behavior
Replacing integration proof with mocks that remove the boundary under claim, ignoring dependency failures, or calling unit PASS integration PASS.

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
Required dependency/environment missing with no safe substitute, stale head, or boundary authority unresolved.

## Validation
V0 file/command integrity; V1 structure; V2 source/spec alignment; V3 behavior; V4 security; V5 architecture impact; V6 integration; V7 regression; V8 evidence; V9 completion proof as applicable.

## Completion Criteria
Applicable integration edges pass positive and negative behavior with evidence bound to the target.

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
