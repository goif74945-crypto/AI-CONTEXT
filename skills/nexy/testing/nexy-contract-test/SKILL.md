---
name: nexy-contract-test
description: Validate NEXY schemas and producer/consumer contracts for exact shape, required fields, enums, versions, authorization/error semantics and compatibility.
---

# NEXY Skill

## Identity
- Formal ID: `TEST-003`
- Name: `nexy-contract-test`
- Family: TEST / VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Validate API/schema contracts. Validate NEXY schemas and producer/consumer contracts for exact shape, required fields, enums, versions, authorization/error semantics and compatibility.

## Authority
Testing validates established requirements and implementation behavior. This Skill cannot redefine requirements, weaken acceptance criteria, or self-approve unsupported claims.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current pinned implementation/test/evidence for the target under test.

## Scope
### In Scope
API/module/event/storage/queue schemas; serialization; required fields; enum exactness; producer-consumer compatibility; negative schema cases.
### Out of Scope
Approving incompatible shape drift, testing only happy-path examples, or changing the contract to match an implementation defect without authority.

## Inputs
Universal inputs plus pinned target/version, requirement or change scope, applicable test commands/cases, environment/dependency state and prior evidence.

## Outputs
Universal outputs plus tests selected/run, exact results, failures, evidence bindings, residual gaps and next action.

## Workflow
Context → Authority → Contract → Producers/Consumers → Positive Shape → Negative Shape → Compatibility → Execute → Evidence.

## Required Behavior
Exact required/forbidden values are tested; extra/missing fields and incompatible versions are rejected where required.

## Forbidden Behavior
Approving incompatible shape drift, testing only happy-path examples, or changing the contract to match an implementation defect without authority.

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
Contract authority conflict, unknown consumer impact, destructive compatibility break or unavailable current contract.

## Validation
V0 file/command integrity; V1 structure; V2 source/spec alignment; V3 behavior; V4 security; V5 architecture impact; V6 integration; V7 regression; V8 evidence; V9 completion proof as applicable.

## Completion Criteria
Contract behavior is proven for applicable producers/consumers with current evidence.

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
