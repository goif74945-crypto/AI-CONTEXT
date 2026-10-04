# Verified Project Snapshot Bundle

**Session:** `NEXY-IIL-20261005-0121-TH`  
**Classification:** exact transport snapshot of the locally verified prototype.

The tested project archive was encoded as Base64 and split into seven text parts because the connected GitHub contents interface is text-oriented. All seven remote Git blob SHAs were fetched after upload and matched the locally calculated Git blob SHAs byte-for-byte.

## Reconstruct

From this directory:

```bash
cat nexy-iil-project.tar.gz.b64.part00 \
    nexy-iil-project.tar.gz.b64.part01 \
    nexy-iil-project.tar.gz.b64.part02 \
    nexy-iil-project.tar.gz.b64.part03 \
    nexy-iil-project.tar.gz.b64.part04 \
    nexy-iil-project.tar.gz.b64.part05 \
    nexy-iil-project.tar.gz.b64.part06 \
    > nexy-iil-project.tar.gz.b64

sha256sum nexy-iil-project.tar.gz.b64
base64 -d nexy-iil-project.tar.gz.b64 > nexy-iil-project.tar.gz
sha256sum nexy-iil-project.tar.gz
tar -xzf nexy-iil-project.tar.gz
cd nexy-intent-integrity-lab
npm run verify
```

Expected encoded snapshot:

- size: 50,340 bytes
- SHA-256: `32accbe8bfe2896caec71a615b25d3d4ee8cfc745fe0026967d1f854c2347073`

Expected decoded `.tar.gz`:

- size: 37,753 bytes
- SHA-256: `b322ce8d5c1db59ff23aff981ee53048680469cfc11b6d6d5af0ceaf6be25e43`
- Git blob SHA: `e6df5c651f38442b8c6687ad3af642eef75851d0`

## Verified remote part identity

| Part | Bytes | Git blob SHA |
|---|---:|---|
| part00 | 8000 | `43d6c0d6b92159b88d67df0637bb596ee1966baf` |
| part01 | 8000 | `fcb04ce9514ea363acf0ce36aaca88ff135e24e6` |
| part02 | 8000 | `ab36df5713b17bc73979756f0adbf3f26afbbd0f` |
| part03 | 8000 | `7aaf7126a408680682e0b7bd38a49a096fd6b1c6` |
| part04 | 8000 | `e8fe4bfb6731f41832597309f71598e314f05f6c` |
| part05 | 8000 | `b640a30f8102bf613f82b0edf00959836b4fba55` |
| part06 | 2340 | `ee0d17d03fb84204d5eb19b2a8578a4fff0adfeb` |

## Verification note

The project snapshot contains the complete source, tests, schemas, examples, architecture notes, differentiation audit, least-authority delegation design, evidence logs, and file manifests. The latest local regression rerun after remote upload also passed strict TypeScript typecheck and all 45 tests.

This archive is research/advisory material only. It is not integrated into NEXY.AI and does not authorize any NEXY.AI repository mutation.
