# AI-CONTEXT Skill Bundle: research

Each section is independently addressable by Registry locator. Version: 1.0.0.

## SKILL:RESEARCH-001
### Identity
- id: RESEARCH-001
- name: deep-research
- category: research
- version: 1.0.0
- status: MATERIALIZED

### Objective
Perform structured source discovery, evidence extraction, cross-checking and synthesis.

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

## SKILL:RESEARCH-002
### Identity
- id: RESEARCH-002
- name: source-verification
- category: research
- version: 1.0.0
- status: MATERIALIZED

### Objective
Verify that a source actually supports the claim being used.

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

## SKILL:RESEARCH-003
### Identity
- id: RESEARCH-003
- name: fact-checking
- category: research
- version: 1.0.0
- status: MATERIALIZED

### Objective
Validate factual claims against appropriate evidence.

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
- RESEARCH-002
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

## SKILL:REDTEAM-001
### Identity
- id: REDTEAM-001
- name: red-team
- category: verification
- version: 1.0.0
- status: MATERIALIZED

### Objective
Search for failure modes, contradictions, bypasses and adversarial counterexamples.

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
- CORE-005
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

