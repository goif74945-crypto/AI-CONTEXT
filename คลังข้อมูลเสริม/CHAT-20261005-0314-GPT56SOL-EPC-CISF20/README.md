# NEXY EPC Constraint Interaction Spectroscopy Foundry 20 (CISF20)

**Operational CHAT_ID:** `CHAT-20261005-0314-GPT56SOL-EPC-CISF20`  
**Platform-internal ChatGPT chat ID:** `UNKNOWN_NOT_EXPOSED`  
**Authority class:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`

CISF20 is a standalone, deterministic Q64.64 analysis package for detecting proposal failures that appear only when constraints interact. It does **not** vote, promote, mutate NEXY state, rewrite Canon, or replace NEXY::JUDGE.

## Why this exists

A proposal can look acceptable under individual scores or a weighted average while still failing because:

- hard constraints are hidden by compensation from soft metrics;
- two or three deficits co-occur more often than their marginal rates imply;
- aggregate interaction signs reverse inside contexts;
- one scenario or one constraint disproportionately controls the result;
- current behavior is Pareto-dominated by a baseline;
- a small risk core explains most of a scenario's failure;
- insufficient interaction coverage makes the apparent quality fragile.

CISF20 turns those failure modes into explicit, replayable evidence.

## Quick start

```bash
npm test
node tools/cisf20-cli.mjs fixtures/compensation-mirage.json
```

The CLI accepts protocol `NEXY-EPC-CISF20/1`. All Q64.64 values cross the JSON boundary as **signed decimal raw integers**, never binary floating point.

## Integration posture

The package is designed as a pure advisory analyzer. A future NEXY adapter can pass a validated evaluation matrix into `runCisf20()` and attach the returned certificate/evidence to a JUDGE-visible dossier. The analyzer itself has no state-transition or promotion API.

Do not wire it as a replacement for NEXY LAW/CORE/JUDGE, and do not convert any metric here directly into ACCEPT/REJECT/KEEP/CUT without the governing NEXY/EPC authority layer.

## Files

- `src/q64.mjs` — checked signed-i128-domain Q64.64 substrate.
- `src/model.mjs` — strict input validation/canonicalization.
- `src/engine.mjs` — 20 interaction-analysis systems.
- `src/wire.mjs` — deterministic raw-Q64 JSON boundary.
- `tools/cisf20-cli.mjs` — standalone CLI adapter.
- `tests/` — unit, property, adversarial, static-contract, wire and replay tests.
- `03_DESIGN_20_SYSTEMS.md` — architecture and all 20 systems.
- `04_NEXY_INTEGRATION_CONTRACT.md` — exact authority/integration boundary.
- `05_THREAT_MODEL.md` — abuse/failure model.
- `EVIDENCE/` — red/green, test, coverage, CLI and stress evidence.

## Numeric law

- raw domain: signed 128-bit range;
- scale: `2^64`;
- carrier in this standalone Node package: `bigint`;
- authoritative analyzer inputs are constrained to Q64.64 `[0,1]` where specified;
- overflow/division-by-zero/malformed raw values fail closed;
- no wall clock, randomness, network, environment, filesystem iteration or binary floating point influences analyzer decisions.

## Status boundary

Passing this package's tests proves the package behavior at the tested revision only. It does **not** prove NEXY integration, NEXY deployment, or Canon promotion.
