# Exact Tested Bundle Manifest

Purpose: preserve the exact source/tests/config bytes that produced the recorded E1/E2/E3 results.

## Archive identity
Logical archive: ATOQ_CODE_TESTS.tar.xz
Archive byte size: 18336
Archive SHA-256: b3460fe3456288af7085aeb3a120bf8cef11416bc95695ccb3315a60ae6bea78
Archive expected Git blob SHA-1 if stored as one binary blob: 1a409a6baf0b899364fd997c4badb532a020bb0c
Files in archive: 15
Deterministic tar metadata: fixed 2026-10-05 mtime, uid/gid 0; run_static_audit.sh mode 755.

The archive is stored as 5 concatenated base64 text parts so every transport piece can be independently content-addressed.

| Part | Chars | SHA-256 of text | Git blob SHA-1 |
|---|---:|---|---|
| part01 | 6000 | 8d9152a6fc13ecdd551ac1f13891529b801aa501cf4ab8edbbf646f98ccd0505 | 8eee6238c3a87c29abefa29781fbc207c0fba068 |
| part02 | 6000 | bc5d58cebdfacc452ebef5483a9b25a9e26138ceeca937b62d62571ae9e77072 | a3901c8473d261a65a3fe589adb3012466890ff5 |
| part03 | 6000 | 97f705724a79429e304342b9add97e76ecf835bf60268373dfc831dcb430dd2b | 176eb6690d90692569dc1896c8e5f6eb61ce6aa1 |
| part04 | 6000 | 025f14c8aa4827fa66a0aa0e3734edbc3ee55e2d32c934a965b4250789de94b3 | b3ea3dfc1e9aefb6e2c2d03dee4cfe72ce3fa666 |
| part05 | 448 | 6903598535642ac83411f35ffca817b6f51dd61a94146df9b9a858013d7779b7 | 4303e1879f9b02033c407dd800fe08ded0d7af19 |

## Reconstruction
Concatenate part01 through part05 with no inserted bytes.
Base64-decode the concatenated text to ATOQ_CODE_TESTS.tar.xz.
Verify SHA-256 equals b3460fe3456288af7085aeb3a120bf8cef11416bc95695ccb3315a60ae6bea78.
Extract with an xz-capable tar implementation.

Example logical flow:
cat bundle/ATOQ_CODE_TESTS.tar.xz.b64.part01 bundle/ATOQ_CODE_TESTS.tar.xz.b64.part02 bundle/ATOQ_CODE_TESTS.tar.xz.b64.part03 bundle/ATOQ_CODE_TESTS.tar.xz.b64.part04 bundle/ATOQ_CODE_TESTS.tar.xz.b64.part05 > /tmp/atoq.b64
base64 -d /tmp/atoq.b64 > /tmp/ATOQ_CODE_TESTS.tar.xz
sha256sum /tmp/ATOQ_CODE_TESTS.tar.xz
tar -xJf /tmp/ATOQ_CODE_TESTS.tar.xz

## Exact source/test SHA-256 identities
bdb2bf281a0dfd68a15e50a07b16661d910fc714be2fa1e78bbc57dbe8095109  node-shim.d.ts
7ea2f146bd9ded0fca4eb2ea9f01868ab734b4e616436660086f1edcb51a596d  package.json
79f46409a924452fa3420e27eb7a9ada967ba64fa58b15f62c6930743fad42ac  run_static_audit.sh
e7f14f895b4a90c3a40772e1297ad56061ba969cbae4ddd9542f35ba9f872684  src/aeap.ts
2bd4836895f2e567456d0ce8fa081fc0a576f62031985c5b90c6fcea52e79a0e  src/cdpp.ts
1a3d2a82eac807883b54c0506866723c14d6cfe18d33274379d09c205adfe441  src/core.ts
09b544683d8906012f490eaa8b9f9712db0f6e3d953ed55099a8b5a8015baf82  src/crg.ts
b5b017e7ab68fb80b857b8c144be1a195deaa850cca2c7fcf2e17f5bdb78b166  src/idw.ts
2123a7dc58f5c8e32f71424fa3d204a256643eac1d3222eeb513c1824d74ce2d  src/index.ts
a646a636ea4e6c102973753a9810090bb5a79b0b0e68e81456b74eabc0bf9f1e  src/nexy-adapters.ts
3dbf43a7d804ce33ec3042ab3e1f9f14c098a1189ad0b43df437fbd012d96fbd  src/rctc.ts
9cf61dc737c2828ba9e51ff639fd750cb6272231b95806b18f5eab4fd84c652c  tests/integration.test.ts
0d9474cbb50b681b33f4bb526e2a97242e6baefe57dcc9378b12712ed5cfac46  tests/property.test.ts
be0e70b14523d623a1be2e349513cd22eefc01d73a8d8c68eea20a5aa955763e  tests/unit.test.ts
2fd3e2b436be197bcbf72f3a32b2167b49d9a3b865607dea00c5c38751a2378d  tsconfig.json

## Trust note
The five part Git blob SHA-1 values were computed locally from the exact text and compared against GitHub create_blob returns before tree attachment. Any mismatch blocks attachment.
