# AI-CONTEXT Skill Bundle: architecture

## Operational Definition
These are executable Skill definitions, not capability names. The Registry uses each `SKILL:<ID>` locator to load the exact procedure.

## SKILL:ARCH-001
### Identity
- id: ARCH-001
- name: architect
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:ARCH-001

### Objective
Analyze structure, boundaries, dependencies, constraints and impact.

### Required Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-001
- CORE-002
- CORE-010

### Execution Algorithm
1. Inventory components.
2. Map boundaries.
3. Map dependencies.
4. Identify bottlenecks.
5. Produce architecture findings.

### Decision Rules
- Authoritative current evidence outranks secondary summaries.
- Missing evidence is UNKNOWN, not permission to infer.
- Requirements and scope are immutable unless explicitly changed by authorized input.
- Dependency failure blocks dependent execution unless a declared safe recovery exists.
- Identical task/context/registry/authority must yield the same decision class.

### Edge Cases
- Missing required input → BLOCKED and identify the field.
- Critical source conflict → FREEZE and expose both sources.
- Stale evidence → do not silently treat as current.
- Partial result → PARTIAL or NOT VERIFIED.
- Tool unavailable → UNKNOWN; never fabricate the result.
- Mid-run scope change → stop and re-audit.

### Evidence Contract
For each material conclusion record:
1. evidence type;
2. source/artifact;
3. exact locator when available;
4. observed result;
5. requirement/decision supported;
6. limitations and unknowns.

### Output Contract
Return:
- status: READY | RUNNING | PASS | PARTIAL | NOT VERIFIED | BLOCKED | FAIL | FREEZE
- actions
- outputs
- evidence
- errors
- unknowns
- remaining
- next_gate

### Validation Gates
- Registry identity matches.
- Dependencies resolve and are acyclic.
- Authority and scope are valid.
- Algorithm steps are completed or explicitly marked incomplete.
- Output contract is satisfied.
- Evidence supports the claimed status.
- No forbidden behavior occurred.

### Forbidden
- fabricated evidence;
- invented repository/system state;
- placeholder presented as implementation;
- unsupported PASS/VERIFIED;
- silent requirement change;
- destructive action outside authority.

### Stop Conditions
Authority conflict, unresolved critical contradiction, missing dependency, permission violation, integrity failure, or impossible validation requirement.

## SKILL:ARCH-002
### Identity
- id: ARCH-002
- name: system-design
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:ARCH-002

### Objective
Design a coherent system from requirements through interfaces, data and boundaries.

### Required Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- ARCH-001
- CORE-003

### Execution Algorithm
1. Convert requirements to architecture.
2. Define components/contracts.
3. Define data flow.
4. Define failure modes.
5. Define validation.

### Decision Rules
- Authoritative current evidence outranks secondary summaries.
- Missing evidence is UNKNOWN, not permission to infer.
- Requirements and scope are immutable unless explicitly changed by authorized input.
- Dependency failure blocks dependent execution unless a declared safe recovery exists.
- Identical task/context/registry/authority must yield the same decision class.

### Edge Cases
- Missing required input → BLOCKED and identify the field.
- Critical source conflict → FREEZE and expose both sources.
- Stale evidence → do not silently treat as current.
- Partial result → PARTIAL or NOT VERIFIED.
- Tool unavailable → UNKNOWN; never fabricate the result.
- Mid-run scope change → stop and re-audit.

### Evidence Contract
For each material conclusion record:
1. evidence type;
2. source/artifact;
3. exact locator when available;
4. observed result;
5. requirement/decision supported;
6. limitations and unknowns.

### Output Contract
Return:
- status: READY | RUNNING | PASS | PARTIAL | NOT VERIFIED | BLOCKED | FAIL | FREEZE
- actions
- outputs
- evidence
- errors
- unknowns
- remaining
- next_gate

### Validation Gates
- Registry identity matches.
- Dependencies resolve and are acyclic.
- Authority and scope are valid.
- Algorithm steps are completed or explicitly marked incomplete.
- Output contract is satisfied.
- Evidence supports the claimed status.
- No forbidden behavior occurred.

### Forbidden
- fabricated evidence;
- invented repository/system state;
- placeholder presented as implementation;
- unsupported PASS/VERIFIED;
- silent requirement change;
- destructive action outside authority.

### Stop Conditions
Authority conflict, unresolved critical contradiction, missing dependency, permission violation, integrity failure, or impossible validation requirement.

## SKILL:ARCH-003
### Identity
- id: ARCH-003
- name: dependency-audit
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:ARCH-003

### Objective
Resolve direct/transitive dependency and cycle impact.

### Required Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- ARCH-001
- CORE-010

### Execution Algorithm
1. Build dependency graph.
2. Detect cycles.
3. Trace versions.
4. Classify risk.
5. Recommend bounded resolution.

### Decision Rules
- Authoritative current evidence outranks secondary summaries.
- Missing evidence is UNKNOWN, not permission to infer.
- Requirements and scope are immutable unless explicitly changed by authorized input.
- Dependency failure blocks dependent execution unless a declared safe recovery exists.
- Identical task/context/registry/authority must yield the same decision class.

### Edge Cases
- Missing required input → BLOCKED and identify the field.
- Critical source conflict → FREEZE and expose both sources.
- Stale evidence → do not silently treat as current.
- Partial result → PARTIAL or NOT VERIFIED.
- Tool unavailable → UNKNOWN; never fabricate the result.
- Mid-run scope change → stop and re-audit.

### Evidence Contract
For each material conclusion record:
1. evidence type;
2. source/artifact;
3. exact locator when available;
4. observed result;
5. requirement/decision supported;
6. limitations and unknowns.

### Output Contract
Return:
- status: READY | RUNNING | PASS | PARTIAL | NOT VERIFIED | BLOCKED | FAIL | FREEZE
- actions
- outputs
- evidence
- errors
- unknowns
- remaining
- next_gate

### Validation Gates
- Registry identity matches.
- Dependencies resolve and are acyclic.
- Authority and scope are valid.
- Algorithm steps are completed or explicitly marked incomplete.
- Output contract is satisfied.
- Evidence supports the claimed status.
- No forbidden behavior occurred.

### Forbidden
- fabricated evidence;
- invented repository/system state;
- placeholder presented as implementation;
- unsupported PASS/VERIFIED;
- silent requirement change;
- destructive action outside authority.

### Stop Conditions
Authority conflict, unresolved critical contradiction, missing dependency, permission violation, integrity failure, or impossible validation requirement.

