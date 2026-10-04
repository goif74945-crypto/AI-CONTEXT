# Task Contract

## Objective
Produce and verify a standalone deterministic interchange reference system for future NEXY compatibility, stored only in AI-CONTEXT supplemental storage.

## Target
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0142-NEXY-DETERMINISTIC-INTERCHANGE-KERNEL/`

## Authorized scope
- create new files only inside the target folder;
- run local static/unit/property verification on the created implementation;
- record design, code, tests, evidence, manifest, and resumable state.

## Protected scope
- do not modify any repository whose name contains `NEXY.AI`;
- do not modify `projects/NEXY.AI/**` in AI-CONTEXT;
- do not modify sibling supplemental projects;
- do not create deployment/release claims.

## Authority sources
1. current user directive;
2. AI-CONTEXT `AI-EXECUTION-KERNEL.md`;
3. AI-CONTEXT NEXY overview/requirements/architecture context;
4. direct local test evidence.

## Success invariants
- deterministic canonical output for logically identical allowed values independent of dict insertion order;
- deterministic repeated execution;
- ambiguous/unsafe data rejected explicitly;
- resource limits enforced;
- envelope tampering detected;
- no implicit clock/random/environment input;
- all shipped tests pass;
- artifact hashes recorded.

## Forbidden behavior
- float coercion/rounding;
- silent duplicate-key overwrite in strict JSON parse;
- Unicode-normalized key collision acceptance;
- hidden fallback;
- implicit timestamp generation;
- NEXY.AI repository mutation;
- claiming production integration.

## Required evidence
- Python compile/static syntax check;
- executed pytest suite;
- example execution;
- deterministic benchmark/sanity record;
- SHA-256 manifest of deliverables.

## Stop conditions
Stop with NOT VERIFIED/BLOCKED if the test environment cannot execute or if repository publication cannot be confirmed.
