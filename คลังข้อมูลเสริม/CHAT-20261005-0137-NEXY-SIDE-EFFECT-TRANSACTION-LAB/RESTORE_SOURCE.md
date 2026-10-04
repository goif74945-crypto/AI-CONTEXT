# Restore the Tested Source Package

The exact tested implementation is stored as a deterministic gzip-compressed tar archive encoded as two plain-text base64 parts:

- `source/SOURCE_ARCHIVE.part00.b64`
- `source/SOURCE_ARCHIVE.part01.b64`

## Integrity

Expected compressed archive SHA-256:

`24749323ac0e6518f00c6071ec1a93a9fd8ab5c4a07d0d365789e927b5fdddf9`

Expected concatenated base64 text SHA-256:

`60d81bc8aff2fe9fcfcfb475af78c40250fddcbaee928bb0f0cd7f34ae144ff5`

## Restore

```bash
cat source/SOURCE_ARCHIVE.part00.b64 source/SOURCE_ARCHIVE.part01.b64 > source.b64
sha256sum source.b64
base64 -d source.b64 > source.tar.gz
sha256sum source.tar.gz
mkdir restored
tar -xzf source.tar.gz -C restored
cd restored
npm install
npm run verify
```

Archive contents:

- `package.json`
- `tsconfig.json`
- `src/canonical.ts`
- `src/types.ts`
- `src/planner.ts`
- `src/nexy-adapter.ts`
- `src/index.ts`
- `tests/planner.test.ts`
- `scripts/benchmark.mjs`

## Verification performed

The two exact generated parts were concatenated, decoded and extracted into a clean temporary directory. The archive SHA-256 matched and the restored package passed `npm run verify` with **47 passed / 0 failed** after the local test environment provided Node type declarations.

This proves archive fidelity and local E1/E2 reproducibility. It does not prove NEXY integration or deployment.
