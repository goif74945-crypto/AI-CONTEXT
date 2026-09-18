# AI-CONTEXT Skill Bundle: verification

## Operational Definition
These are executable Skill definitions, not capability names. The Registry uses each `SKILL:<ID>` locator to load the exact procedure.

## SKILL:QA-001
### Identity
- id: QA-001
- name: regression-audit
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:QA-001

### Objective
Identify and validate the regression surface created by a change.

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
1. Compute changed surface.
2. Trace dependents.
3. Select regression tests.
4. Run/inspect results.
5. Report uncovered risk.

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

## SKILL:QA-002
### Identity
- id: QA-002
- name: test-and-verify
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:QA-002

### Objective
Run applicable tests and verification gates and report evidence-backed status.

### Required Inputs
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

### Execution Algorithm
1. Discover test commands.
2. Run applicable checks.
3. Capture outputs.
4. Map results to requirements.
5. Assign status.

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

## SKILL:SEC-001
### Identity
- id: SEC-001
- name: security-audit
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:SEC-001

### Objective
Inspect authorization, input, secrets, dependencies, privacy and abuse surfaces.

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
- CORE-006

### Execution Algorithm
1. Threat-model surface.
2. Inspect trust boundaries.
3. Check auth/input/secrets.
4. Review dependencies.
5. Document findings.

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

