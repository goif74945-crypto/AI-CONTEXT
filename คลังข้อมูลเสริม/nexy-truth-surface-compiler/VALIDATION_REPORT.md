# Validation Report

## Classification
**PROTOTYPE VALIDATION ONLY. NOT NEXY.AI INTEGRATION OR DEPLOYMENT EVIDENCE.**

## Executed environment
- Python: `3.13.5`
- Dependency model: Python standard library only for runtime/tests
- Target: local mirror of `คลังข้อมูลเสริม/nexy-truth-surface-compiler`

## Executed commands

```bash
python -m compileall -q src tests tools
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m nxts.cli fixtures/release.json
PYTHONPATH=src python -m nxts.cli fixtures/freeze-unknown.json
PYTHONPATH=src python -m nxts.cli fixtures/freeze-conflict.json
```

## Observed results
- compileall: PASS
- unit/adversarial/golden-vector suite: **25 tests / 25 PASS**
- release fixture: decision `RELEASE`, process exit `0`
- freeze-unknown fixture: decision `FREEZE`, process exit `2`, blocker `MATERIAL_UNKNOWN`
- freeze-conflict fixture: decision `FREEZE`, process exit `2`, blocker `MATERIAL_CONFLICT`
- release fixture output SHA-256 receipt: `4714ef33adec2b330788c89f2c275575f39cf1bda39dda86ca225204f7ff4a54`
- freeze-unknown output SHA-256 receipt: `bd6dc7c1353d1cb2310dc486aeb33b1f6f56e70771a8ae64cdd3c18f53dd7324`
- freeze-conflict output SHA-256 receipt: `36e3f22e1a88a02559ff1ea2ae89d413517626c99ab917821ee3d8004a4a78a8`

## Proven
- E1: Python sources/tests/tools compile in the observed environment.
- E2: the 25 executed tests pass against compiler version `0.2.0`.
- E2/subprocess: CLI uses exit 0 for RELEASE and exit 2 for tested FREEZE paths.
- Golden vectors match the current reference implementation.

## Not proven
- production-grade DLP or complete secret detection;
- semantic validity of evidence references;
- compatibility with any current NEXY.AI implementation code;
- browser/UI behavior;
- performance/load behavior;
- deployment behavior;
- security beyond the narrow executed tests;
- canonical NEXY authority status.

## Status
Reference prototype validation: **PASS for executed local scope**.  
NEXY.AI integration: **NOT_VERIFIED**.  
Deployment: **NOT_VERIFIED**.  
Canonical adoption: **NOT AUTHORIZED / PROPOSAL ONLY**.
