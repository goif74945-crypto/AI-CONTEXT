# Exact Tested Source Bundle

Files part-00.b64 through part-04.b64 concatenate to the exact gzip tar archive tested in the sandbox.

Run:
bash REASSEMBLE.sh

Expected archive SHA-256:
99d61fc903013f1c99d09719fbbcbd62b7a5bda6bff2a208034d3db6a500bac7

The archive contains package.json, tsconfig.json, src/core, all 20 src/engines modules, the NEXY proposal adapter, tests, design/test/evidence documents, and the exact source manifest.
