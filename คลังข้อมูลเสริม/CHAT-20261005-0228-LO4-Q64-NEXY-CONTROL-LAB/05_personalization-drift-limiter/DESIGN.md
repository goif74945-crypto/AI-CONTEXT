# 05 — Personalization Drift Limiter

**Lo4 status:** AI-proposed innovation only. NOT Canon. Formal promotion is required before any governing authority.

## Objective
Bounds preference updates so personalization evolves without abrupt profile drift.

## NEXY integration boundary
- Pure deterministic TypeScript module; no network, storage, secret, or NEXY repository mutation.
- Consumes normalized Q64.64 inputs and returns deterministic outputs.
- Adapter code in NEXY would be a separate future integration task.

## Invariants
1. All decision math uses signed Q64.64 backed by checked BigInt.
2. No IEEE-754 float participates in decision arithmetic.
3. Invalid domains fail explicitly.
4. Stable tie-break uses lexical ID when ranking.
5. This module cannot promote itself into Canon.

## Failure model
- Overflow => RangeError.
- Invalid domain/empty eligible set => explicit error where applicable.
- No hidden saturation or fallback.

## Evidence target
E1 TypeScript static check + E2 executed unit test. Higher classes require NEXY integration/runtime and are intentionally NOT claimed.
