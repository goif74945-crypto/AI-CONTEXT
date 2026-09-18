# AI-CONTEXT Skill Bundle: core

Each section is independently addressable by Registry locator. Version: 1.0.0.

## SKILL:CORE-001
### Identity
- id: CORE-001
- name: context-load
- category: core
- version: 1.0.0
- status: MATERIALIZED

### Objective
Load authoritative current context before execution.

### Authority
Use caller authority and the AI-CONTEXT Registry. Never override higher-authority source material.

### Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- none

### Required Behavior
- Validate authority and scope before execution.
- Preserve evidence provenance.
- Distinguish FACT / ASSUMPTION / UNKNOWN.
- Preserve deterministic behavior for identical inputs and registry state.
- Propagate BLOCKED / FAIL / UNKNOWN.

### Forbidden Behavior
- Guessing or inventing facts, tools, requirements or evidence.
- Placeholder-based completion.
- Silent scope expansion.
- Skipping required validation.
- Claiming VERIFIED without evidence.

### Workflow
1. Load current context.
2. Validate authority and scope.
3. Validate inputs and dependencies.
4. Execute only this Skill's objective.
5. Record actions, outputs, evidence, errors and unknowns.
6. Run applicable validation.
7. Return explicit status.

### Failure / Freeze
Freeze or block on critical unresolved uncertainty, dependency failure, authority conflict, scope expansion or insufficient evidence.

### Validation
- Registry identity matches.
- Dependencies resolve without cycles.
- Scope is respected.
- Output contract is satisfied.
- Evidence is traceable.
- No false PASS condition exists.

### Output
Return: status, objective, actions, outputs, evidence, errors, unknowns, remaining.

## SKILL:CORE-002
### Identity
- id: CORE-002
- name: requirement-audit
- category: governance
- version: 1.0.0
- status: MATERIALIZED

### Objective
Convert a task into explicit objective, scope, constraints, inputs, outputs and acceptance criteria.

### Authority
Use caller authority and the AI-CONTEXT Registry. Never override higher-authority source material.

### Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-001

### Required Behavior
- Validate authority and scope before execution.
- Preserve evidence provenance.
- Distinguish FACT / ASSUMPTION / UNKNOWN.
- Preserve deterministic behavior for identical inputs and registry state.
- Propagate BLOCKED / FAIL / UNKNOWN.

### Forbidden Behavior
- Guessing or inventing facts, tools, requirements or evidence.
- Placeholder-based completion.
- Silent scope expansion.
- Skipping required validation.
- Claiming VERIFIED without evidence.

### Workflow
1. Load current context.
2. Validate authority and scope.
3. Validate inputs and dependencies.
4. Execute only this Skill's objective.
5. Record actions, outputs, evidence, errors and unknowns.
6. Run applicable validation.
7. Return explicit status.

### Failure / Freeze
Freeze or block on critical unresolved uncertainty, dependency failure, authority conflict, scope expansion or insufficient evidence.

### Validation
- Registry identity matches.
- Dependencies resolve without cycles.
- Scope is respected.
- Output contract is satisfied.
- Evidence is traceable.
- No false PASS condition exists.

### Output
Return: status, objective, actions, outputs, evidence, errors, unknowns, remaining.

## SKILL:CORE-003
### Identity
- id: CORE-003
- name: scope-guard
- category: governance
- version: 1.0.0
- status: MATERIALIZED

### Objective
Prevent unauthorized scope expansion and destructive or unrelated changes.

### Authority
Use caller authority and the AI-CONTEXT Registry. Never override higher-authority source material.

### Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-001
- CORE-002

### Required Behavior
- Validate authority and scope before execution.
- Preserve evidence provenance.
- Distinguish FACT / ASSUMPTION / UNKNOWN.
- Preserve deterministic behavior for identical inputs and registry state.
- Propagate BLOCKED / FAIL / UNKNOWN.

### Forbidden Behavior
- Guessing or inventing facts, tools, requirements or evidence.
- Placeholder-based completion.
- Silent scope expansion.
- Skipping required validation.
- Claiming VERIFIED without evidence.

### Workflow
1. Load current context.
2. Validate authority and scope.
3. Validate inputs and dependencies.
4. Execute only this Skill's objective.
5. Record actions, outputs, evidence, errors and unknowns.
6. Run applicable validation.
7. Return explicit status.

### Failure / Freeze
Freeze or block on critical unresolved uncertainty, dependency failure, authority conflict, scope expansion or insufficient evidence.

### Validation
- Registry identity matches.
- Dependencies resolve without cycles.
- Scope is respected.
- Output contract is satisfied.
- Evidence is traceable.
- No false PASS condition exists.

### Output
Return: status, objective, actions, outputs, evidence, errors, unknowns, remaining.

## SKILL:CORE-004
### Identity
- id: CORE-004
- name: evidence-first
- category: governance
- version: 1.0.0
- status: MATERIALIZED

### Objective
Require traceable evidence for substantive claims and completion state.

### Authority
Use caller authority and the AI-CONTEXT Registry. Never override higher-authority source material.

### Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-001

