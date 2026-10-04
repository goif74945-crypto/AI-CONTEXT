# NEXY Integration Contract

## Adapter boundary
`src/nexy-adapter.ts` creates `NexyExternalJudgeEnvelope` only.

Required pins:
- repository;
- branch;
- exact 64-hex commit SHA;
- spec ID;
- exact 64-hex spec SHA-256.

Envelope invariants:
- `requestedAction = REVIEW_ONLY`;
- `advisoryOnly = true`;
- `externalJudgeRequired = true`;
- `canonMutationAllowed = false`;
- `coreStateMutationAllowed = false`;
- `promotionAllowed = false`.

The adapter contains no GitHub client, repository writer, state-transition caller, deployment path, LAW bypass, or Core mutation interface.

## Current compatibility basis
At observed NEXY commit `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`, `packages/intelligence/trinity.ts` identifies the publisher as `EXTERNAL_JUDGE` and forbids implicit/Lo2 current-decision override. The package therefore terminates at a review envelope and intentionally refuses to pretend that an EPC score can become NEXY state.

## Integration mode
Recommended future use is shadow/advisory:
1. NEXY exports a proposal/evidence dossier to an authorized external review boundary.
2. An adapter constructs `CourtCase` + externally authorized `CourtPolicy`.
3. EPC-AJ executes twenty organs deterministically.
4. The review-only envelope returns to the existing external JUDGE path.
5. Existing JUDGE/LAW/Canon promotion logic decides what, if anything, happens next.

This repository contains only steps 2-4 as a standalone reference. Actual NEXY runtime wiring is NOT_VERIFIED and was deliberately not performed.
