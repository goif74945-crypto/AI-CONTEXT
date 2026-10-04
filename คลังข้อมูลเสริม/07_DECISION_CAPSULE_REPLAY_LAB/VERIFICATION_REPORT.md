# Verification Report

Target: standalone reference implementation under AI-CONTEXT supplemental lab.  
Status: **PASS** for prototype acceptance criteria listed below.  
NEXY.AI implementation status: **NOT_VERIFIED / NOT MODIFIED**.

## Evidence executed

Runtime dependency:
- Python standard library only for the prototype.
- No third-party runtime package is required by the implementation.

Commands rerun in the execution container:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m nexy_dcr.cli compile examples/pass-plan.json examples/pass-capsule.json
PYTHONPATH=src python -m nexy_dcr.cli verify examples/pass-capsule.json
PYTHONPATH=src python -m nexy_dcr.cli replay examples/pass-capsule.json
PYTHONPATH=src python -m nexy_dcr.cli receipt examples/pass-capsule.json
PYTHONPATH=src python -m nexy_dcr.cli compile examples/freeze-plan.json examples/freeze-capsule.json
PYTHONPATH=src python -m nexy_dcr.cli replay examples/freeze-capsule.json
PYTHONPATH=src python benchmarks/benchmark.py --count 10000
```

Latest observed rerun:
- **30 tests executed, 30 passed**;
- `compileall` passed;
- PASS example compile / verify / replay / receipt passed;
- FREEZE example compile / replay passed;
- PASS capsule ID: `e633317c88b7f23a79520efd1ea5ff3cb4bf18d9a52e9a3b294b5b99516c7eff`;
- FREEZE capsule ID: `bb663b764a7482b9ee8b959973439096298f72411b8ad5b03d8c9bb60d3359e0`;
- benchmark at 10,000 capsules x 6 events: about **7,343 builds/s** and **9,805 replays/s** on the latest observed run.

An earlier run in the same work session observed about 10,031 builds/s and 12,201 replays/s. The variance is retained as evidence that this microbenchmark is environment-sensitive. **No production throughput guarantee is claimed.**

## Blob identity proof

All Python source files and unit-test files on branch `dcrl-20261005-0121` were compared by Git blob object ID against the exact local baseline that produced the 30/30 test run.

Result: **byte-for-byte identity confirmed for all 17 source/test files**.

See `TESTED_BLOB_MANIFEST.md`.

## Acceptance status

PASS:
- deterministic map-key canonicalization;
- non-finite float rejection;
- authority-order normalization;
- event-chain tamper detection;
- authority mutation detection;
- capsule-ID mutation detection;
- immutable AI-proposal label;
- valid PASS replay;
- valid FREEZE replay;
- execution-after-FREEZE rejection;
- PASS-without-verification rejection;
- unresolved tool-intent rejection;
- tool intent/result digest binding;
- FAIL and BLOCKED terminal proof rules;
- structural divergence detection;
- public receipt raw-payload minimization;
- CLI compile / verify / replay path.

## Limitations

NOT VERIFIED:
- production-scale throughput;
- cryptographic signatures/authentication;
- distributed concurrency;
- integration with the actual NEXY runtime;
- deployment/runtime security;
- persistence/encryption policy;
- browser/UI behavior.

## Scope proof

The implementation is stored under AI-CONTEXT only. No mutation to `goif74945-crypto/NEXY.AI-` is part of this work.
