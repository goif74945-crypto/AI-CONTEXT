# Architecture — Q64 Constitutional Physics

**Authority:** Lo4 AI proposal only. This document proposes mechanisms; it does not override NEXY law/specification.

## Architecture map

```text
normalized plan/evidence state
        |
        +--> UMC: uncertainty conservation ----------+
        |                                            |
        +--> DRC: perturbation robustness -----------+--> conservative pipeline --> PASS or FREEZE
        |                                            |
        +--> VBR: non-fungible budget reservation ---+
        |                                            |
        +--> RHL: rollback-quality time window -------+
        |                                            |
        +--> EDB: preview/consequence fidelity -------+

Shared substrate: checked signed Q64.64 (`qcp.fixed.Q64`)
```

No engine grants execution authority. A PASS is only an advisory quantitative precondition; a higher NEXY authority layer may still deny/freeze.

## Global invariants
1. Quantitative executable state is Q64.64; float input is rejected.
2. Overflow and invalid domains stop evaluation rather than saturating silently.
3. A positive result from one engine cannot erase a FREEZE from another engine in the composition demo.
4. Inputs carry explicit identities; duplicate identities fail or freeze where ambiguity would change meaning.
5. Each engine exposes compact reason codes suitable for deterministic audit records.
6. No engine owns User Law, final JUDGE authority, provider credentials, external side effects, or Canon promotion.

## State and concurrency
The reference engines are pure or return replacement state objects. VBR is modeled as immutable-state transitions at the API level. A production adapter would require atomic compare-and-swap/transaction semantics around reservations; this isolated package does not claim distributed concurrency correctness.

## Failure model
- malformed typed state -> exception at construction/API boundary;
- insufficient proof/ambiguous quantitative state -> `FREEZE`;
- robust negative decision in DRC -> `CERTIFY_DENY`, not a system error;
- exact safe advisory result -> PASS/certificate;
- overflow/domain failure -> exception, to be translated by a future adapter into the authoritative NEXY freeze contract.

## Complexity summary
- UMC: O(n) stages, O(n) receipt validation already materialized in input.
- DRC: O(n log n) due canonical feature ordering; O(n) arithmetic.
- VBR: O(r*d) to aggregate current reservations, where r is reservation count and d dimensions per reservation. A production indexed accumulator can reduce reservation checks to O(d).
- RHL: O(log deadline * log exponent) Q64 multiplications due binary search plus exponentiation-by-squaring. A production cache could reduce repeated powers.
- EDB: O(n log n) dominated by deterministic ID ordering.

## Evolution law
Any future change to Q64 rounding, dimensional meaning, conservation tolerance, threshold inclusivity, budget state transitions, reversibility decay, or expectation weighting is a contract change. Such changes require versioned adapters and fresh evidence; old PASS artifacts must not be silently reused.
