# Publication Evidence

## Repository target
`goif74945-crypto/AI-CONTEXT`

Namespace:
`คลังข้อมูลเสริม/CHAT-20261005-0230-NEXY-LO4-OUTCOME-MECHANICS-LAB/`

Initial project publication commit:
`1f28bc3fb8dfaa18b5e9c9215420878f77baa2c4`

Exact-bundle repair/seal commit:
`09fd9dc0299f8e9b30c39085b6c4327d8bbeac30`

Both writes used fast-forward-only ref updates with `force=false`; repeated concurrent-main races were retried against refreshed HEADs. No other chat folder was overwritten.

## Exact source archive
SHA-256:
`99d61fc903013f1c99d09719fbbcbd62b7a5bda6bff2a208034d3db6a500bac7`

Current-main bundle readback after repair:
- part-00.b64 — 7000 bytes — Git blob `2fa80f5abf9e23cd770974ee8e1a527996253e68`
- part-01.b64 — 7000 — `78d9b2e52bc0902b7ffc2bdb7a8d8b4f3b462a02`
- part-02.b64 — 7000 — `a4564dfc435179ff927d1125f5417c82b0a80747`
- part-03-0.b64 — 1000 — `d895bb533eacf8c5cd1acec55a3a63702d95d810`
- part-03-1.b64 — 1000 — `6c698cc580c53e6e58682eb88d407949b5b3ad47`
- part-03-2.b64 — 1000 — `b1b7253155678e9956649c5f2aae26b62af26e84`
- part-03-3.b64 — 1000 — `56c762fe1f4f103f617da4f7277831e8002e13b3`
- part-03-4.b64 — 1000 — `207ca2593c239ed7a9c919360bad0f1c0f65ba73`
- part-03-5.b64 — 1000 — `14952f4a112b4aff17be258181711fd5c21f262a`
- part-03-6.b64 — 1000 — `51696526b9834a94c9a06a37289ab68d5bda0e91`
- part-04.b64 — 4468 — `46e0163090d6b805824612cdd70471a0be49feff`

The obsolete malformed `part-03.b64` was removed from the tree.

## Reassembly and execution proof
The exact local equivalents of the persisted Git blobs were concatenated in the published explicit order, decoded, and produced the expected archive SHA-256. The archive was then extracted into a clean directory and `npm run verify` executed:
- TypeScript compile: PASS
- tests: 29
- pass: 29
- fail: 0
- skipped: 0
- todo: 0

This is E1 + E2 + local E3 evidence for the standalone artifact only.
