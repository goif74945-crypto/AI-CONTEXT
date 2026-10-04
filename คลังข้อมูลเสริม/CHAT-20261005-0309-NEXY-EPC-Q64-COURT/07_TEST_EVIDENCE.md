# Executed Verification Evidence

Environment observed:
- Node.js `v22.16.0`
- TypeScript compiler `5.8.3`
- Python `3.13.5` used only for local file-generation/patch scripting, not EPC runtime.

## Static/type proof
`tsc -p tsconfig.json` -> PASS under strict settings.

Static runtime-surface audit found no imports/calls for filesystem, network, child process, environment variables, `Math.random`, `Date.now`, or `fetch` in `src/`. The only Node core dependency is `node:crypto` for deterministic SHA-256 canonical hashing.

Decimal-literal grep against `q64.ts` and `scoring.ts` produced only text `v0.1` inside a policy identifier, not floating-point arithmetic.

## Runtime tests
Final local execution after three hardening loops:
- tests: **33**
- pass: **33**
- fail: **0**
- cancelled: 0
- skipped: 0

Covered behavior:
- exact Q64.64 binary-fraction arithmetic;
- 1,000 deterministic rational-product property cases;
- Q64 overflow and divide-by-zero freeze;
- one KEEP and one CUT lifetime entitlement per CHAT_ID;
- independent KEEP/CUT rights;
- WIP/DEFER non-vote preservation;
- direct factual evidence binding for every CUT basis;
- UNKNOWN cannot substitute for adverse factual proof;
- semantic duplicate proof rejects name-only similarity;
- KEEP_MERGE and CUT_SUPERSEDED require exact semantic targets;
- stale NEXY/AI-CONTEXT snapshot freeze;
- unresolved Canon conflict cannot be overridden by KEEP;
- assumption evidence-class discipline;
- dependency closure for promotion preparation;
- append-only hash-chain tamper detection;
- sealed-head tail-truncation detection;
- immutable evidence revisions;
- non-authoritative promotion packet;
- JUDGE-bound advisory integration output;
- exact count of 20 distinct implemented concepts.

The full raw files `evidence/test-run.txt`, `evidence/static-audit.txt`, and `evidence/FILE-MANIFEST.sha256` are contained in the source archive bundle.

## Failure/recovery history
Initial strict compile exposed a narrowing defect in revision handling; it was repaired before the suite passed.

A self-audit then identified two missing proof properties: tail truncation needed a sealed expected head+length, and CUT basis needed direct factual evidence linkage. Both were implemented and retested.

A third hardening pass added semantic merge/supersede target requirements, independent entitlement tests, Q64 failure edges, scoring policy validation, and promotion rejection. Final result: 33/33 PASS.
