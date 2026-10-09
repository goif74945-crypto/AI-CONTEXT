# AAI-20261009-003 | AI.AI Chrome Companion v0.4.1 (candidate)
**Target product:** AI.AI v0.4.0, exact local main HEAD `95741bede86405685a022633df03a2c39ce7fc4c`. Baseline ZIP SHA256 `5e47a9cb11f52be3c8c13be86a4551246d30d601091b6919b5dbbe6a3d9dd733`.

## Distinct criticism and testable improvement
The original `ai_ai/browser.py` lines 1-4 and 82-100 create a private Playwright Chromium context instead of controlling user's Google Chrome tabs. `ai_ai/server.py` lines 67-80 store a one-time pending plan for 180 seconds. There is no Manifest V3 Chrome extension or durable multi-day browser workflow executor in that source. This gap is different from AAI-001 file.read truncation and AAI-002 stale OCR coordinates.

**Idea:** User-approved site-scoped MV3 Chrome companion with side panel; read-only page inspection and extractive analysis; typed click/fill/scroll/navigate/assert/wait; optional per-site host permission; 30-second Chrome alarms, persistent checkpoints, explicit emergency stop, no blind repeat after uncertain mutation, and maximum plan duration seven days. Full extension source and tests are present inside a **complete tested integration patch**, transported as gzip/Base64 to preserve bytes.

## Extract exact executable patch (Python 3.11+)
```bash
python unpack_patch.py FULL-INTEGRATION-PATCH.b64.md integration.patch
sha256sum integration.patch
# MUST equal 7ff3a856b1eba7dac7d745c04463fc8c4ac5934d85eb30f4271e29ac20ae3234
# From an isolated fresh copy of the exact pinned AI.AI v0.4.0 source:
git apply --check /absolute/path/integration.patch
git apply /absolute/path/integration.patch
python -m pytest -q -o addopts=''
node --test tests-js/*.test.mjs
python tests-chrome/dom_smoke.py
```
This patch creates `chrome-extension/`, `tests-js/extension.test.mjs`, `tests-chrome/dom_smoke.py`, plus docs. No existing protected paths are modified.

## Chrome installation
Download the unpacked extension from the chat artifact, or apply the patch then open Chrome Desktop `chrome://extensions` > Developer mode > Load unpacked > choose `chrome-extension`. Review the site and commands, request origin permission, then start. Do not confuse seven-day scheduling cap with a validated seven-day run.

## Evidence and limitations
See [TEST_EVIDENCE.md](TEST_EVIDENCE.md). Isolated patch applied successfully with all Python/Node and actual injected-DOM checks. **NOT VERIFIED:** Chrome extension installation in this runtime (blocked by administrator), user-device reliability, service-worker long soak, multi-day task success, remote GitHub Product merge. Workflows are site-scoped, not universal OS automation; no external generative AI connected. No CAPTCHA bypass, hidden access or password operations. Page text remains untrusted data.

**State:** TESTED_ON_PINNED_REVISION for isolated patched v0.4.0, NOT MERGED, NOT PRODUCTION CERTIFIED.
