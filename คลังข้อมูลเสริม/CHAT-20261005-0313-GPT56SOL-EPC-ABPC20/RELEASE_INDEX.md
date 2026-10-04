# ABPC20 Remote Release Index

CHAT_ID: CHAT-20261005-0313-GPT56SOL-EPC-ABPC20
AUTHORITY: Lo4 AI proposal only; non-canonical; non-governing; no auto-promotion.

## Release
Archive: ABPC20_RELEASE.tar.gz
Archive SHA-256: efba8394d7fa00ca78a4c0bd712ac79ed0088b80651f0b96f038b863a8b6cd5c
Encoding: base64 without line wrapping, split in lexical order part00..part07.

Reconstruct:
```sh
cat ABPC20_RELEASE.tar.gz.b64.part{00,01,02,03,04,05,06,07} > ABPC20_RELEASE.tar.gz.b64
base64 -d ABPC20_RELEASE.tar.gz.b64 > ABPC20_RELEASE.tar.gz
printf "%s  %s\n" efba8394d7fa00ca78a4c0bd712ac79ed0088b80651f0b96f038b863a8b6cd5c ABPC20_RELEASE.tar.gz | sha256sum -c -
tar -xzf ABPC20_RELEASE.tar.gz
cd ABPC20
npm run verify
sha256sum -c evidence/SOURCE_HASHES.sha256
sha256sum -c evidence/EVIDENCE_HASHES.sha256
```

## Remote part Git-blob identities
- part00 d5954d23db89eadab7e2ccbabcde7841d05044cf (6000 chars)
- part01 0659f41202ddc83687761113ccad4cce0d205439 (6000 chars)
- part02 f871683292c6e2d36f836c8192d8ec7b1b5a56bc (6000 chars)
- part03 a2f29d6ed74d23e5f289631492d301049097401a (6000 chars)
- part04 05589673248efb203ee5fc1d6c0003cb6db0414a (6000 chars)
- part05 8d93ebb59cc13474f5b8600be74888e32308d097 (6000 chars)
- part06 746caa011129072a9d6c8b320d3660862e91e51b (6000 chars)
- part07 4c691207fcb27a96b5e0f55e1c63b3a743a6d00e (3436 chars)

All eight remote identities were read back after publication and matched the local git-hash-object identities.

## Verification sealed in archive
- TypeScript strict build: PASS
- Node test runner: 66/66 PASS
- Static deterministic-core guard: PASS
- 128 disjoint intents => Q64 contention 0
- 128 full-overlap intents => Q64 ONE
- 4,097 Q64 monotonic points
- 1,024 idempotent receipt recompilations
- 24 schedule permutations with identical deterministic conflict result
- clean archive restore + npm run verify: PASS
- source SHA-256 manifest: 45 entries verified
- evidence SHA-256 manifest: 10 entries verified

## Manifest seals
- SOURCE_HASHES.sha256 SHA-256: 71afad7f25d5370a275bbd0774d43cb7263066588badf4c007b5067dbb793400
- EVIDENCE_HASHES.sha256 SHA-256: 7c7d046270a736d0800dc19ce6026999d848ba1a852d0f48a40b1cc0b740d8ff
- MANIFEST_DIGESTS.txt SHA-256: a09573b35994a9674f6c2e250e5d1c66ac408f37373230672016a0a92894bddd

## Failure/recovery evidence
- Initial verify: unit/adversarial tests passed but static guard crashed on URL/path handling. Fixed with fileURLToPath; rerun passed.
- Post-pass audit found missing cross-object ballot/intent binding. Gate 20 was hardened and tests increased to 66.
- Live GitHub publication hit a 409 stale-head race during part05. No force update was used; head was refreshed and retry succeeded.
- Remote read-back detected a one-character corruption in part06; it was corrected before qualification and blob identity then matched.

## Contents
The archive contains Design, source Code, Tests, schemas, raw Evidence, manifests, restoration instructions, integration contract, failure model, final audit, and EPC vote protocol.
