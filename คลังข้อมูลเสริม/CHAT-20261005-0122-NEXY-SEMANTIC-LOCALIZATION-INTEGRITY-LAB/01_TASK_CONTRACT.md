# Task Contract

Status: ACTIVE UNTIL FINAL AUDIT

## Objective
Build a new, non-duplicative supplemental project useful to future NEXY.AI development, store it only in AI-CONTEXT, implement its core idea as working reference code, test it, and record evidence without modifying any NEXY.AI-named repository.

## Authorized scope
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-SEMANTIC-LOCALIZATION-INTEGRITY-LAB/**`

## Protected scope
- every repository whose name contains `NEXY.AI`;
- all pre-existing AI-CONTEXT sibling paths outside this new session folder;
- credentials/secrets/private tokens;
- production/runtime state.

## Authority sources
1. current explicit user request;
2. AI-CONTEXT execution/security/verification law;
3. NEXY project overview and current source-normalization authority boundaries;
4. current AI-CONTEXT repository evidence;
5. this lab's proposal documents only as non-authoritative design.

## Required outputs
- temporary/resumable execution memory;
- concept scope and divergence rationale;
- architecture and interfaces;
- invariants/failure model;
- machine-readable policy and request schemas;
- executable dependency-free reference implementation;
- fixtures and adversarial tests;
- validation script;
- proposal/adoption gates;
- evidence record;
- final audit.

## Immutable requirements
- no NEXY.AI repository mutation;
- no fake completion or fake testing;
- proposals must remain visibly non-authoritative;
- unsupported semantics must freeze rather than be silently accepted;
- deterministic output for identical relevant input/policy;
- no external runtime dependency required for the reference tests.

## Acceptance criteria
- all deliverables exist in the authorized folder;
- local static validation passes;
- all unit/adversarial tests pass;
- exact committed implementation is re-fetched and the same checks pass;
- final evidence names exact commit(s);
- no protected repository mutation is performed by this session.

## Stop conditions
- next write would touch a NEXY.AI-named repository;
- repository authority conflict invalidates the design;
- write cannot be made additive/safely rebased against current AI-CONTEXT HEAD;
- secret material would be persisted;
- required verification cannot be executed honestly.
