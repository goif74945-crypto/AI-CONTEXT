# AI-CONTEXT Skill Bundle: meta

## Operational Definition
These are executable Skill definitions, not capability names. The Registry uses each `SKILL:<ID>` locator to load the exact procedure.

## SKILL:AI-001
### Identity
- id: AI-001
- name: skill-discovery
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:AI-001

### Objective
Find candidate Skills from the registry using intent, tags, category and constraints.

### Required Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- CORE-001
- CORE-004

### Execution Algorithm
1. Parse task.
2. Query indexes.
3. Filter by status/permissions.
4. Resolve semantic/tag matches.
5. Return candidates with reasons.

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

## SKILL:AI-002
### Identity
- id: AI-002
- name: skill-selection
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:AI-002

### Objective
Select a valid Skill set using scope, status, dependencies and permissions.

### Required Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- AI-001
- CORE-003

### Execution Algorithm
1. Validate candidates.
2. Resolve dependencies.
3. Check permissions.
4. Reject invalid candidates.
5. Produce deterministic selection.

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

## SKILL:AI-003
### Identity
- id: AI-003
- name: skill-compose
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:AI-003

### Objective
Compose selected Skills into a dependency-valid acyclic execution plan.

### Required Inputs
- task
- current_context
- authority
- scope
- expected_output
- validation_requirements

### Dependencies
- AI-002
- ARCH-003

### Execution Algorithm
1. Expand dependencies.
2. Topologically order.
3. Detect cycles.
4. Define node contracts.
5. Emit executable DAG.

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

## SKILL:AI-004
### Identity
- id: AI-004
- name: skill-execute
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:AI-004

### Objective
Execute a composed Skill plan with state, evidence and failure propagation.

### Required Inputs
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

### Execution Algorithm
1. Initialize state.
2. Run nodes in dependency order.
3. Persist outputs/evidence.
4. Propagate failures.
5. Stop safely.

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

## SKILL:AI-005
### Identity
- id: AI-005
- name: skill-verify
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:AI-005

### Objective
Verify execution results, evidence, scope and completion criteria.

### Required Inputs
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

### Execution Algorithm
1. Check outputs.
2. Check requirements.
3. Check evidence.
4. Check scope.
5. Assign final status.

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

