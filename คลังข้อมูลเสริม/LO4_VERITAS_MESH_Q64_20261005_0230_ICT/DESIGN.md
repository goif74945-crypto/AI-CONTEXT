# VERITAS MESH — System Design

Status: **PROPOSAL / Lo4 / NON-CANONICAL**

## 1. Purpose

Build a deterministic shadow laboratory that evaluates experimental NEXY capabilities before promotion. It is meant to make pre-canon innovation aggressive without making Canon reckless.

## 2. Non-goals

- no automatic Canon promotion;
- no replacement of DOC-B / DOC-C / source authority;
- no mutation of NEXY.AI;
- no probabilistic inference engine;
- no floating-point scoring;
- no production deployment claim;
- no attempt to replace NEXY core `Fixed128`.

## 3. Architecture

```text
Candidate experiment
      │
      ▼
SignalFrame (24 UnitQ64 signals)
      │
      ├───────────────┐
      ▼               ▼
20 deterministic   Q64.64 numeric law
concept lenses     + invariant guards
      │               │
      └──────┬────────┘
             ▼
       Score vector
             │
             ▼
 Mandatory + critical gates
             │
      ┌──────┼────────────┐
      ▼      ▼            ▼
   REJECT  QUARANTINE  ELIGIBLE_FOR_PROMOTION_REVIEW
                          │
                          ▼
               external authorized process only
               (VERITAS has zero promotion authority)
```

## 4. Numeric law

### Representation

`Q64.raw` is a `bigint` constrained to signed i128 range.

Mathematical value:

`value = raw / 2^64`

### Unit domain

All scoring models use `UnitQ64`:

`0 <= raw <= 2^64`

This bounded domain is intentional. It removes overflow from the actual scoring path even though the generic Q64 helper supports saturating arithmetic for compatibility with NEXY's TypeScript G15 profile.

### Rounding

BigInt division truncates toward zero. No rounding is allowed to improve a candidate's score.

### Serialization

All raw Q64.64 values cross JSON boundaries as base-10 strings, never JSON numbers.

## 5. State and authority

VERITAS is stateless with respect to Canon. A decision contains:

- engine version;
- explicit `NON_CANONICAL_LO4_ONLY` authority label;
- status;
- overall score;
- 20 concept scores;
- failed mandatory gates;
- SHA-256 deterministic receipt;
- `canonicalPromotionPerformed: false`.

The receipt identifies the exact scoring result and input ordering. It is evidence correlation, not authority.

## 6. Failure model

| Failure | Behavior |
|---|---|
| invalid decimal | throw `SyntaxError` |
| raw UnitQ64 outside [0,1] | throw `RangeError` |
| Q64 division by zero | throw `RangeError` |
| invalid weight <= 0 | throw `RangeError` |
| critical safety/repro/canon/requirement gate too low | `REJECT` |
| mandatory gates not all met but critical floor survives | `QUARANTINE` when overall floor survives |
| all mandatory gates + overall threshold pass | `ELIGIBLE_FOR_PROMOTION_REVIEW` only |

## 7. Security/trust boundary

SignalFrame is assumed to be produced by an upstream evidence collector. VERITAS does not decide whether a raw external document is trustworthy. The integration boundary must validate provenance before mapping external facts to scores.

This separation prevents the scorer from accidentally becoming a trust escalator.

## 8. Determinism model

For identical raw signal strings and engine version, concept scores, overall status, failed gates, portable JSON, and receipt hash are deterministic.

Time, random numbers, filesystem state, network state, locale, and environment variables are not part of scoring.

## 9. Version evolution

Any formula, threshold, signal, rounding, or receipt payload change requires an engine version bump. Evidence from another version cannot silently satisfy the new version.

## 10. Promotion law

VERITAS can recommend review. It cannot mutate Canon, repository authority, policy, or release state. Promotion requires an external authorized process and its own evidence.
