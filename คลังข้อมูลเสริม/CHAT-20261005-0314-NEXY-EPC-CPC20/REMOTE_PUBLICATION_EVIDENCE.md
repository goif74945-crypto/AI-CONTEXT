# CPC20 Remote Publication Evidence

CHAT_ID: `CHAT-20261005-0314-NEXY-EPC-CPC20`
EVIDENCE_CLASS: `E0_REMOTE_READBACK + E1_STATIC_COMPILE + E2_EXECUTED_TESTS`
AUTHORITY_CLASS: `LO4_ADVISORY_ONLY / NON_CANONICAL / NON_GOVERNING`

## Scope
- Writable repository used: `goif74945-crypto/AI-CONTEXT`.
- Writable namespace used: `คลังข้อมูลเสริม/CHAT-20261005-0314-NEXY-EPC-CPC20/**`.
- Protected repository inspected read-only: `goif74945-crypto/NEXY.AI-`, branch `NEXY.ai`.
- No write action was sent to a repository whose name contains `NEXY.AI`.

## Exact NEXY baseline
- NEXY commit before work: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- NEXY tree before work: `a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c`
- NEXY commit after publication/readback: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- NEXY tree after publication/readback: `a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c`
- Protected-target result: `UNCHANGED_AT_OBSERVED_BASELINE`

## Local verification sealed before publication
- TypeScript strict compile: PASS
- Node tests: 36/36 PASS
- Static determinism scan: 31 TypeScript source files, 0 forbidden findings
- Replay stress: 1000 iterations, 1 unique dossier hash
- Reference dossier: PASS, 20/20 analyzers
- Reference dossier hash: `24073299e30d55d6dcaed39d18705a1fce04186708f03d0200ab65cb4988bd19`
- Source/design/test manifest entries: 50
- Source/design/test root hash: `36415c3b4daaa5acc8910a72d1678043a0e23d40bc0964344b463a0fc89f6857`
- Archive SHA-256: `21f1cd6a1ba87e27658da0ea3cd36e62b85dc25212a800fd2f0e45cb7efabc4e`
- Archive vs local verified tree (excluding generated dist): PASS

## Publication commits
- part00: `49b5b225ed079027c44f150efed08c741c5ed1da`
- part01: `7a8a5244b33c97f3fc29e7ce7a8fa02f6e918611`
- part02: `2f6f704b60968a2e658270d40ed12694c2c20401`
- part03: `fbab2d58fc2f9894852a5fb203464c77923cca50`
- part04: `6d1af9ecb63757334439223f0f9f1c31be931aa4`
- part05: `3b77543144ea3df76a9b78e7cab98d19902afec2`
- part06: `7b45088f091f3e7875a3347d25caee0ede23caf9`
- REMOTE_INDEX.md: `27c4c81bdd438861f8a80efa1664553b42c57863`
- BUNDLE_SHA256.txt: `e73427e38853bb46503965f4db74972cbff586f9`

## Remote blob read-back
Expected and observed Git blob SHA values were identical:
- part00: `d071ce7630aad45e5f0b17ec49f87298fdfc784b`
- part01: `7edd9a805e107f7a52400913688b40158968a7a8`
- part02: `13aa87b47bb5474897b2558d258a7076329622e4`
- part03: `a151cda20f3d5329d172aa59d0cc35208a71b6eb`
- part04: `8c859d255b4d506a7abf4cebb049a110b833c9b8`
- part05: `59465b40859aeffe160c6c51c3384345de5d452e`
- part06: `1b56c7ad4512a34e3707bea58e6e7dbd3ba54179`
- REMOTE_INDEX.md: `e6ecf6891896ba92f69121dde322e440c0c58689`
- BUNDLE_SHA256.txt: `1ec7efce3ff4ca4962fe676011b6e67bbff14060`

## Remote reconstruction proof
The intended remote representation was reconstructed by:
1. taking the exact no-newline base64 text bytes represented by part00 through part06;
2. concatenating in numeric part order;
3. base64-decoding;
4. SHA-256 hashing and byte-comparing with the locally sealed tarball.

Result:
- reconstructed SHA-256: `21f1cd6a1ba87e27658da0ea3cd36e62b85dc25212a800fd2f0e45cb7efabc4e`
- byte comparison to sealed local tarball: PASS
- because every remote Git blob SHA matched its exact expected text bytes, the read-back establishes that the remote parts reconstruct the sealed archive.

## Concurrency incident and recovery
One create-file attempt for part04 received GitHub HTTP 409 because AI-CONTEXT/main advanced concurrently. No force update was used. The branch head was refreshed and the new-file write was retried normally. The final remote blob was read back and matched the intended bytes.

## EPC authority/vote state
- CPC20 verdicts are PASS / FAIL / DEFER only.
- CPC20 cannot promote a proposal.
- CPC20 cannot mutate Core state.
- Test suite asserts that serialized CPC output contains neither `KEEP` nor `CUT`.
- KEEP entitlement for this CHAT_ID: UNUSED.
- CUT entitlement for this CHAT_ID: UNUSED.
- DEFER/WIP remains non-vote state.

## AI-CONTEXT publication observation
AI-CONTEXT main observed after bundle/index/receipt read-back:
- commit: `0373fc3bd048f111ba5c31ae1a329a667be04204`
- tree: `74ebf82ab5827e8b0acafab8def8a196304d9f69`

This observation may advance later because other chats share the repository; the artifact identities above remain content-addressed evidence.
