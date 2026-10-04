# NEXY Freeze Bridge Lab — Current v1.1

> **AI-PROPOSED CONCEPT / REFERENCE IMPLEMENTATION / ADVISORY ONLY**
>
> This namespace does not claim current NEXY implementation. It exists in AI-CONTEXT only.

## Session

- Session code: `NEXY-FREEZE-BRIDGE-20261005-0121-ICT`
- Namespace: `CHAT-20261005-0121-NEXY-FREEZE-BRIDGE-LAB`
- Actual ChatGPT platform conversation ID: **UNKNOWN / not exposed by available tools**
- NEXY.AI implementation-repository writes by this session: **0**

## Current purpose

Freeze Bridge v1.1 is an **upstream freeze-semantics normalizer**.

```text
authoritative freeze metadata
        ↓
NEXY Freeze Bridge v1.1
  - reason normalization
  - unknown-reason fail-safe
  - disclosure-safe evidence refs
  - required-input identifiers
  - recovery-intent intersection
  - dependency-recheck safety clamp
  - Thai/English explanation text
  - deterministic fingerprint
        ↓
FreezeExplanation
        ↓
downstream Trust UX / presentation authority
```

It deliberately does **not** receive a user role, choose display modes, create UI buttons, expose a Recover affordance, authorize an operation, or mutate Core state.

## Why v1.1 exists

The initial v1.0 design included human recovery-card/action concepts. During execution, a concurrent sibling project appeared:

`คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-TRUST-UX-CONTRACT-LAB`

That sibling already owns the presentation problem: backend envelope + role → Trust Card/display/action visibility.

To satisfy the user's no-duplication requirement, Freeze Bridge was pivoted upstream. Files `01_...` through `09_...` are retained as **HISTORICAL / SUPERSEDED v1.0** provenance.

## Current machine contract

Input: `schema/freeze-event.schema.json`  
Output: `schema/freeze-explanation.schema.json`

Protocol: `1.1`  
Policy: `freeze-bridge-policy/1.1`

Key invariant:

`eligible_recovery_intents = upstream_authorized_intents ∩ reason_policy_intents`

The output always carries:

`downstream_ui_authority_required = true`

## Current code

- `freeze_bridge/model.py`
- `freeze_bridge/policy.py`
- `freeze_bridge/compiler.py`
- `freeze_bridge/cli.py`
- `tests/test_freeze_bridge.py`
- `tools/policy_selfcheck.py`
- `tools/benchmark.py`

Runtime dependencies: Python standard library only.

## Verified local evidence for v1.1

- 23/23 unit + negative-path tests PASS.
- Production library line + branch coverage: 100%.
- Policy matrix self-check: 330/330 PASS.
- `compileall`: PASS.
- JSON Schema Draft 2020-12 self-check: PASS.
- Three input→output schema round-trips: PASS.
- Thai CLI JSON round-trip: PASS.
- Local microbenchmark: 50,000 compiles in 1.516704s, about 32,966.23 ops/s in that sandbox only.

The benchmark is not a production SLA. E3–E6 integration/runtime/deployment claims remain NOT_VERIFIED.

## Current documents

- `00_EXECUTION_STATE.md` — durable execution state.
- `10_V1_1_PIVOT_AND_SIBLING_BOUNDARY.md` — non-overlap law.
- `11_PROTOCOL_V1_1.md` — current protocol/policy contract.
- `12_VERIFICATION_V1_1.md` — executed evidence.
- `13_FINAL_AUDIT.md` — final repository/write-back audit.

## Non-goals

Freeze Bridge does not:
- override DOC-B/C/D/E;
- decide release/deployment;
- infer missing intent;
- guess a causal reason;
- grant authorization;
- decide role visibility;
- decide display mode;
- execute a recovery operation;
- mutate any NEXY.AI repository.

Promotion into current NEXY build scope requires a separately authorized task and matching current-head evidence.


## Localization sibling boundary

A second concurrent sibling was discovered:

`คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-SEMANTIC-LOCALIZATION-INTEGRITY-LAB`

Freeze Bridge may select fixed English/Thai reference wording, but it does **not** claim translation correctness or semantic-equivalence verification. Its locale test proves only that machine fields/intents do not change when locale changes. Cross-language drift detection belongs to the Localization Integrity sibling.
