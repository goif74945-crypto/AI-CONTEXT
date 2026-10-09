# TEST_EVIDENCE | AAI-20261009-002 | 2026-10-09
- Product source: exact local v0.4.0 release ZIP SHA256 `5e47a9cb11f52be3c8c13be86a4551246d30d601091b6919b5dbbe6a3d9dd733` and embedded HEAD `95741bede86405685a022633df03a2c39ce7fc4c`.
- Patch SHA256 `1d617ada2f229aed326cb5f6f8faea12dbc074abb71acdab06e4e34db99fcbeb`; Git blob SHA `ce0eb4386504c34863a89b37ba9825b2de7157fe`.
- `git apply --check`: exit 0 on FRESH COPY; actual `git apply`: exit 0; byte-level equality against development candidate for source and tests: TRUE.
- Focused new regression tests: `8 passed`; full v0.4.0 suite + tests: `224 passed in 5.27s`; `python -m compileall -q ai_ai tests`: exit 0.
- Negative proof against ORIGINAL baseline (not patched): run `tests/test_adaptive_click.py::test_small_drift_requires_third_and_uses_latest_center` in isolated UNMODIFIED v0.4.0 copy. Exit 1; `1 failed in 0.12s`; expected click(34,30), actual click(30,30). This FAIL is intentional reproduction.
- System under test: Python 3.13, pytest in local runtime; `unittest.mock.Mock` desktop and synthetic OCR hits; no real pointer event injected.
- Remaining gates: Actual mouse/window behavior and performance on approved Windows/macOS/Linux devices NOT_RUN; complete system reliability and user task completion NOT_VERIFIED; no GitHub Product CI.
- Protected `โค้ดโปรเจคปัจจุบัน` and Product GitHub repositories unchanged.
**VERDICT:** TESTED_ON_PINNED_REVISION, not MERGE_READY or MERGED without current-head authorization/physical proof.
