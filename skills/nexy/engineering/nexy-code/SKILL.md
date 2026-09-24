---
name: nexy-code
description: Create NEXY code only from source-backed requirements and inspected architecture, with explicit scope, contract, security, test and evidence gates.
---

# NEXY Skill

## Identity
- Formal ID: `ENG-001`
- Name: `nexy-code`
- Family: ENGINEERING
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Create code supported by inspected source, requirements and architecture without assuming a language, framework, provider or stack is canonical unless the current source/repository establishes it.

## Authority
This Skill may propose or perform code creation only when the task grants the required mutation authority. Materialization of this Skill does not grant WRITE/TEST permission by itself and cannot override protected/human-gated boundaries.

## Source of Truth
- Primary skill specification: `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current implementation decisions require exact repository/branch/HEAD inspection.

## Scope
### In Scope
- implement authorized new code from explicit requirements;
- preserve architecture, contracts, security, state/data and compatibility;
- create the minimum coherent change needed for acceptance;
- add/update tests only when authorized and required by the change;
- produce diff, validation and evidence.

### Out of Scope
- speculative features;
- architecture invention;
- unrelated refactor;
- provider/dependency invention;
- weakening tests/specification;
- release/deployment approval.

## Inputs
### Required
- task
- authority
- scope
- repository
- branch
- head
- source_of_truth
- constraints
- expected_output
- validation_requirements
- normalized_requirement
- architecture_context
- allowed_change_surface
- forbidden_change_surface

### Optional
- contracts
- state/FSM
- security constraints
- existing implementation patterns
- tests
- change-impact output

## Preconditions
- requirement is established;
- target HEAD is pinned;
- architecture needed for the change is known;
- scope is authorized;
- required contracts/security constraints are known or explicitly BLOCKED.

## Outputs
- status
- objective
- scope
- inputs
- actions
- changed_files
- unchanged_files
- diff
- impact
- tests
- validation
- evidence
- errors
- unknowns
- remaining
- rollback
- next_action

## Workflow
### Phase 1 — Context
Pin target revision and inspect current implementation surface.

### Phase 2 — Authority
Confirm allowed mutation and protected/human-gated surfaces.

### Phase 3 — Requirement
Bind implementation to explicit acceptance, contracts and non-goals.

### Phase 4 — Inspection
Inspect architecture, source patterns, callers/consumers, tests and dependency constraints.

### Phase 5 — Execution
Implement the smallest coherent source-backed change. Do not widen scope.

### Phase 6 — Validation
Compile/typecheck/build and run applicable unit/contract/integration/security/regression tests required by the task.

### Phase 7 — Evidence
Return exact changed files, diff, commands/results, failures and rollback.

## Required Behavior
- Missing requirement → BLOCK.
- Unknown architecture affecting correctness → BLOCK.
- Invalid/unknown required contract → BLOCK.
- Security violation → BLOCK/FREEZE.
- Test failure → NOT VERIFIED.
- Scope expansion → STOP.
- Preserve existing compatibility unless explicit authority changes it.
- Use inspected repository patterns instead of inventing technology choices.

## Forbidden Behavior
- Do not create placeholder implementation counted as complete.
- Do not silently add dependencies.
- Do not delete/weaken tests to pass.
- Do not swallow errors or fabricate success.
- Do not change unrelated files.
- Do not claim VERIFIED without executed evidence.

## Architecture Constraints
All new code must fit current legal module/layer boundaries or require an explicit architecture change authority.

## Security Constraints
Validate inputs/outputs, auth/RBAC, secrets, logging, tenant boundaries and audit obligations when applicable.

## Compatibility Constraints
Preserve API/schema/event/state semantics and dependency compatibility unless explicitly changed by authoritative requirement.

## Data Integrity
Any persistent/data mutation requires known ownership, atomicity/migration/rollback constraints as applicable.

## Failure Handling
On build/test/security failure, return the failure with evidence and do not convert partial implementation into completion.

## Freeze Conditions
Critical authority/scope/architecture/security/data uncertainty; required contract missing; unsafe irreversible mutation; stale target before execution.

## Validation
### Structural
Changed files remain inside authorized surface and output contract is complete.
### Functional
Acceptance behavior is demonstrated by applicable tests.
### Security
Applicable negative/security tests pass.
### Architecture
No unauthorized boundary/dependency violation.
### Integration
Consumers and integration edges remain compatible.
### Regression
Affected regression surface passes.
### Evidence
Every completion claim binds to actual diff and executed results.

## Completion Criteria
Complete only when the authorized implementation exists, required validation has executed successfully, evidence is traceable and no critical unknown remains.

## Stop Conditions
Missing requirement, unknown critical architecture, invalid contract, security violation, scope expansion, forbidden path, human gate, or stale HEAD.

## Checkpoint
Persist START_HEAD, change plan, changed files, test/evidence status and rollback.

## Resume
Refresh HEAD and revalidate diff/impact before continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Add a source-backed API helper only after inspecting the existing contract, consumers and tests.
- Refuse to invent a new framework merely because the requirement says “web”.

## Non-Goals
This Skill does not approve release or redefine requirements/architecture.

## Version
1.0.0
