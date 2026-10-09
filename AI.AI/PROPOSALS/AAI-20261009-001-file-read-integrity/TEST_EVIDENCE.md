# Test evidence | AAI-20261009-001

Source used: AI.AI-main-v0.2.0.zip SHA256 5dd451976a03b404f508f296c4489319e945a65d0de782005c56b9841130d720; embedded main 0b226669d5635339c00c3836d91dca9bfbf63cea.

Before: Executor.perform(file.read) returned only 20,000 characters from a 120,000-character text file without error. Reproduced in the preceding independent v0.2 audit and verified original source has [:20000].

After applying integration.patch to an ISOLATED local source copy (not the protected current-code folder):

    python -m pytest -q tests/test_executor.py
    ..............                                                           [100%]
    # 14/14 PASS

    python -m pytest -q
    ........................................................................ [ 61%]
    .............................................                            [100%]
    # 117/117 PASS (original 114 + 3 new tests)

    python -m compileall -q ai_ai tests
    # PASS, exit 0

On untouched original source, patch --dry-run -p1 < integration.patch:

    checking file ai_ai/executor.py
    checking file tests/test_executor.py
    PATCH_DRY_RUN=PASS

Patch SHA256: d05c180adb45640d79f7128bbbe1b7272889c10c2bc666ef347340578ebe7fa9.

Tests explicitly cover exact boundary, 1-character overflow, and Thai Unicode under the 200,000-byte source limit. No mock substitutes for these filesystem tests. No claim of Android/browser/real device E2E.

Limitations: source v0.2 only; v0.3 has a historical release record but source/compatibility NOT VERIFIED; no GitHub product merge, production CI or real-device E2E. Consumers must run git apply --check and latest product tests before claiming MERGE_READY.
