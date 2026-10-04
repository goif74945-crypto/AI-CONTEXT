# NEXY EPC SCARM-20

**SCARM-20** is a Lo4 experimental, non-governing reference package for the proposed **NEXY Evolutionary Proposal Court (EPC)**. It supplies 20 deterministic mechanisms for detecting strategic manipulation across candidate/vote/revision flows.

It is deliberately unable to promote proposals, alter Canon, mutate Core/JUDGE state, or cast KEEP/CUT votes.

## Build and test

```bash
npm run build
npm test
```

Toolchain used for the recorded evidence: Node.js 22.16.0 and TypeScript 5.8.3.

## Structure
- `src/q64.ts` — checked signed i128-domain Q64.64 helpers.
- `src/canonical.ts` — locale-independent canonical ordering/set helpers.
- `src/model.ts` — input/output contracts.
- `src/scarm.ts` — all 20 mechanisms.
- `tests/` — unit, negative, exhaustive permutation/property, and integration tests.
- `scripts/determinism-replay.mjs` — cross-process deterministic replay artifact.
- `evidence/` — exact logs, replay output, environment/static scan, and SHA-256 manifest.

## Authority boundary
The package returns only review findings and `ALLOW_REVIEW / DEFER_REVIEW / BLOCK_REVIEW`. A future adapter must route these as evidence to the existing NEXY authority path. It must not turn SCARM into a state-transition owner.
