# AI-CONTEXT Skill Bundle: meta

Each section is independently addressable by Registry locator. Version: 1.0.0.

## SKILL:AI-001
### Identity
- id: AI-001
- name: skill-discovery
- category: meta
- version: 1.0.0
- status: MATERIALIZED

### Objective
Find candidate Skills from the registry using intent, tags, category and constraints.

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

## SKILL:AI-002
### Identity
- id: AI-002
- name: skill-selection
- category: meta
- version: 1.0.0
- status: MATERIALIZED

### Objective
Select a valid Skill set using scope, status, dependencies and permissions.

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
- AI-001
- CORE-003

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

## SKILL:AI-003
### Identity
- id: AI-003
- name: skill-compose
- category: meta
- version: 1.0.0
- status: MATERIALIZED

### Objective
Compose selected Skills into a dependency-valid acyclic execution plan.

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
- AI-002
- ARCH-003

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

## SKILL:AI-004
### Identity
- id: AI-004
- name: skill-execute
- category: meta
- version: 1.0.0
- status: MATERIALIZED

### Objective
Execute a composed Skill plan with state, evidence and failure propagation.

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
- AI-003
- CORE-004
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

## SKILL:AI-005
### Identity
- id: AI-005
- name: skill-verify
- category: meta
- version: 1.0.0
- status: MATERIALIZED

### Objective
Verify execution results, evidence, scope and completion criteria.

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
- AI-004
- QA-002
- CORE-009

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

