# Sealed Source Bundle — NEXY Lo4 Anti-Goodhart Q64 Foundry 20

Status: VERIFIED_PUBLICATION_BUNDLE
Classification: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`
Work code: `CHAT-20261005-0229-NEXY-LO4-ANTI-GOODHART-Q64-20`

This directory stores the exact verified project as a base64-split XZ tar archive because the repository connector is text-oriented. The archive contains Design + Code + Tests + Evidence + final wheel.

## Archive identity
- Reconstructed archive: `nexy_lo4_antigoodhart_q64_20-full.tar.xz`
- Archive SHA-256: `46bb4e0e7d8e5a9ca262462c6c08e639d109e7cbd7f16c34d2335b368b9563d6`
- Archive byte size: 42,368
- Base64 total length: 56,492
- Parts: `part-00.b64` through `part-09.b64`, lexical order
- Wheel: `nexy_lo4_antigoodhart_q64-0.1.0-py3-none-any.whl`
- Wheel SHA-256: `130dd3791fb2ba51fda3c2a564987087eb722a4073a9370c669d17f22090e83a`
- Tested-bytes manifest SHA-256: `4a8b8a23f8dabd769191bad95cfdf1d1eb4b95f1c107d3ae43eee1f4f922ddd0`

## Reconstruction
From this directory:

```sh
cat part-00.b64 part-01.b64 part-02.b64 part-03.b64 part-04.b64 \
    part-05.b64 part-06.b64 part-07.b64 part-08.b64 part-09.b64 > bundle.b64
base64 -d bundle.b64 > nexy_lo4_antigoodhart_q64_20-full.tar.xz
sha256sum nexy_lo4_antigoodhart_q64_20-full.tar.xz
mkdir extracted
tar -xJf nexy_lo4_antigoodhart_q64_20-full.tar.xz -C extracted
cd extracted
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
python -m pip install --no-deps evidence/wheel-final/nexy_lo4_antigoodhart_q64-0.1.0-py3-none-any.whl
```

Expected archive SHA-256 is the value above. Do not trust or execute reconstructed bytes if the hash differs.

## Published part readback proof
Every part was re-fetched from GitHub after publication and its Git blob SHA matched the SHA computed from the exact local part bytes:

| Part | Expected/read-back Git blob SHA |
|---|---|
| part-00.b64 | 02b9d64a7b86802cbd5ce4bd6a9c512760cacae8 |
| part-01.b64 | ede57ec1f265a5358e98faa18d416285170a1911 |
| part-02.b64 | ffd2882c612bc6254336b5bccc8dc2f0d2b54b5c |
| part-03.b64 | 48465bfcc96530f5fa56c4e8af3a93d6660871c7 |
| part-04.b64 | e137474dd01507d75216ea1e5a6777f5a887d143 |
| part-05.b64 | 38e6d793afe49d667b520468eb38c71defbc791c |
| part-06.b64 | 3846e2ee2e17a154a49da8b1de78393bbb71005c |
| part-07.b64 | 548c7b6e4fd20eb0913544392731606c1887acd1 |
| part-08.b64 | af48e2ccb164c8eedef8b2ddb2c51e0fc4068992 |
| part-09.b64 | 99f08dab8b9fba60fd9382ddf50c611b43b92fc7 |

## Evidence boundary
This bundle proves only the isolated reference package at the exact tested bytes:
- E0 publication/readback: PASS
- E1 compile/static: PASS
- E2 unit/adversarial/boundary/property: PASS
- E3 isolated cross-engine integration: PASS

It does NOT prove NEXY.AI runtime integration, deployment, production security, user adoption, or Canon eligibility. No repository whose name contains `NEXY.AI` was mutated by this mission.
