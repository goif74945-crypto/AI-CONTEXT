# Verification Plan

## Evidence classes targeted
- **E0 presence**: files and committed blobs exist.
- **E1 static**: Python `compileall` succeeds; manifest structure and local file identities are generated.
- **E2 unit/adversarial**: all gate behaviors and negative paths execute under `unittest`; current run is 59/59 PASS.
- **E3-reference integration**: a local test crosses epoch, intent, inputs, completion and cache boundaries. This proves only the standalone reference composition, not NEXY integration.
- **Determinism probe**: representative fingerprints are compared under multiple `PYTHONHASHSEED` processes.

## Critical negative paths
- stale/superseded epoch;
- cancelled epoch;
- changed action after lease preparation;
- replayed lease;
- foreign/tampered cache entry;
- policy/model/tool contract drift;
- modality target/permission divergence;
- duplicate/missing modality;
- missing/ambiguous/wrong-kind/wrong-trust/wrong-digest input;
- unreferenced input quarantine;
- missing final marker;
- duplicate/gapped sequence;
- mixed run or contract;
- illegal final marker position;
- final payload digest mismatch;
- expected chunk count mismatch.

## Verification command
```bash
python3 scripts/verify.py
```

## Local coverage evidence
Coverage.py 7.13.3 branch-aware report currently measures **97%** across the source package. This is a test-surface metric, not proof of production completeness.

## Explicit limitations
- `ruff` and `mypy` are not installed in the current execution environment, so no lint/mypy result may be claimed.
- no real NEXY adapter, database, Redis, provider API, browser, distributed worker or deployment runtime is exercised;
- no load, crash-recovery or concurrent mutation proof exists;
- SHA-256/Git blob matching establishes byte identity, not semantic adoption or production fitness.
