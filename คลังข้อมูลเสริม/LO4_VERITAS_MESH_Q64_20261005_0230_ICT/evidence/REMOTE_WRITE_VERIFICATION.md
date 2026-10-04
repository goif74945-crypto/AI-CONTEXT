# Remote Write Verification

Status: **PASS**

## Target
Repository: `goif74945-crypto/AI-CONTEXT`  
Branch verified: `main`  
VERITAS merge commit: `7eb5de0e9719217d71855aaa742a36a92eb0ee81`

## Verification method

Direct clone from the execution sandbox was attempted, but sandbox DNS could not resolve `github.com`. That path is therefore **BLOCKED by sandbox network**, not treated as proof.

Instead, the exact files executed locally were compared byte-for-byte using Git blob identity:

1. local file -> `git hash-object <file>`
2. remote `main` file -> GitHub Contents API blob SHA
3. require exact SHA equality

Git blob SHA equality proves identical byte content for the compared files.

## Exact blob matches: 12 / 12

| File | Local git hash-object | Remote main blob SHA | Result |
|---|---|---|---|
| package.json | 10998fe1244df500cc7eb230e2b57550b0de447c | 10998fe1244df500cc7eb230e2b57550b0de447c | PASS |
| tsconfig.json | fd92b041744a3ca86c065cdfa1441a19b75cba89 | fd92b041744a3ca86c065cdfa1441a19b75cba89 | PASS |
| bench.ts | 09caa7824a7331adbe27a8d0338cc28e7709a082 | 09caa7824a7331adbe27a8d0338cc28e7709a082 | PASS |
| src/index.ts | 8a5a6d86c66cfcf2ad7bd882f0af5b1bfb6a2877 | 8a5a6d86c66cfcf2ad7bd882f0af5b1bfb6a2877 | PASS |
| src/q64.ts | a76930f829beed84adfb7302dc15be5340413b4d | a76930f829beed84adfb7302dc15be5340413b4d | PASS |
| src/signals.ts | e8e889cafa56ebd0027818a181c73600b6e0e197 | e8e889cafa56ebd0027818a181c73600b6e0e197 | PASS |
| src/models.ts | c9300d10e8795feef4a6b0aa27fcb0b9bb0d1f8f | c9300d10e8795feef4a6b0aa27fcb0b9bb0d1f8f | PASS |
| src/promotion.ts | 9a21d1245772e24358b06eabcdde8bd2f4a9597d | 9a21d1245772e24358b06eabcdde8bd2f4a9597d | PASS |
| tests/q64.test.ts | 55303d7c99ad4e5894587fa084d7b3bb56d0f919 | 55303d7c99ad4e5894587fa084d7b3bb56d0f919 | PASS |
| tests/models.test.ts | f454af1842ca5c00d33ea215a82896306d49e3ad | f454af1842ca5c00d33ea215a82896306d49e3ad | PASS |
| tests/promotion.test.ts | 5dea8e460abba6f3a44208cdef22b05a77f4fa06 | 5dea8e460abba6f3a44208cdef22b05a77f4fa06 | PASS |
| types/node-shim.d.ts | eafc32106ce298357122bc29666d25f2c9861b07 | eafc32106ce298357122bc29666d25f2c9861b07 | PASS |

## Re-run after merge identity check

The local artifact whose 12 core/runtime/test files match remote `main` was rerun:

- `npm test`: **17/17 PASS**, 0 failed.
- `tsc -p tsconfig.json --pretty false`: **PASS**, no diagnostics.
- `npm run bench`: 10,000 decisions, 245.199 ms observed, 40,783.15 decisions/s in that rerun.
- deterministic final digest remained:
  `4fa8904e73a0dbf0f33a0f94506474b0a7f0fb4d2f4a07abdd57cd0d12f7f18f`

The throughput number is a local observation only, not an SLA.

## Protected-scope audit

No GitHub mutation tool was called against `goif74945-crypto/NEXY.AI-`.
NEXY.AI interactions in this work were read/search/fetch only.

## Result

The executable/static artifact stored on AI-CONTEXT `main` is byte-identical, for all 12 compared runtime/config/test files, to the artifact that passed the final local rerun.
