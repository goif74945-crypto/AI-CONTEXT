# Decode and Verify

Canonical reachable package:
`epc-jurisprudence20.tar.gz.b64`

```bash
base64 -d epc-jurisprudence20.tar.gz.b64 > epc-jurisprudence20.tar.gz
printf '%s  %s\n' \
  b71547f52482c8d633a2b953b70124ee8e33e425f9ab134a1d7561d03a070440 \
  epc-jurisprudence20.tar.gz | sha256sum -c -
tar -xzf epc-jurisprudence20.tar.gz
cd epc-jurisprudence20
npm run verify
```

Expected final result:
- archive SHA-256 matches exactly
- npm run verify exits 0
- 29 tests pass
- 0 fail
- 0 skip
