# NEXY Authority-Preserving Causal Merge Lab — Durable Record

Status: **EXPERIMENTAL / AI-PROPOSED / STANDALONE REFERENCE IMPLEMENTATION**
Date: 2026-10-05
Project-local work ID: `CHAT-20261005-0140-NEXY-CAUSAL-MERGE-LAB`
Platform immutable ChatGPT conversation ID: **UNKNOWN / not exposed by current toolset; not invented**

## 1. Objective

Build a standalone deterministic causal merge/reference implementation that may be adapted to NEXY.AI in the future while making **zero writes to any repository whose name contains `NEXY.AI`**.

This project is supplemental engineering work. It is not canonical NEXY law, not a DOC-C implementation change, and not evidence that current NEXY runtime already uses the design.

## 2. Source-grounded NEXY constraints

Context was read from `goif74945-crypto/AI-CONTEXT`, including:
- `projects/NEXY.AI/deep/doc-c-vnext-build-spec.md`
- `projects/NEXY.AI/deep/final-architecture-cross-system.md`
- `projects/NEXY.AI/overview.md`
- global/security/verification/workflow rules in AI-CONTEXT.

FACTS from those sources that shaped this lab:
- DOC-C is the narrow build obligation.
- vNEXT includes multi-agent debate/verification/consensus and Vault revisioning.
- `VAULT_COMMIT_CONFLICT` is a named error class.
- unresolved conflict must not be averaged or guessed through.
- validation includes SWARM result and VAULT commit boundaries.
- dependency law allows `CORE -> SWARM` and `CORE -> VAULT`, but **forbids `SWARM -> VAULT`**.
- Vault revisions are monotonic/no-overwrite and optimistic concurrency uses `previous_version`.
- Lo3 treats model intelligence as workers, not final authority.
- candidate output still passes constraints/evidence/Judge/Law/release or freezes.
- adaptive conflict is expected to branch/simulate rather than silently rewrite law.

Search evidence at inspection time returned zero direct AI-CONTEXT matches for CRDT/vector-clock/Lamport/causal-consistency terminology. This is only search evidence, not proof of absolute conceptual absence.

## 3. Design

### Core invariant set

1. Same valid operation set + same policy must converge to the same merge result or the same freeze certificate regardless of input permutation.
2. No last-write-wins. Arrival order, wall time, database race winner, model score, and locale ordering are not semantic authority.
3. Causality is explicit through positive-entry vector clocks and per-replica counters.
4. Concurrent divergent writes to the same semantic key freeze.
5. Concurrent writes to different keys commute.
6. Concurrent identical effects with identical preconditions coalesce.
7. Missing causal history, cycles, equivocation, tampering, unknown/insufficient authority, policy violations, resource violations, and failed preconditions fail closed.
8. Authority ranks and protected-key policies are injected configuration. The lab does not invent canonical NEXY authority law.
9. Active policy semantics are SHA-256 fingerprinted and bound into success/freeze evidence.
10. DELETE leaves a causal tombstone frontier.
11. Canonical ordering is locale-independent.
12. Canonical JSON uses null-prototype normalized objects, cycle detection, finite-number checks, negative-zero normalization, and a depth cap.
13. Resource limits bound operations, vector width, key bytes, evidence references, and canonical nesting.
14. No code imports from protected NEXY repositories.

### Operation model

`CausalOperation` includes:
- schemaVersion 1
- replicaId / actorId / authority
- positive safe-integer counter
- vector clock whose own replica entry equals counter
- semantic key
- SET or DELETE
- optional JSON value
- optional expected key digest for compare-and-set
- canonical sorted unique evidenceRefs
- operationId = SHA-256(canonical operation body)

### Replay

1. validate policy;
2. enforce resource bounds;
3. validate all raw operations as untrusted;
4. select failures deterministically rather than by input position;
5. deduplicate exact operation IDs;
6. reject same replica/counter with different IDs as equivocation;
7. construct exact causal dependencies;
8. reject missing predecessors;
9. topologically schedule with deterministic lexical min-heap;
10. apply key policy;
11. resolve against per-key frontier;
12. allow causal successor when precondition matches;
13. coalesce concurrent identical effect + precondition;
14. freeze divergent concurrency;
15. emit state/history/frontier/policy digests.

### Why conservative conflict handling

This reference is register-like per semantic key. It intentionally does not perform clever document/array/code merges. False conflict is preferable to silent semantic loss for a control system whose source direction is proof/freeze instead of guessing.

## 4. Future NEXY integration contract

**NOT IMPLEMENTED / NOT VERIFIED END-TO-END.**

