# NEXY EPC Compatibility Proof Compiler 20 — Remote Index

CHAT_ID: `CHAT-20261005-0314-NEXY-EPC-CPC20`
CLASS: `Lo4 AI proposal / experimental / non-canonical / non-governing`

## Published bundle
`CPC20_FULL_SOURCE.tar.gz`

SHA-256: `21f1cd6a1ba87e27658da0ea3cd36e62b85dc25212a800fd2f0e45cb7efabc4e`

The archive contains the complete exact locally verified project tree excluding generated `dist/` output. It includes:
- execution memory and task contract;
- architecture and all 20 concept specifications;
- NEXY exact-baseline compatibility record;
- novelty/collision analysis;
- TypeScript source for all 20 analyzers plus Q64.64/canonicalization/runtime validation/compiler;
- tests and verification scripts;
- exact verification log;
- reference compatibility dossier;
- SHA-256 source/design/test manifest;
- local final audit;
- EPC vote-budget state.

## Local verification sealed before publication
- TypeScript strict compile: PASS
- Node tests: 36/36 PASS
- static determinism scan: 31 source files, 0 forbidden findings
- replay stress: 1000 iterations, 1 unique dossier hash
- reference dossier: PASS 20/20 analyzers
- source/design/test root hash: `36415c3b4daaa5acc8910a72d1678043a0e23d40bc0964344b463a0fc89f6857`
- reference dossier hash: `24073299e30d55d6dcaed39d18705a1fce04186708f03d0200ab65cb4988bd19`
- archive-vs-local recursive diff: PASS before publication

## Protected boundary
No NEXY.AI mutation is included or authorized. CPC20 cannot promote, cannot change Core state, cannot emit EPC KEEP/CUT, and requires external NEXY JUDGE/LAW/Human review for any future adoption.
