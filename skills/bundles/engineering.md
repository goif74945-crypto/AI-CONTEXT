# AI-CONTEXT Skill Bundle: engineering

Each section is independently addressable by Registry locator. Version: 1.0.0.

## SKILL:ENG-001
### Identity
- id: ENG-001
- name: root-cause
- category: engineering
- version: 1.0.0
- status: MATERIALIZED

### Objective
Reproduce, localize and prove root cause before selecting a fix.

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

## SKILL:ENG-002
### Identity
- id: ENG-002
- name: codebase-audit
- category: engineering
- version: 1.0.0
- status: MATERIALIZED

### Objective
Inspect a repository for structure, behavior, dependencies, risks and verification state.

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
- ARCH-001
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

## SKILL:ENG-003
### Identity
- id: ENG-003
- name: full-stack-build
- category: engineering
- version: 1.0.0
- status: MATERIALIZED

### Objective
Coordinate frontend, backend, contracts, data and tests into a bounded implementation flow.

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
- CORE-003
- ARCH-002
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

## SKILL:ENG-004
### Identity
- id: ENG-004
- name: production-implementation
- category: engineering
- version: 1.0.0
- status: MATERIALIZED

### Objective
Implement production changes with validation, security, compatibility and evidence.

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
- CORE-003
- ARCH-001
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

## SKILL:ENG-005
### Identity
- id: ENG-005
- name: refactor-safely
- category: engineering
- version: 1.0.0
- status: MATERIALIZED

### Objective
Refactor while preserving behavior, contracts, compatibility and regression safety.

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
- ENG-002
- CORE-010
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

