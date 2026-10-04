# Verification Evidence Report

## Environment
- date context: 2026-10-05 Asia/Bangkok
- Node: v22.16.0
- npm: 10.9.2
- TypeScript compiler available in sandbox: 5.8.3
- Rust: unavailable in sandbox

## Claim 1: source is strict-type-checkable standalone
- evidence class: E1 Static
- command: `tsc -p tsconfig.json --pretty false`
- observed: exit 0, no diagnostics after fixes
- status: PASS
- limitation: local compiler is TS 5.8.3; NEXY package currently declares TypeScript ^6.0.3, so exact TS6 compatibility is not independently executed here.

## Claim 2: implemented behavior passes unit/stress tests
- evidence class: E2 Unit
- command: `npm test`
- observed: 17 tests, 17 pass, 0 fail
- status: PASS
- artifact: `test-output.txt`

## Claim 3: all 20 concept scores remain bounded
- evidence class: E2 Unit/property-style stress
- test: 2000 deterministic pseudo-random frames; each evaluates 20 concepts
- observed: no score below zero or above Q64.64 one
- status: PASS

## Claim 4: unsafe promotion fails closed
- evidence class: E2 Unit
- observed: candidate with zero safety is `REJECT`
- status: PASS

## Claim 5: Lo4 cannot self-promote Canon
- evidence class: E1 + E2
- implementation: only statuses are REJECT/QUARANTINE/ELIGIBLE_FOR_PROMOTION_REVIEW; `canonicalPromotionPerformed` literal false
- executed test verifies strong candidate remains review-eligible, not promoted
- status: PASS

## Claim 6: deterministic receipt
- evidence class: E2
- same input evaluated twice produced same SHA-256 receipt
- final healthy-frame receipt: `4fa8904e73a0dbf0f33a0f94506474b0a7f0fb4d2f4a07abdd57cd0d12f7f18f`
- status: PASS

## Claim 7: local throughput observation
- evidence class: local runtime observation, not deployment evidence
- command: `npm run bench`
- runs: 10,000
- final observed elapsed: 276.903 ms
- final observed rate: 36,113.74 decisions/s
- status: PASS for this one local observation only
- limitation: not a stable performance SLA; host load and runtime differ.

## Regression sequence
- initial run: FAIL (2 tests)
- fix + rerun: FAIL (1 test)
- second fix + strict typecheck repair + rerun: PASS 17/17

This failure history is retained because deleting it would make the evidence prettier and less useful.
