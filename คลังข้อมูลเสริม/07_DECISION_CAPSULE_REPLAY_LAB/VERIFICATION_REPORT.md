# Verification Report

Target: local standalone reference implementation under AI-CONTEXT supplemental lab.  
Status: PASS for prototype acceptance criteria listed below.  
NEXY.AI implementation status: NOT_VERIFIED / NOT MODIFIED.

## Evidence executed

Commands:

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

Observed:
- 30 tests executed, 30 passed;
- compileall passed;
- PASS example compile/verify/replay/receipt passed;
- FREEZE example compile/replay passed;
- PASS example capsule ID: `e633317c88b7f23a79520efd1ea5ff3cb4bf18d9a52e9a3b294b5b99516c7eff`;
- FREEZE example capsule ID: `bb663b764a7482b9ee8b959973439096298f72411b8ad5b03d8c9bb60d3359e0`;
- local benchmark, 10,000 capsules x 6 events: ~10,031 builds/s and ~12,201 replays/s in the observed container. This is not a production guarantee.

## Acceptance status

PASS:
- deterministic map-key canonicalization;
- non-finite float rejection;
- authority-order normalization;
- event-chain tamper detection;
- authority mutation detection;
- capsule-ID mutation detection;
- immutable proposal label;
- valid PASS replay;
- valid FREEZE replay;
- execution-after-FREEZE rejection;
- PASS-without-verification rejection;
- unresolved tool intent rejection;
- tool intent/result digest binding;
- FAIL and BLOCKED terminal proof rules;
- structural divergence detection;
- public receipt raw-payload minimization;
- CLI compile/verify/replay path.

## Limitations

NOT VERIFIED:
- production-scale throughput;
- cryptographic signatures/authentication;
- distributed concurrency;
- integration with the actual NEXY runtime;
- deployment/runtime security;
- persistence/encryption policy;
- browser/UI behavior.
