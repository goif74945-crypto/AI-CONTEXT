# OXC Validation Report

Date: 2026-10-05 Asia/Bangkok  
Classification: reference implementation evidence only  
Environment: sandbox container, Node.js v22.16.0, TypeScript 5.8.3

## Claim 1 — TypeScript reference compiles under strict configuration

Evidence class: E1  
Command:

```bash
npm run build
```

Observed: PASS

Compiler options include `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noFallthroughCasesInSwitch`, `noImplicitReturns` and NodeNext module resolution.

## Claim 2 — Focused and negative-path unit behavior passes

Evidence class: E2  
Command:

```bash
npm run test
```

Observed:

- tests: 15
- pass: 15
- fail: 0
- cancelled: 0
- skipped: 0

Covered assertions include:

1. deterministic equal output for equal input;
2. input not mutated;
3. presentation preference cannot alter authorization/reasons/friction;
4. FREEZE mandatory signal;
5. ordinary mutation blocked under FREEZE;
6. non-owner recovery authority denied;
7. backend denial fails closed;
8. VIEW mutation denied;
9. VERIFIED truth requirement enforced;
10. CRITICAL + IRREVERSIBLE → DOUBLE_CONFIRM;
11. STOP blocks mutation/recovery;
12. duplicate action ids rejected;
13. unknown role rejected;
14. empty allowed-state contract rejected;
15. unknown friction value rejected.

The suite also contains two combinatorial loops:
- 576 role × mode × state × truth cases proving a backend-denied mutation is never ENABLED;
- 36 presentation preference combinations proving authorization projection invariance.

## Claim 3 — Published source blob identity matches tested source

The following local `git hash-object` values were computed after the final passing test run:

| File | Git blob SHA |
|---|---|
| package.json | 6ce6d214f50e6021905147d8540d47136c6f3eec |
| tsconfig.json | 3c2a1ac36b339a597b91b7965dc2ecc934e0a7c6 |
| src/index.ts | 281dfdb7575a93b7d54363b5a0f3f730a19849e0 |
| src/model.ts | e0d99608782c6ecdb22673602c5fe199a7ae4a08 |
| src/compiler.ts | 1f50d7bc723772c1b110f2aca777046c261367ea |
| tests/compiler.test.mjs | 384b1da453572862173c9b835636871c6aaea507 |

GitHub `create_blob` returned the exact same blob IDs for all six files before tree creation.

Status: PASS for byte identity between tested local files and staged Git blobs.

## SHA-256 fingerprints of tested local files

| File | SHA-256 |
|---|---|
| package.json | f61f1b402aa7130569b65fa67222f7b404f3d84b9d49e4ea05d96e21ccfe6ad0 |
| tsconfig.json | 3913936f4d04cc5040808d01682beaad98503964483357c83eb7e8628b09d133 |
| src/index.ts | d2a8d2f0636459a5342aa4f4659105f87346dd5f8e0fc2c902ebe35f55763943 |
| src/model.ts | 9a3dafbbf97772e59281a7962542f0f070e415e1c9e853276290d2885de3d678 |
| src/compiler.ts | a07824f303173530c533b95d6263ae461adf74f18260dcc66b4ca810196fb6b8 |
| tests/compiler.test.mjs | 6d48cf9e1b9a5bf3e2c6059e39ca3eca800685663cb99d75e484e12bc0c2b3d2 |

## What this does NOT prove

NOT VERIFIED:

- NEXY repository integration;
- browser E2E behavior;
- real backend permission integration;
- production security;
- stale-snapshot handling;
- accessibility;
- localization correctness;
- performance/load characteristics;
- deployment behavior;
- release readiness.

## Protected-scope check

No connector write action in this lab targeted a repository whose name contains `NEXY.AI`.

NEXY context was read from AI-CONTEXT only for authority alignment.
