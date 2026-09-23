# NEXY.AI Work Handoff Protocol

## Purpose
Make Builder ↔ Auditor ↔ Fixer ↔ new chat transfers deterministic enough to resume without re-reading the entire project or trusting unsupported claims.

## Required handoff object
Every handoff must contain:

`HANDOFF_ID`
`CREATED_AT`
`ROLE`
`TASK`
`TARGET {repo, branch, head}`
`SCOPE`
`INPUTS`
`OUTPUTS`
`CLAIMS`
`PROOF`
`TESTS`
`CHANGES`
`FINDINGS`
`UNRESOLVED`
`NEXT_ACTION`
`AUTHORITY`
`FRESHNESS`

## Protocol

### 1. Pin target identity
The sender records exact repository, branch and HEAD.  
If the receiver observes a different HEAD, implementation/test/evidence claims become stale until refreshed.

### 2. Separate claim classes
Every claim must be tagged as one of:
- SOURCE
- IMPLEMENTATION_E0
- STATIC_E1
- UNIT_E2
- INTEGRATION_E3
- E2E_E4
- RUNTIME_E5
- DEPLOYMENT_E6
- PHYSICAL
- INFERENCE
- UNKNOWN

### 3. Never hand off “done” without proof
A sender may say:
- `IMPLEMENTED_E0`
- `TESTED_E3`
- `BLOCKED`
- `NOT_VERIFIED`

But not generic “done” if the required evidence class is missing.

### 4. Preserve unresolved state
Unknown/conflict/blocker items must be copied verbatim enough to remain actionable.
Do not silently collapse them into assumptions.

### 5. Preserve authority/scope
The receiver must know:
- which source governs;
- what is current/future/excluded;
- whether mutation was authorized;
- which branches/files are protected.

### 6. Changes are explicit
For each change:
- repository/path;
- commit;
- semantic purpose;
- affected systems;
- affected requirements/invariants;
- regression obligations.

### 7. Resume rule
Receiver:
`VALIDATE HANDOFF → REFRESH TARGET → LOAD MINIMAL CONTEXT PACK → CONTINUE FROM NEXT_ACTION`

Do not restart discovery from zero unless handoff integrity fails.

## Handoff statuses
- VALID
- STALE_HEAD
- INCOMPLETE
- AUTHORITY_CONFLICT
- SCOPE_CONFLICT
- EVIDENCE_STALE
- BLOCKED

## Source of truth
A handoff is navigation state, not Canon.
Governance/requirements/evidence registries still win.
