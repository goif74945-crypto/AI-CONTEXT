# AI-CONTEXT Skill Bundle: engineering

## Operational Definition
These are executable Skill definitions, not capability names. The Registry uses each `SKILL:<ID>` locator to load the exact procedure.

## SKILL:ENG-001
### Identity
- id: ENG-001
- name: root-cause
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:ENG-001

### Objective
Reproduce, localize and prove root cause before selecting a fix.

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
- CORE-004
- CORE-005

### Execution Algorithm
1. Reproduce failure.
2. Collect observations.
3. Narrow fault domain.
4. Test hypotheses.
5. Prove causal mechanism.

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

## SKILL:ENG-002
### Identity
- id: ENG-002
- name: codebase-audit
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:ENG-002

### Objective
Inspect a repository for structure, behavior, dependencies, risks and verification state.

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
- ARCH-001
- CORE-004

### Execution Algorithm
1. Inventory tree.
2. Inspect entry points.
3. Trace dependencies.
4. Inspect tests/config.
5. Map evidence and gaps.

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

## SKILL:ENG-003
### Identity
- id: ENG-003
- name: full-stack-build
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:ENG-003

### Objective
Coordinate frontend, backend, contracts, data and tests into a bounded implementation flow.

### Required Inputs
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

### Execution Algorithm
1. Freeze requirements.
2. Design contracts.
3. Implement layers.
4. Integrate.
5. Run verification.

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

## SKILL:ENG-004
### Identity
- id: ENG-004
- name: production-implementation
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:ENG-004

### Objective
Implement production changes with validation, security, compatibility and evidence.

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
- CORE-003
- ARCH-001
- CORE-004
- CORE-005

### Execution Algorithm
1. Audit current state.
2. Plan smallest safe change.
3. Implement.
4. Test.
5. Review diff.
6. Record evidence.

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

## SKILL:ENG-005
### Identity
- id: ENG-005
- name: refactor-safely
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:ENG-005

### Objective
Refactor while preserving behavior, contracts, compatibility and regression safety.

### Required Inputs
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

### Execution Algorithm
1. Baseline behavior.
2. Define invariant.
3. Refactor incrementally.
4. Run regression suite.
5. Compare behavior.

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

