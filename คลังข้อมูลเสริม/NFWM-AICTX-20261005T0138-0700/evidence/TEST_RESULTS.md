# NFWM Executed Test Results

## Environment

- execution sandbox: local container
- language: Python 3.11-compatible source
- network required by NFWM tests: no
- runtime third-party dependencies: none

## E1 — Static bytecode compilation

Command:

```bash
python -m compileall -q src tests
```

Observed result: `PASS` (exit 0, no compile errors).

Evidence class: E1 static.

## E2 — Unit + CLI behavior suite

Command:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Observed result:

```text
Ran 17 tests in 3.182s
OK
```

Covered behavior includes:

- valid trace PASS;
- illegal FSM transition detection;
- missing FREEZE incident link detection;
- release-after-freeze detection;
- duplicate idempotency detection;
- non-increasing sequence detection;
- STOP terminal rule;
- deterministic witness hash;
- 2-event witness reduction for two-event causal rules;
- strict unknown-field rejection;
- canonical hash key-order independence;
- CLI PASS/failure exit behavior;
- witness round-trip verification;
- tampered witness hash rejection.

Evidence class: E2 unit/isolated behavior.

## E2 — Sample failure minimization

Input: `tests/fixtures/release_after_freeze.json`

Observed:

- source event count: `7`
- selected violation: `INV_RELEASE_AFTER_FREEZE`
- witness event count: `2`
- witness event seqs: `4, 6`
- witness hash: `6b31dac7cea7806e02603c131c35bcc5e7de02957dd4ed5bf6fc4a4da9cd3a10`

CLI exits `2`, intentionally meaning a valid trace was analyzed and a violation was found.

## E2 — Witness replay

Command:

```bash
PYTHONPATH=src python -m nfwm.cli verify-witness \
  evidence/sample-witness.json \
  --profile profiles/nexy-vnext-trace-profile.json
```

Observed:

```json
{"hash_ok":true,"one_minimal":true,"same_event_count_after_reminimize":true,"schema_version":"nfwm.witness-verification.v1","status":"PASS","violation_code":"INV_RELEASE_AFTER_FREEZE","witness_hash":"6b31dac7cea7806e02603c131c35bcc5e7de02957dd4ed5bf6fc4a4da9cd3a10"}
```

## Negative-path proof

A test replaces the stored witness hash with 64 zeroes. Replay returns exit `3`, `status=FAIL`, and `hash_ok=false`.

## Not proven

- NEXY.AI integration: NOT_VERIFIED.
- NEXY production logs/schema compatibility: NOT_VERIFIED.
- deployment behavior: NOT_VERIFIED.
- global-minimum witness cardinality: not claimed.

## Final regression after remote-state synchronization

After remote byte-identity readback passed and only documentation/evidence state was synchronized locally, the full suite was executed again:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Observed:

```text
Ran 17 tests in 3.315s
OK
```

Artifact: `evidence/unittest-final-after-remote.txt`.

This second run confirms the executable source/test state still passes after the publication-verification phase. No NEXY.AI runtime was involved.
