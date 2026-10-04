# ECRPF-20 Source Bundle Manifest

STATUS: `VERIFIED_ON_PUBLICATION_BRANCH`

The exact locally tested source tree, tests, documents, and raw evidence are preserved as a gzip-compressed tar archive encoded as six ordered base64 parts:

1. `ECRPF20_SOURCE_BUNDLE.part00.b64`
2. `ECRPF20_SOURCE_BUNDLE.part01.b64`
3. `ECRPF20_SOURCE_BUNDLE.part02.b64`
4. `ECRPF20_SOURCE_BUNDLE.part03.b64`
5. `ECRPF20_SOURCE_BUNDLE.part04.b64`
6. `ECRPF20_SOURCE_BUNDLE.part05.b64`

## Reconstruction

```bash
cat ECRPF20_SOURCE_BUNDLE.part00.b64 \
    ECRPF20_SOURCE_BUNDLE.part01.b64 \
    ECRPF20_SOURCE_BUNDLE.part02.b64 \
    ECRPF20_SOURCE_BUNDLE.part03.b64 \
    ECRPF20_SOURCE_BUNDLE.part04.b64 \
    ECRPF20_SOURCE_BUNDLE.part05.b64 > ECRPF20_SOURCE_BUNDLE.tar.gz.b64

sha256sum ECRPF20_SOURCE_BUNDLE.tar.gz.b64
# expected: 1666cea55e55d401d82256de230721f68ed2c974e124f9876b499265e26bfcb2

base64 -d ECRPF20_SOURCE_BUNDLE.tar.gz.b64 > ECRPF20_SOURCE_BUNDLE.tar.gz
sha256sum ECRPF20_SOURCE_BUNDLE.tar.gz
# expected: 88b21831a64ddf64f0a29e4e1909b015e07e1ac1b96f417abf2c48b671679e0c

mkdir ecrpf20
tar -xzf ECRPF20_SOURCE_BUNDLE.tar.gz -C ecrpf20
cd ecrpf20
npm test
```

## Part evidence

| Part | chars | SHA-256 (part text) | Git blob SHA expected/observed |
|---|---:|---|---|
| 00 | 5000 | `63fa319d85e8ebff2f82cd0aacd9f8a7c43342868739cee9758f6656719375d7` | `8b3bcdb5cd1f6c9b23ff63f3ff4f08bbdd848e10` |
| 01 | 5000 | `246f5505bed4d1bca579c273a6797188341e77b444dd6a249720d4d597c94877` | `6c41d9bcebca5f4a74e3c3d4489a3f36137ed5eb` |
| 02 | 5000 | `3810ecb5269a8372a20aa15c2e84497f0f234bd1f572cbcf6fad4bfd95a883a1` | `a194fe69bc59d83d02dded41cc0bcb9548ce1503` |
| 03 | 5000 | `740329c0e6ef861637cee4bf77d4a48137646f54af02b2eb8664a1b9e2dce8c6` | `b78a667e3da6d3165f362cab2e93b456c1ad993d` |
| 04 | 5000 | `5452d3d72505ebe959b054e1e09eba63d9c4214f65282a612798bcd5618e9779` | `033197a53b4ba674c7870bb41eccd452118229f5` |
| 05 | 376 | `5faed0622fde531f10bd3df86219c15e2ccd97d288d0964bcafc08e868728705` | `b5f1a9b0775bdb4cbd3d7c65a4490d5839606316` |

All six Git blob SHAs were read back from the publication branch and matched locally computed `git hash-object` values exactly. The earlier oversized single-file upload attempt was proven truncated and removed from the unmerged publication branch before PR creation.

## Exact internal source manifest

The archive contains `evidence/SHA256SUMS.txt` with SHA-256 for the tested files. Key executable hashes:

- `src/engine.ts`: `bbd914ff164d20817ccc977fe2c0990e5af41da5d66e319408d5635dc46b8b9d`
- `src/q64.ts`: `321c44289cf17c4bfbd674e534e7c3c1e37d80b703de5d0ad8fcb8b2ade52361`
- `src/canonical.ts`: `e927556f58bb8244511072049147aa446d49ac965ef21997191b078e2f42bd70`
- `src/types.ts`: `54d47a8a3fe66d72a2881fd93d92a845c57e9512d83f9856312c0fadb40215e0`
- `tests/ecrpf.test.mjs`: `cab966ac2e379ba39ecb3d563847ab16a97a8c8bb60bab05f45a80052306e47d`
- final test log: `36c327553884605d875cbd35ccf7a0b733009fe4148212a52b980f7cb9ffadef`

The archive is a transport artifact only. It grants no Canon, Core, VERIFY, JUDGE, rollout, deployment, or NEXY mutation authority.
