# AAI-20261009-001 | File Read Result-Integrity Gate

## CRITICISM: demonstrated bug in v0.2.0

Zip: AI.AI-main-v0.2.0.zip, SHA-256 5dd451976a03b404f508f296c4489319e945a65d0de782005c56b9841130d720. Embedded Git main HEAD: 0b226669d5635339c00c3836d91dca9bfbf63cea.

Source: ai_ai/executor.py, Executor.perform(file.read). Current v0.2 accepts files up to 200,000 bytes but uses read_text(encoding="utf-8")[:20000], silently returning 20,000 characters for a 120,000-character file while claiming PASS. ai_ai/server.py also caps result text at 20,000. This is a real data-integrity bug, medium severity, especially during source audits.

## NEW IMPLEMENTABLE REPAIR SYSTEM

Return exact complete text only within the pre-existing 20,000-character result contract. Read a bounded 20,001 Unicode characters; raise ActionError if there is even one over the cap. Keep existing workspace path, 200,000-byte and user approval controls. This fails closed instead of silently reporting incomplete evidence as complete.

Integration patch includes source code and three new tests: 20,000 ASCII characters preserved; 20,001 rejected; Thai Unicode boundary accepted and then rejected above the limit.

## Exact integration instructions

Use a disposable copy of AI.AI v0.2.0 at embedded SHA 0b226669d5635339c00c3836d91dca9bfbf63cea. From project root:

    git apply --check /absolute/path/to/integration.patch
    git apply /absolute/path/to/integration.patch
    python -m pytest -q tests/test_executor.py
    python -m pytest -q
    python -m compileall -q ai_ai tests

This patch changes ONLY ai_ai/executor.py and tests/test_executor.py inside the disposable source copy. It does NOT touch protected project code in AI-CONTEXT. Tests require the original package test dependencies.

## Safety/compatibility and observed state

For reads longer than 20,000 characters, behavior intentionally changes from partial PASS to explicit error; callers should handle ActionError. File streaming/chunking remains OUT OF SCOPE and would require a new API contract. This is compatible with old file size/path restrictions. Do not treat a source patch as a physical device test.

Status: TESTED_ON_PINNED_REVISION for v0.2 only. A historical AI.AI v0.3 record exists, but v0.3 source was not available in the uploaded ZIP; compatibility with v0.3 and current deployed product is UNKNOWN until fresh tests. No product merge or CI claim.
