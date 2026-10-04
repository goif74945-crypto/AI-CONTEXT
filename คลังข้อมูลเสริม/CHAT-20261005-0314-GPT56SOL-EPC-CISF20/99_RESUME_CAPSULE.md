# Resume Capsule — CISF20

## Identity

- Operational ID: `CHAT-20261005-0314-GPT56SOL-EPC-CISF20`
- Platform internal chat ID: unavailable to the model.
- Writable target: only this mission namespace in AI-CONTEXT, plus shared VOTES protocol bootstrap if absent.
- Protected target: every repository with `NEXY.AI` in its name.

## What exists

A pure Node ESM package implementing 20 Q64.64 constraint-interaction analyzers, strict validation, deterministic certificate hashing, raw-Q64 JSON wire protocol, CLI, fixtures, tests and evidence.

## Commands

```bash
npm test
npm run test:coverage
node tools/cisf20-cli.mjs fixtures/compensation-mirage.json
```

## Expected invariants

- tests all pass;
- exactly 20 unique system IDs;
- reordered semantic input → identical certificate;
- no production-core clock/random/network/env/fs dependency;
- no state-transition or promotion API;
- `canMutateNexyState=false` and `canPromote=false`.

## Vote state

KEEP and CUT are unused. `VOTE_STATUS.md` is DEFER and consumes no round.

## Next legal work

1. Re-read latest NEXY + AI-CONTEXT heads.
2. If integrating, create an adapter outside NEXY first, then verify contracts; do not mutate NEXY without explicit user authorization.
3. If voting, obtain direct source/spec evidence sufficient under the user law and inspect the shared VOTES ledger for entitlement conflicts.
4. Do not edit historical vote receipts; add revision/evidence appendices only.