Because DOC-C forbids `SWARM -> VAULT`, the merge gate must not become a persistence backdoor for workers.

Conceptual seam:

`SWARM candidate -> CORE -> causal merge/conflict gate -> CORE authorization/validation -> VAULT previous_version commit`

The lab augments, never replaces, Vault `previous_version` optimistic concurrency. A merge success does not mean a database/Vault commit succeeded. A later Vault conflict remains authoritative.

The generic adapter contract contains replicaId, actorId, authorityClass, observedClock, semanticKey, SET/DELETE action, optional value, optional expectedKeyDigest, and evidenceRefs. A future authorized NEXY adapter must map canonical identities/evidence/roles into this contract. Worker-provided authority labels must never be trusted directly.

Possible future failure mappings to `VAULT_COMMIT_CONFLICT`, freeze, law denial, or integrity incidents are proposals only until current NEXY contracts authorize and verify them.

## 5. Failure model

Freeze codes implemented:
- INVALID_OPERATION
- TAMPERED_OPERATION
- DUPLICATE_DOT_EQUIVOCATION
- CAUSAL_GAP
- CAUSAL_CYCLE
- AUTHORITY_UNKNOWN
- AUTHORITY_VIOLATION
- POLICY_VIOLATION
- PRECONDITION_MISMATCH
- CONCURRENT_DIVERGENT_WRITE
- RESOURCE_LIMIT

Freeze certificates include schema, code, sorted operation IDs, optional key, structured details, optional policy digest, and a canonical SHA-256 certificate digest. Wall-clock timestamps are excluded from certificate identity.

## 6. Repair log

Defects found and corrected during design/implementation review:
- strict TypeScript initially lacked Node crypto typings in the isolated environment; fixed with a minimal local declaration rather than disabling strict checks;
- exactOptionalPropertyTypes construction issues fixed;
- test harness shape corrected to avoid silent async mishandling;
- `localeCompare()` removed because locale/ICU can undermine cross-runtime determinism;
- zero-valued vector-clock entries rejected to avoid alternate canonical forms;
- repeated ready-array sorting replaced by deterministic min-heap;
- canonicalization changed to null-prototype objects to preserve `__proto__` as data rather than prototype mutation;
- cycle and excessive-depth canonical JSON rejected;
- policy semantics bound into outcome proof with policyDigest;
- ambiguous adapter precondition name changed to `expectedKeyDigest`;
- malformed evidence-ref errors separated from configured count-limit errors.

Residual risks: vector-clock growth, conservative conflicts, SHA-256 not being authentication, externally trusted replica identity requirement, no transactional store, no Byzantine consensus.

## 7. Executed verification

Latest full local command:
`npm run verify`

Pipeline:
- strict `tsc --noEmit`
- NEXY-style Node16/moduleResolution Node16 strict compatibility config
- build
- compiled test runner

Result:
**39 tests passed, 0 failed**

Coverage includes:
- canonical JSON and SHA-256 known vector;
- vector-clock relations;
- causal supersession;
- different-key concurrency;
- same-key divergent freeze;
- identical concurrent coalescing;
- idempotence;
- tamper/gap/cycle/equivocation detection;
- authority/policy/evidence/CAS gates;
- DELETE tombstones;
- deterministic failure selection;
- frontier digest stability;
- 500 merge permutations;
- 500 conflict permutations;
- 10,000 independent-operation stress path;
- dangerous property-name safety;
- JSON cycle/depth rejection;
- policy digest binding;
- generic NEXY adapter construction with no NEXY import.

One observed full verification run in the sandbox:
- wall: 2.56 seconds
- max RSS: 144368 KB

Those numbers are sandbox observations only, not production performance guarantees.

Evidence class:
- E1 static: PASS
- E2 executed/unit: PASS
- E3 actual NEXY integration: NOT_VERIFIED
- E4 user-flow/E2E: NOT_VERIFIED
- E5 runtime/operational: NOT_VERIFIED
- E6 deployment: NOT_VERIFIED

Observed NEXY repo currently declares TypeScript ^6.0.3; this isolated lab compatibility run used TypeScript 5.8.3, so exact TS 6.x workspace compatibility is NOT_VERIFIED.

## 8. Code/test preservation

Exact source+tests+configs are preserved losslessly in four base64 parts in this same folder:
- `CODE_TEST_BUNDLE.b64.part01`
- `CODE_TEST_BUNDLE.b64.part02`
- `CODE_TEST_BUNDLE.b64.part03`
- `CODE_TEST_BUNDLE.b64.part04`

