# Verification Evidence — EPC Constitutional SAT 20

## Environment
- Node.js: 22.16.0
- TypeScript: 5.8.3
- authoritative project math: checked BigInt Q64.64 under signed-i128 raw bounds

## Executed verification
`npm run verify` completed successfully on the sealed project.

Results:
- TypeScript strict compile: PASS
- executable tests: **28 passed / 0 failed / 0 skipped**
- static audit: **PASS — 23 scanned code/config files, 0 forbidden hits**
- deterministic SAT corpus cross-check: **180/180 formulas** agreed with independent brute-force truth tables
- deterministic implication cross-check: **576/576 pairs** agreed with independent brute-force semantics
- exact bounded minimal UNSAT-core test: PASS
- Q64.64 boundary / overflow / divide-by-zero tests: PASS
- malformed input and unknown evidence fail-closed tests: PASS
- canonical/permutation replay equality: PASS

## CLI replay digests
Safe fixture, two independent runs:
`9178c7c029a89e8d62d282abb4d6ea354e5c6a9ebbef6376335ce16416365763`
Exit code: `0`

Conflict fixture, two independent runs:
`e9b2949531cd288af4e805b31ce1d8e56656879da513b11d48e061abd0ce40e6`
Exit code: `3`

## Artifact seal
Exact deterministic `.tar.xz` archive SHA-256:
`33fc410780ebfb819130453f0995c8e45c692c18fb321662745b9371ef47c90f`

The archive contains Design + source + compiled ESM + declarations + fixtures + unit/property tests + raw verification logs + MANIFEST.sha256 + final audit.

## Evidence ceiling
FACT:
- standalone code executed successfully under the environment above.
- the tested bytes are hash-sealed.
- source evidence pins were read before design.
- no NEXY.AI write was required or performed for standalone verification.

UNKNOWN / NOT PROVEN:
- production performance at NEXY-scale constraint counts.
- runtime integration compatibility beyond the inspected contracts.
- deployment behavior.
- Canon promotion eligibility.
- formal proof of semantic uniqueness against every historical proposal.

Therefore status remains:
`VERIFIED_STANDALONE / NON_CANONICAL / NOT_RUNTIME_INTEGRATED`.