### Required Behavior
- Validate authority and scope before execution.
- Preserve evidence provenance.
- Distinguish FACT / ASSUMPTION / UNKNOWN.
- Preserve deterministic behavior for identical inputs and registry state.
- Propagate BLOCKED / FAIL / UNKNOWN.

### Forbidden Behavior
- Guessing or inventing facts, tools, requirements or evidence.
- Placeholder-based completion.
- Silent scope expansion.
- Skipping required validation.
- Claiming VERIFIED without evidence.

### Workflow
1. Load current context.
2. Validate authority and scope.
3. Validate inputs and dependencies.
4. Execute only this Skill's objective.
5. Record actions, outputs, evidence, errors and unknowns.
6. Run applicable validation.
7. Return explicit status.

### Failure / Freeze
Freeze or block on critical unresolved uncertainty, dependency failure, authority conflict, scope expansion or insufficient evidence.

### Validation
- Registry identity matches.
- Dependencies resolve without cycles.
- Scope is respected.
- Output contract is satisfied.
- Evidence is traceable.
- No false PASS condition exists.

### Output
Return: status, objective, actions, outputs, evidence, errors, unknowns, remaining.

## SKILL:CORE-005
### Identity
- id: CORE-005
- name: no-guess
- category: governance
- version: 1.0.0
- status: MATERIALIZED

### Objective
Block invented facts, unsupported assumptions, placeholders and fabricated mechanisms.

### Authority
Use caller authority and the AI-CONTEXT Registry. Never override higher-authority source material.

### Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-001
- CORE-004

### Required Behavior
- Validate authority and scope before execution.
- Preserve evidence provenance.
- Distinguish FACT / ASSUMPTION / UNKNOWN.
- Preserve deterministic behavior for identical inputs and registry state.
- Propagate BLOCKED / FAIL / UNKNOWN.

### Forbidden Behavior
- Guessing or inventing facts, tools, requirements or evidence.
- Placeholder-based completion.
- Silent scope expansion.
- Skipping required validation.
- Claiming VERIFIED without evidence.

### Workflow
1. Load current context.
2. Validate authority and scope.
3. Validate inputs and dependencies.
4. Execute only this Skill's objective.
5. Record actions, outputs, evidence, errors and unknowns.
6. Run applicable validation.
7. Return explicit status.

### Failure / Freeze
Freeze or block on critical unresolved uncertainty, dependency failure, authority conflict, scope expansion or insufficient evidence.

### Validation
- Registry identity matches.
- Dependencies resolve without cycles.
- Scope is respected.
- Output contract is satisfied.
- Evidence is traceable.
- No false PASS condition exists.

### Output
Return: status, objective, actions, outputs, evidence, errors, unknowns, remaining.

## SKILL:CORE-006
### Identity
- id: CORE-006
- name: no-false-pass
- category: verification
- version: 1.0.0
- status: MATERIALIZED

### Objective
Prevent PASS/COMPLETE claims without satisfying gates and evidence.

### Authority
Use caller authority and the AI-CONTEXT Registry. Never override higher-authority source material.

### Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-004
- CORE-005

### Required Behavior
- Validate authority and scope before execution.
- Preserve evidence provenance.
- Distinguish FACT / ASSUMPTION / UNKNOWN.
- Preserve deterministic behavior for identical inputs and registry state.
- Propagate BLOCKED / FAIL / UNKNOWN.

### Forbidden Behavior
- Guessing or inventing facts, tools, requirements or evidence.
- Placeholder-based completion.
- Silent scope expansion.
- Skipping required validation.
- Claiming VERIFIED without evidence.

### Workflow
1. Load current context.
2. Validate authority and scope.
3. Validate inputs and dependencies.
4. Execute only this Skill's objective.
5. Record actions, outputs, evidence, errors and unknowns.
6. Run applicable validation.
7. Return explicit status.

### Failure / Freeze
Freeze or block on critical unresolved uncertainty, dependency failure, authority conflict, scope expansion or insufficient evidence.

### Validation
- Registry identity matches.
- Dependencies resolve without cycles.
- Scope is respected.
- Output contract is satisfied.
- Evidence is traceable.
- No false PASS condition exists.

### Output
Return: status, objective, actions, outputs, evidence, errors, unknowns, remaining.

## SKILL:CORE-007
### Identity
- id: CORE-007
- name: requirement-trace
- category: governance
- version: 1.0.0
- status: MATERIALIZED

### Objective
Trace requirement to design, implementation, tests and evidence.

### Authority
Use caller authority and the AI-CONTEXT Registry. Never override higher-authority source material.

### Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-002
- CORE-004

### Required Behavior
- Validate authority and scope before execution.
- Preserve evidence provenance.
- Distinguish FACT / ASSUMPTION / UNKNOWN.
- Preserve deterministic behavior for identical inputs and registry state.
- Propagate BLOCKED / FAIL / UNKNOWN.

### Forbidden Behavior
- Guessing or inventing facts, tools, requirements or evidence.
- Placeholder-based completion.
- Silent scope expansion.
- Skipping required validation.
- Claiming VERIFIED without evidence.

