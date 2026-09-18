# AI-CONTEXT Skill Bundle: verification

Each section is independently addressable by Registry locator. Version: 1.0.0.

## SKILL:QA-001
### Identity
- id: QA-001
- name: regression-audit
- category: qa
- version: 1.0.0
- status: MATERIALIZED

### Objective
Identify and validate the regression surface created by a change.

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

## SKILL:QA-002
### Identity
- id: QA-002
- name: test-and-verify
- category: verification
- version: 1.0.0
- status: MATERIALIZED

### Objective
Run applicable tests and verification gates and report evidence-backed status.

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
- CORE-006
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

## SKILL:SEC-001
### Identity
- id: SEC-001
- name: security-audit
- category: security
- version: 1.0.0
- status: MATERIALIZED

### Objective
Inspect authorization, input, secrets, dependencies, privacy and abuse surfaces.

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

