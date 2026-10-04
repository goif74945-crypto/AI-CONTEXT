# NEXY EPC Adversarial Jurisprudence Q64-20

**Work code:** `CHAT-20261005-0310-NEXY-EPC-ADVERSARIAL-JURISPRUDENCE-Q64-20`  
**Class:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`  
**Target integration:** NEXY `EXTERNAL_JUDGE` review boundary only.  
**Protected target:** `goif74945-crypto/NEXY.AI-` remains read-only.

This standalone TypeScript reference package adds an adversarial procedural layer to the proposed **NEXY Evolutionary Proposal Court (EPC)**. It does not generate proposals, own KEEP/CUT vote entitlements, promote candidates, mutate Canon, mutate Core state, or replace JUDGE/LAW.

The package implements 20 distinct court organs using deterministic signed Q64.64 (`bigint`) metrics where quantitative policy is required. It treats policy thresholds as externally supplied authority. Decision output is advisory and can only be wrapped as a `REVIEW_ONLY` envelope for an external JUDGE.

## Verified local commands

```bash
npm run verify
node scripts/replay-proof.mjs
node examples/integration_example.mjs
npm pack --dry-run
```

Current local evidence: 40/40 tests pass in normal mode and 40/40 pass again in production-mode execution; 1,000 canonical replay checks produce one stable proof; no float/random/wall-clock token is admitted in authoritative `src/` by the static gate.

## Important status boundary

`LOCAL_REFERENCE_IMPLEMENTATION = PASS`  
`NEXY_RUNTIME_INTEGRATION = NOT_VERIFIED`  
`CANON_PROMOTION = NOT_AUTHORIZED`  
`KEEP_ROUND_USED = NO`  
`CUT_ROUND_USED = NO`

No KEEP/CUT round is consumed by this work package because the exact authoritative DOCX bytes were not directly readable in this session, even though the current NEXY repository binds the named design source to SHA-256 `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7` and its current code/source snapshots corroborate the relevant authority constraints.
