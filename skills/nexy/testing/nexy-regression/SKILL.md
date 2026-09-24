---
name: nexy-regression
description: After a change or remediation, validate the semantic regression surface implied by dependencies, contracts, state, security and prior failures.
---

# NEXY Skill

## Identity
- Formal ID: `TEST-007`
- Name: `nexy-regression`
- Family: TEST / VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Affected regression validation. After a change or remediation, validate the semantic regression surface implied by dependencies, contracts, state, security and prior failures.

## Authority
Testing validates established requirements and implementation behavior. This Skill cannot redefine requirements, weaken acceptance criteria, or self-approve unsupported claims.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current pinned implementation/test/evidence for the target under test.

## Scope
### In Scope
changed paths, dependency closure, linked requirements, historical failures, contract consumers, state/recovery/security neighbors and previously passing guarantees.
### Out of Scope
Running only the newly added test, ignoring adjacent systems, deleting old tests, weakening assertions or treating unrelated PASS as regression proof.

## Inputs
Universal inputs plus pinned target/version, requirement or change scope, applicable test commands/cases, environment/dependency state and prior evidence.

## Outputs
Universal outputs plus tests selected/run, exact results, failures, evidence bindings, residual gaps and next action.

## Workflow
Context → Diff/Change Impact → Regression Surface → Prior Failures/Golden Tests → Execute Applicable Suite → Semantic Compare → Evidence.

## Required Behavior
Regression scope is justified by dependency/change impact; existing guarantees must remain intact.

## Forbidden Behavior
Running only the newly added test, ignoring adjacent systems, deleting old tests, weakening assertions or treating unrelated PASS as regression proof.

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
Change impact cannot be established, target HEAD moved, required regression test unavailable or failure indicates unresolved regression.

## Validation
V0 file/command integrity; V1 structure; V2 source/spec alignment; V3 behavior; V4 security; V5 architecture impact; V6 integration; V7 regression; V8 evidence; V9 completion proof as applicable.

## Completion Criteria
Required regression surface is clean for the exact changed head with evidence and residual risk documented.

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
