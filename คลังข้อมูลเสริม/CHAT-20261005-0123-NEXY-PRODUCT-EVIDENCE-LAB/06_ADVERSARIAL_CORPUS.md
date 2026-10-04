# 06 — Adversarial Scenario Corpus

These cases define expected reference behavior and are covered by executed tests where noted.

| Case | Input condition | Required result |
|---|---|---|
| A01 | experiment ID malformed | compile failure |
| A02 | title/hypothesis/population empty | compile failure |
| A03 | no guardrail | compile failure |
| A04 | `dark_pattern` risk flag | compile failure |
| A05 | `privacy_violation` risk flag | compile failure |
| A06 | non-50/50 allocation | compile failure in v1 |
| A07 | proportion baseline outside (0,1) | compile failure |
| A08 | baseline +/- MDE outside (0,1) | compile failure |
| A09 | mean metric missing planning stddev | compile failure |
| A10 | duplicate guardrail names | compile failure |
| A11 | evidence hash differs from exact contract hash | `FREEZE` |
| A12 | data-quality flag false | `FREEZE` |
| A13 | invariant violation present | `FREEZE` |
| A14 | required guardrail missing | `FREEZE` |
| A15 | hard guardrail degradation above threshold | `FREEZE` |
| A16 | sample size below planned per-arm minimum | `INCONCLUSIVE` |
| A17 | confidence interval overlaps MDE | `INCONCLUSIVE` |
| A18 | confidence interval wholly below MDE threshold | `REJECTED` |
| A19 | confidence interval clears MDE threshold | `SUPPORTED` |
| A20 | proportion observation outside [0,1] | `FREEZE` |
| A21 | mean observation missing stddev | `FREEZE` |
| A22 | analytics payload includes `token` | instrumentation validation failure |
| A23 | analytics payload misses required property | instrumentation validation failure |
| A24 | analytics payload contains unexpected property | instrumentation validation failure |

## Numeric adversarial sweep

A separate executed sweep tested:
- inverse-normal round-trip over 9,999 probabilities;
- proportion planning over baseline/MDE/direction combinations;
- observed interval ordering and p-value bounds.

Recorded result in the final local verification run:

`ADVERSARIAL_SWEEP_PASS checks=10149 max_roundtrip_error=2.726e-10`
