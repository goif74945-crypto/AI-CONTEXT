# AI-CONTEXT Skill Bundle: data

## Operational Definition
These are executable Skill definitions, not capability names. The Registry uses each `SKILL:<ID>` locator to load the exact procedure.

## SKILL:DATA-001
### Identity
- id: DATA-001
- name: data-integrity
- version: 1.1.0
- status: MATERIALIZED
- locator: SKILL:DATA-001

### Objective
Validate consistency, provenance, hashing and transformation integrity.

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
- CORE-005

### Execution Algorithm
1. Validate schema.
2. Check provenance.
3. Detect duplicates/corruption.
4. Verify transformations.
5. Record integrity evidence.

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

