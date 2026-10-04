# ARTIFACT RESTORE

The complete runnable project is stored as base64 text parts so GitHub/context tooling can preserve exact bytes without binary-upload assumptions.

From this folder:

```bash
cat artifact/nexy-lo4-q64-decision-utility-fabric.tar.gz.b64.part-* \
  | base64 -d > /tmp/nexy-lo4-q64-decision-utility-fabric.tar.gz
sha256sum /tmp/nexy-lo4-q64-decision-utility-fabric.tar.gz
# Compare with artifact/nexy-lo4-q64-decision-utility-fabric.tar.gz.sha256
tar -xzf /tmp/nexy-lo4-q64-decision-utility-fabric.tar.gz -C /desired/path
cd /desired/path
node --test tests/*.test.mjs
```

The expected archive SHA-256 is recorded in the `.sha256` file. The archive contains source, compiled `dist`, tests, schemas, raw evidence, docs and manifest.
