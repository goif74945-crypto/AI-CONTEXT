# 11 — Validation Report

## Status

`PASS` for the **standalone reference prototype evidence classes explicitly tested below**.

This is **not** proof of integration with NEXY.AI, production analytics, production privacy compliance, browser UI, deployment, or real user outcomes.

## Environment

- execution target: local Python runtime available to the current ChatGPT task
- project root: temporary build copy of this supplemental artifact
- external network dependency: none

## Executed verification

### V1 — Syntax/static import compilation

Command:

```bash
python -m compileall -q src tests
```

Result: `PASS`.

### V2 — Unit/integration-within-package tests

Command:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Final result:

```text
Ran 61 tests in 1.245s
OK
```

Covered behaviors include proposal validation, prohibited-risk blocking, equal-allocation boundary, deterministic hashing, statistical planning primitives, proportion/mean evaluation, hash mismatch freeze, data-quality freeze, guardrail freeze, underpowered/inconclusive behavior, CLI compilation, and analytics event/payload validation.

### V3 — Deterministic numeric adversarial sweep

Final result:

```text
ADVERSARIAL_SWEEP_PASS checks=10143 max_roundtrip_error=2.726e-10
```

This swept inverse-normal round trips plus proportion planning/evaluation combinations across multiple baselines, MDE values, and both metric directions.

### V4 — Critical-source nondeterminism/dependency scan

The package source was scanned for common direct network/current-time/random/environment/subprocess dependencies in the critical package namespace.

Final result:

```text
STATIC_FORBIDDEN_SOURCE_SCAN_PASS
```

This is a targeted source scan, not a formal whole-language proof.

### V5 — CLI example

Command:

```bash
PYTHONPATH=src python -m nexy_product_evidence.cli compile examples/proposal.json
```

Observed example planning result:
- planned sample per arm: `2417`
- contract hash: `732bc2dcc023d622753acfb460538a8f61c581067ede09f637c9aca08826168b`

## Defect discovered and repaired during verification

Initial reference code accepted arbitrary `allocation_fraction` while the sample-size equations assumed equal arms. This was a correctness mismatch.

Correction:
- reference v1 now accepts only exactly `0.5` allocation;
- non-50/50 allocation returns `ALLOCATION_UNSUPPORTED`;
- a regression test was added;
- tests were rerun after the correction and finished `61/61 PASS`.

This defect is preserved here because hiding a repaired defect would reduce the value of the evidence record.

## Evidence-class boundary

Verified:
- E1-style syntax/static behavior for this standalone package;
- E2-style unit behavior for the tested reference logic.

Not verified:
- NEXY.AI integration;
- live experiment provider integration;
- production event integrity;
- real causal lift;
- privacy/legal compliance;
- deployment/runtime SLOs;
- sequential testing correctness;
- domain-specific ethics/safety review.