### Workflow
1. Load current context.
2. Validate authority and scope.
3. Validate inputs and dependencies.
4. Execute only this Skill's objective.
5. Record actions, outputs, evidence, errors and unknowns.
6. Run applicable validation.
7. Return explicit status.

### Failure / Freeze
Freeze or block on critical unresolved uncertainty, dependency failure, authority conflict, scope expansion or insufficient evidence.

### Validation
- Registry identity matches.
- Dependencies resolve without cycles.
- Scope is respected.
- Output contract is satisfied.
- Evidence is traceable.
- No false PASS condition exists.

### Output
Return: status, objective, actions, outputs, evidence, errors, unknowns, remaining.

## SKILL:CORE-008
### Identity
- id: CORE-008
- name: contradiction-check
- category: verification
- version: 1.0.0
- status: MATERIALIZED

### Objective
Detect conflicting sources, requirements or outputs.

### Authority
Use caller authority and the AI-CONTEXT Registry. Never override higher-authority source material.

### Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-004

### Required Behavior
- Validate authority and scope before execution.
- Preserve evidence provenance.
- Distinguish FACT / ASSUMPTION / UNKNOWN.
- Preserve deterministic behavior for identical inputs and registry state.
- Propagate BLOCKED / FAIL / UNKNOWN.

### Forbidden Behavior
- Guessing or inventing facts, tools, requirements or evidence.
- Placeholder-based completion.
- Silent scope expansion.
- Skipping required validation.
- Claiming VERIFIED without evidence.

### Workflow
1. Load current context.
2. Validate authority and scope.
3. Validate inputs and dependencies.
4. Execute only this Skill's objective.
5. Record actions, outputs, evidence, errors and unknowns.
6. Run applicable validation.
7. Return explicit status.

### Failure / Freeze
Freeze or block on critical unresolved uncertainty, dependency failure, authority conflict, scope expansion or insufficient evidence.

### Validation
- Registry identity matches.
- Dependencies resolve without cycles.
- Scope is respected.
- Output contract is satisfied.
- Evidence is traceable.
- No false PASS condition exists.

### Output
Return: status, objective, actions, outputs, evidence, errors, unknowns, remaining.

## SKILL:CORE-009
### Identity
- id: CORE-009
- name: completeness-audit
- category: verification
- version: 1.0.0
- status: MATERIALIZED

### Objective
Check that required items are present and validated.

### Authority
Use caller authority and the AI-CONTEXT Registry. Never override higher-authority source material.

### Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-007
- CORE-006

### Required Behavior
- Validate authority and scope before execution.
- Preserve evidence provenance.
- Distinguish FACT / ASSUMPTION / UNKNOWN.
- Preserve deterministic behavior for identical inputs and registry state.
- Propagate BLOCKED / FAIL / UNKNOWN.

### Forbidden Behavior
- Guessing or inventing facts, tools, requirements or evidence.
- Placeholder-based completion.
- Silent scope expansion.
- Skipping required validation.
- Claiming VERIFIED without evidence.

### Workflow
1. Load current context.
2. Validate authority and scope.
3. Validate inputs and dependencies.
4. Execute only this Skill's objective.
5. Record actions, outputs, evidence, errors and unknowns.
6. Run applicable validation.
7. Return explicit status.

### Failure / Freeze
Freeze or block on critical unresolved uncertainty, dependency failure, authority conflict, scope expansion or insufficient evidence.

### Validation
- Registry identity matches.
- Dependencies resolve without cycles.
- Scope is respected.
- Output contract is satisfied.
- Evidence is traceable.
- No false PASS condition exists.

### Output
Return: status, objective, actions, outputs, evidence, errors, unknowns, remaining.

## SKILL:CORE-010
### Identity
- id: CORE-010
- name: compatibility-audit
- category: verification
- version: 1.0.0
- status: MATERIALIZED

### Objective
Check contracts, dependencies and compatibility impact.

### Authority
Use caller authority and the AI-CONTEXT Registry. Never override higher-authority source material.

### Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-007

### Required Behavior
- Validate authority and scope before execution.
- Preserve evidence provenance.
- Distinguish FACT / ASSUMPTION / UNKNOWN.
- Preserve deterministic behavior for identical inputs and registry state.
- Propagate BLOCKED / FAIL / UNKNOWN.

### Forbidden Behavior
- Guessing or inventing facts, tools, requirements or evidence.
- Placeholder-based completion.
- Silent scope expansion.
- Skipping required validation.
- Claiming VERIFIED without evidence.

### Workflow
1. Load current context.
2. Validate authority and scope.
3. Validate inputs and dependencies.
4. Execute only this Skill's objective.
5. Record actions, outputs, evidence, errors and unknowns.
6. Run applicable validation.
7. Return explicit status.

### Failure / Freeze
Freeze or block on critical unresolved uncertainty, dependency failure, authority conflict, scope expansion or insufficient evidence.

### Validation
- Registry identity matches.
- Dependencies resolve without cycles.
- Scope is respected.
- Output contract is satisfied.
- Evidence is traceable.
- No false PASS condition exists.

### Output
Return: status, objective, actions, outputs, evidence, errors, unknowns, remaining.

