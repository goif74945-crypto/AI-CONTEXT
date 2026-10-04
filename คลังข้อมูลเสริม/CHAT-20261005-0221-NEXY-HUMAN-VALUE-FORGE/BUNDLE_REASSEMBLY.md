# Exact Tested Bundle Reassembly

The `bundle.parts/*.b64` files are consecutive chunks of the exact deterministic tar.gz bundle that passed the recorded local verification.

Reassemble from this directory:

```bash
cat bundle.parts/part-*.b64 | base64 -d > NEXY-HVF-tested-bundle.tar.gz
sha256sum NEXY-HVF-tested-bundle.tar.gz
```

Expected archive SHA-256:

`73f58e03ba96aa543020f85b6e891ae171deca1d34397ee7f8d7accba35c11f5`

Expected archive byte size: `16953`.

After extraction, `evidence/SHA256SUMS.txt` inside the archive binds the 33 tested files (the checksum manifest excludes itself). Publication wrapper files outside the archive are not part of the tested code bundle.
