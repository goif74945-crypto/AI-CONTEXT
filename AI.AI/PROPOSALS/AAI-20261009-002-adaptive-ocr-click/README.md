# AAI-20261009-002 | Adaptive Third-Frame OCR Click Stability Gate
**Chat:** CHAT-20261009-AI-AI-V04-002. **Version:** AI.AI v0.4.0; embedded main HEAD `95741bede86405685a022633df03a2c39ce7fc4c`.
**Authority:** [AI.AI/CONSTITUTION.md](../../CONSTITUTION.md). **Scope:** candidate-only AI-CONTEXT/AI.AI/PROPOSALS/**; never modify protected code folders.

## FACT: independently reproducible criticism
Original `ai_ai/executor.py`, `Executor._desktop_text`, lines 127-141: two OCR reads are taken and movement <=8px is allowed, but the pointer event uses `hit.center` from the FIRST read, not `confirmed.center` from the freshest read. Repro: first center (30,30); second center (34,30); baseline clicks (30,30). Isolated negative test fails as expected: `Expected: click(34, 30); Actual: click(30, 30)`. The bug is an input-targeting integrity issue, not proof of a real-device incident.

## UNIQUE IDEA
Adaptive third observation when two frame centers differ <=8px, otherwise existing two-frame fast path. If a third frame center differs from second, raise `ActionError` and perform no click. On stable confirmation, click at latest verified center, and accurately report latest coordinates/confidence. Existing window identity and cancellation checks remain AFTER the final observation. New test covers stable fast path, small corrected drift, repeated drift blocked, large drift blocked, ambiguous result blocked, wrong window blocked, emergency stop blocked and missing target blocked.

**Difference vs AAI-001:** This idea addresses stale OCR mouse coordinates in the desktop action engine; AAI-001 addresses file.read silent truncation. Separate defect class, touched behavior and test suite.

## Integration contract
Source: `AI.AI-main-v0.4.0.zip` SHA256 `5e47a9cb11f52be3c8c13be86a4551246d30d601091b6919b5dbbe6a3d9dd733`. Git `main` HEAD `95741bede86405685a022633df03a2c39ce7fc4c`.
Patch: [integration.patch](integration.patch), SHA256 `1d617ada2f229aed326cb5f6f8faea12dbc074abb71acdab06e4e34db99fcbeb`.
Touches ONLY `ai_ai/executor.py` and `tests/test_adaptive_click.py`. No extra runtime dependencies. Command from disposable copy of pinned source:
```bash
git apply --check /path/to/integration.patch
git apply /path/to/integration.patch
python -m pytest -q -o addopts=''
python -m compileall -q ai_ai tests
```
Rollback: restore original `executor.py` from pinned source ZIP; remove new test file (or reverse this exact patch on the disposable copy). Not an authorization to touch an existing protected directory or live product.

## Risk / limitations
Adding another OCR capture only on movement increases latency and still cannot guarantee that a UI stays stationary AFTER the scan. No physical desktop E2E, no reliability benchmark and no guarantee all OCR boxes are correct. CPU/OCR errors fail closed, not silently accepted. The patch has passed mocked GUI regressions and all v0.4.0 Python tests in an isolated copy, but is not yet merged to any live AI.AI release.

Status: **TESTED_ON_PINNED_REVISION / NOT_MERGED**.
