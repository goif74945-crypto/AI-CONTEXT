# Verified Artifact Bundle

The five adjacent `.b64.part-XX` files are consecutive chunks of one Base64-encoded deterministic XZ-compressed tar archive.

Expected concatenated Base64 length: `33384` characters.
Expected decoded archive SHA-256:
`33fc410780ebfb819130453f0995c8e45c692c18fb321662745b9371ef47c90f`

Reconstruct and verify:

```bash
cat VERIFIED_ARTIFACT.tar.xz.b64.part-* | base64 -d > VERIFIED_ARTIFACT.tar.xz
echo "33fc410780ebfb819130453f0995c8e45c692c18fb321662745b9371ef47c90f  VERIFIED_ARTIFACT.tar.xz" | sha256sum -c -
mkdir recovered
tar -xJf VERIFIED_ARTIFACT.tar.xz -C recovered
cd recovered
sha256sum -c MANIFEST.sha256
npm run verify
```

This transfer form preserves the exact locally tested bytes through a UTF-8-only repository contents interface.
