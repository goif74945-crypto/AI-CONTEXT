# Exact Tested Source Bundle

The base64 parts reconstruct the exact gzip tar archive tested in the standalone sandbox.

Run:
`bash REASSEMBLE.sh`

The script concatenates part-00, part-01, part-02, seven 1,000-byte part-03 fragments, and part-04 in explicit order, verifies the archive SHA-256, then extracts it.

Expected archive SHA-256:
`99d61fc903013f1c99d09719fbbcbd62b7a5bda6bff2a208034d3db6a500bac7`

The archive contains package.json, tsconfig.json, src/core, all 20 src/engines modules, the NEXY proposal adapter, tests, design/test/evidence documents, and the exact source manifest.
