# Future Integration / Conformance Plan

**Classification: AI proposal, not authorized NEXY implementation work.**

## Phase A — freeze byte contract
Promote the current vectors only after human/project review. Assign an immutable format identifier. Any incompatible rule becomes a new format version.

## Phase B — independent TypeScript port
Implement without copying Python runtime shortcuts. Consume `conformance/valid-vectors.json` and `invalid-vectors.json`; require exact UTF-8 canonical text and SHA-256 fingerprint equality.

## Phase C — differential corpus
Generate a deterministic corpus covering:
- nested arrays/objects;
- Unicode BMP and supplementary scalar values;
- escape-sensitive strings;
- safe integer boundaries;
- depth/node/output limits;
- invalid surrogate and normalization-collision cases.

Python and TypeScript must agree on every valid vector and every failure class.

## Phase D — integration adapter
Only after conformance PASS, define narrow adapters for candidate NEXY boundaries. A recommended first target is non-authoritative evidence-object fingerprinting because it is reversible and does not directly control execution.

## Phase E — rollout law
- shadow mode first;
- compare old/new identities;
- no automatic migration of existing Vault identifiers;
- freeze on mismatch;
- migration requires explicit version mapping and rollback plan.

## Adoption gates
1. zero vector mismatch;
2. explicit schema ownership;
3. collision/failure semantics reviewed;
4. no secret material hashed as a substitute for encryption;
5. production adapter has integration tests;
6. exact-head evidence exists for the integrating repository.
