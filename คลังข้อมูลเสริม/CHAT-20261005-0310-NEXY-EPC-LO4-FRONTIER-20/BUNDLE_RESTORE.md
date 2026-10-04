# Bundle restore

The full EPC project is stored as split base64 text parts so the AI-CONTEXT publication is transport-safe.

From this work directory after checkout:

```bash
cat bundle/BUNDLE.part* > /tmp/EPC_LO4_FRONTIER_20.tar.gz.b64
base64 -d /tmp/EPC_LO4_FRONTIER_20.tar.gz.b64 > /tmp/EPC_LO4_FRONTIER_20.tar.gz
printf '%s  %s\n' '4e24493cd39f89e48d7a2b31c18e6ce4f9a4bcd120c8315fb9a80cd9c8e99666' '/tmp/EPC_LO4_FRONTIER_20.tar.gz' | sha256sum -c -
tar -xzf /tmp/EPC_LO4_FRONTIER_20.tar.gz -C /tmp
cd /tmp/epc_lab
npm run test
```

Expected final local proof recorded in the bundle: 63 tests, 63 pass, 0 fail. The tarball SHA-256 above is the reconstruction identity.
