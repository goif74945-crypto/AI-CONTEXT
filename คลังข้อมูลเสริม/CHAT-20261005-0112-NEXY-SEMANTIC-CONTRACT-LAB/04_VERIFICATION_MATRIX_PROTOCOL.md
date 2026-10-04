# Verification Matrix Protocol

## Matrix Schema
For every requirement record:
requirement_id | statement | criticality | verifier | evidence | observed_result | status | timestamp | notes

## Verifier Classes
V1 Existence: required artifact/resource exists.
V2 Content: expected semantic content is present.
V3 Structural: schema/shape/interface is valid.
V4 Behavioral: system behaves correctly under execution.
V5 Negative: forbidden behavior does not occur under defined test.
V6 Persistence: state remains after write boundary/reload.
V7 Integration: downstream/upstream contract still works.
V8 Regression: previously verified behavior remains valid.
V9 Provenance: fact/claim can be traced to authority.
V10 Completion: all critical rows are terminal and passing.

## Evidence Strength
E0 assertion only.
E1 tool response without independent read-back.
E2 direct read-back/state observation.
E3 independent cross-check or deterministic test.
E4 multiple independent checks covering failure modes.

Critical completion should target E2+; destructive/high-impact changes should target E3 where tools permit.

## False Verification Patterns
- "Command exited 0" proves only process exit, not business correctness.
- "File created" does not prove content correctness.
- "Tests passed" is weak if tests do not map to requirements.
- "No error shown" is not proof of success.
- "UI looks right" does not prove persistence or backend semantics.
- "API returned 200" does not prove the intended record changed.
- "AI reviewer agrees" is not independent evidence unless grounded in observable state.

## Closure Algorithm
1. enumerate critical requirements;
2. assign verifier class;
3. execute verification;
4. attach evidence;
5. mark PASS/FAIL/UNKNOWN/BLOCKED;
6. fix FAIL;
7. re-run impacted tests;
8. require zero unresolved critical rows for COMPLETE.

## Contradiction Rule
If two evidence items conflict:
- do not average them,
- do not choose the convenient one,
- mark CONTRADICTION,
- inspect authority, freshness, target identity, and measurement method,
- resolve before completion.
