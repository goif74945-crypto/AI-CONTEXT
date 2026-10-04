# NEXY Minimal Blocker Core / Freeze Explanation Engine

**Status:** `EXPERIMENTAL / AI-PROPOSED CONCEPT / ADVISORY ONLY`  
**Session code:** `NEXY-MBC-20261005-0121-ICT`  
**Platform chat ID:** `UNKNOWN` because the available chat/tool surface does not expose a trustworthy platform conversation identifier.

## Why this exists

NEXY's stable project direction is verify-or-freeze: one legal verified output, otherwise an explicit block/freeze state. A freeze that only says “not ready” is operationally weak. Operators and future agents need to know:

- which exact obligations are unsatisfied;
- which declared PASS claims are stale or supported by the wrong evidence class;
- whether alternative proof paths exist;
- the inclusion-minimal sets of obligations that must be repaired to make the gate pass;
- which minimal set is cheapest under an explicitly declared, non-authoritative repair-cost heuristic;
- whether the explanation can be reproduced byte-for-byte for the same semantic input.

This project implements that capability as a standalone Python tool inside `AI-CONTEXT`. It does **not** modify or claim to be integrated into the NEXY.AI implementation repository.

## Core behavior

Input is a monotone gate expression over evidence leaves:

- `leaf`: one named evidence obligation;
- `all_of`: every child must pass;
- `any_of`: at least one child must pass;
- `at_least(k, of)`: threshold gate.

Each evidence leaf carries a project status and may carry:

- required/observed evidence class `E0` through `E7`;
- target and observed revision;
- repair kind;
- declared repair cost;
- remediation text.

A leaf declared `PASS` is deterministically downgraded to `NOT_VERIFIED` when its evidence class is below the required class, its required revision is missing, or its observed revision is stale/wrong.

The engine then emits:

1. `ALLOW` only when the root gate is `PASS`; otherwise `FREEZE`;
2. a structured explanation tree;
3. unsatisfied evidence with downgrade reasons;
4. inclusion-minimal repair sets;
5. a primary blocker core / recommended repair set;
6. truncation/optimality disclosure;
7. a SHA-256 certificate over canonical JSON.

## Determinism boundary

The certificate hash is computed from canonical JSON with sorted keys and no wall-clock input. The hash covers the certificate body **excluding** `certificate_sha256` itself.

Determinism here means: identical semantic JSON input plus engine version and repair-set limit produce the same output/certificate. It does **not** prove that upstream evidence is truthful.

## Run

```bash
python3 src/blocker_core.py \
  --input fixtures/release_gate_example.json \
  --output fixtures/release_gate_actual.json \
  --pretty
```

Exit codes:

- `0`: root gate PASS / ALLOW;
- `2`: valid evaluation but root gate does not pass / FREEZE;
- `64`: malformed/invalid input or I/O failure.

Run the full validation pack:

```bash
python3 scripts/run_validation.py
```

## Verified in this execution slice

Local sandbox verification produced:

- Python syntax/import execution: PASS;
- 14/14 unit tests: PASS;
- deterministic seeded structural regression: 50 iterations inside the unit suite: PASS;
- nested repair-set result checked against a brute-force oracle: PASS;
- current revision-locked example fixture: valid `FREEZE` result;
- generated fixture certificate SHA-256: `fbd001162936086eb9e53a52df7218cd99ee657d3e78d19c950bd7ddce23153c`.

These are E1/E2-style proofs for this standalone tool in the local execution sandbox. They are **not** NEXY.AI integration, runtime, deployment, or release evidence.

## Non-goals

- No NEXY.AI code mutation.
- No automatic release authorization.
- No conversion of advisory repair cost into project authority.
- No negative boolean operator. The repair-set algorithm assumes monotone gates.
- No claim that a mathematically minimal repair set is feasible in the real system.
- No claim that every NEXY requirement has already been modeled as a leaf.

## Adoption boundary

Promotion into canonical NEXY build/runtime scope requires an explicit authority decision, schema/version review, integration design, exact-head tests, abuse tests, operational evidence, and rollback semantics. Until then this folder remains experimental supplemental knowledge/tooling.
