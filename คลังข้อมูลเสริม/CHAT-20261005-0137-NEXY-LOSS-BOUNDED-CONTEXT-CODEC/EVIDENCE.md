# LBCC Verification Evidence

## Scope

Evidence applies only to the standalone LBCC implementation in this folder. It does **not** prove integration, deployment, or runtime behavior inside NEXY.AI.

## Environment

- execution environment: isolated ChatGPT container;
- language: Python 3.11+ target;
- network required by tests: no;
- third-party runtime dependencies: none;
- test framework: Python `unittest`.

## E1 — Static compilation

Command:

```bash
PYTHONPATH=src python -m compileall -q src tests tools
```

Observed: `PASS`, exit code 0. Raw record: `evidence/compileall.txt`.

## E2 — Unit / negative / randomized invariants

Command:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Observed: **29 tests PASS**.

Coverage by behavior includes:
- deterministic byte-identical result;
- full-fit zero-loss;
- immutable/protected budget freeze;
- UNKNOWN protection;
- CONFLICT protection;
- authority-threshold protection;
- loss-budget freeze;
- exact capsule byte ceiling;
- provenance/evidence preservation;
- valid source verification;
- retained-atom tamper detection;
- loss-ledger tamper detection;
- metrics tamper detection;
- rehydration roundtrip;
- bad rehydration store rejection;
- duplicate ID rejection;
- invalid authority rejection;
- empty text rejection;
- metadata deep-freeze against caller mutation;
- non-string metadata key rejection;
- floating metadata rejection to preserve cross-language canonicality;
- secret patterns in payload and metadata;
- explicit sensitive-policy override;
- CLI freeze exit behavior;
- strict unknown-field rejection;
- randomized 40-seed determinism/budget/verification invariant suite;
- 200-atom protected-retention stress case.

Raw record: `evidence/unittest.txt`.

## E3 — CLI compact → verify integration

Compact command:

```bash
PYTHONPATH=src python -m lbcc.cli compact tests/fixtures/sample_bundle.json \
  --max-bytes 900 --max-loss-ppm 200000 > examples/sample_result.json
```

Observed PASS capsule:
- source atoms: 3;
- retained atoms: 2;
- dropped atoms: 1;
- capsule bytes: 861;
- loss: 179246 ppm;
- policy ceiling: 900 bytes / 200000 ppm.

Verify command:

```bash
PYTHONPATH=src python -m lbcc.cli verify tests/fixtures/sample_bundle.json \
  examples/sample_result.json --max-bytes 900 --max-loss-ppm 200000
```

Observed: `{"failures":[],"passed":true}`.
Raw record: `evidence/cli_verify.json`.

## Performance evidence

Synthetic deterministic benchmark, no network, no I/O inside timed `compact()` call. Values are environment-specific and are **not** a production SLA.

Final benchmark run recorded in `evidence/benchmark.jsonl`:
- 250 atoms / 25,000-byte budget: median around tens of milliseconds;
- 1,000 atoms / 100,000-byte budget: median under 0.1 s in this container;
- 5,000 atoms / 500,000-byte budget: median under 0.5 s in this container.

### Performance defect and repair evidence

Earlier implementation rebuilt a full ledger and reserialized the whole capsule for every candidate. Observed:
- 250 atoms median ~1.24 s;
- 1,000 atoms exceeded a 45 s tool window.

Root cause: near-quadratic repeated whole-state work.

Repair:
- precompute atom importance and canonical byte length;
- exact capsule-size accounting from scalar skeleton + retained atom lengths;
- exact `Fraction` density ranking;
- build SHA-256 dropped ledger once after selection.

After repair, the same benchmark family completed in sub-second ranges through 5,000 atoms in this environment. This is evidence of the local implementation improvement, not a universal performance guarantee.

## Evidence class limits

PASS:
- E1 static compilation;
- E2 unit/negative/randomized behavior;
- E3 local CLI component integration.

NOT_VERIFIED:
- NEXY.AI repository integration;
- NEXY.AI runtime behavior;
- production load/SLA;
- deployment;
- multi-process/distributed integration;
- cross-language canonicalization implementation parity;
- cryptographic signature/authenticity (SHA-256 here is integrity commitment only).