Reconstruction:
`cat CODE_TEST_BUNDLE.b64.part01 CODE_TEST_BUNDLE.b64.part02 CODE_TEST_BUNDLE.b64.part03 CODE_TEST_BUNDLE.b64.part04 | base64 -d > CODE_TEST_BUNDLE.tar.gz`
then:
`tar -xzf CODE_TEST_BUNDLE.tar.gz`

Expected decoded tar.gz SHA-256:
`7f2e8d086f729597b0427ca7ea20949c7df7803a1745517644d8b89fafdea4ab`

Expected part SHA-256:
- part01: `ebc88b1c8dbc310731d895221db47365e8e19543f225df0afd12954c71676d22`
- part02: `e39322a184ab90f96bceaae22e1027878f7bd4c3e7acfecbf0b3fdf8531a4f91`
- part03: `c131567a855b8ad0d7aeaf820e00d87f29beeb52918351373e39fa8cce3166b1`
- part04: `4261a498fc1370b610c6d692782b91aae9771532ba0f87d30ec6fc0f0728159a`

Bundle contents:
- package.json
- tsconfig.json
- tsconfig.nexy-compat.json
- types/node-crypto.d.ts
- src/canonical.ts
- src/engine.ts
- src/index.ts
- src/nexy-adapter.ts
- src/operation.ts
- src/order.ts
- src/policy.ts
- src/types.ts
- src/vector-clock.ts
- tests/engine.test.ts
- tests/harness.ts
- tests/run.ts

Canonical local SHA-256 values for those files:
- package.json ee0757c00259526e39b592b84e83cf8090f69e21ed9fa2fb5667be5864cd414a
- src/canonical.ts 90a6396ce9b139be15c6cf3eef24cf9083a5cc6e306d466ac5471bbdab5f4079
- src/engine.ts 0a8ddffea6bd685dae66cd31423a33097caf5cc6245a4e5af33eac7187fc1fe0
- src/index.ts 2e5a4165f9991b014b18c048595d2077a41bf045f830f46d34481b3a71ccccda
- src/nexy-adapter.ts 34dca3a5efa06eeab774d4412de741aa731a84bd6dc622f5d7440c276834b4d2
- src/operation.ts 1359176d28d727f38194eca40512b74cc67f5f4cbc0f0ecbac3e674dcf77a84d
- src/order.ts 2fb74d735ffd82a839d1b3d3de7adab931b4dc6ee5008625b24405f1b56845ae
- src/policy.ts 5286e364094e5b719d10690fcbb400a3f17b3da1e4f213107c64c05550de7c2a
- src/types.ts e800548ddce3faafaf3be167c07cfdc79a36fe4b01dd093835dc90a76a1cfac8
- src/vector-clock.ts 4bed62b6ecc402fad9577682d160d0b7bde8ba3baecee1eda4f27032406eb70f
- tests/engine.test.ts 217cd85120de56b1c894f1dfc37b8c949ee9f59ae33f6977fab789ab303eb0b2
- tests/harness.ts 81ffee1c402cab50659870e5232c69698ed075b555c7ad413b86d70840acad2e
- tests/run.ts 03df5a80b9e01a719cf31f00b3599d7531c33f754ac8a5a26485f307172b5cae
- tsconfig.json 3fc476f6b86182ae8a9673198f451b08c47e31cd8c8687e652ba169b7bed7225
- tsconfig.nexy-compat.json 2701e5a04ac8624b092b987ee0ea96171885ccb7bac55ac1e3e5f33963c68090
- types/node-crypto.d.ts 42b00f55f7322643feff0dffc7f02a5b512f7f0c4f937aa414ec9d8a607aced0

## 9. Future ideas, not requirements

AI-proposed only:
- authenticated/signed operation envelopes;
- compact causal checkpoints;
- Merkle frontiers/proofs;
- formally proven domain-specific merge registry;
- TLA+/PlusCal model;
- seeded property/fuzz testing;
- cross-language Rust mirror with golden-vector parity;
- actual PostgreSQL/Vault serialization harness;
- merge evidence capsules tied to request/trace/incident IDs;
- explicit replica lifecycle/retirement law.

## 10. Final audit

Standalone authorized scope:
- design produced: PASS
- code produced: PASS
- tests produced/executed: PASS
- evidence produced: PASS
- repair/retest loop executed: PASS
- durable temporary/final state: PASS
- protected NEXY repo mutation: NONE
- actual NEXY integration/deployment: NOT VERIFIED and intentionally outside scope

Do not describe this lab as integrated into NEXY.AI until future explicit authorization and E3+ evidence exist.
