# AI.AI Chrome Companion v0.4.1 — Manifest root packaging correction (2026-10-10)

## Symptom and evidence
User reported Chrome Load unpacked: "Manifest file is missing or unreadable." Exact prior distributed ZIP `AI.AI-Chrome-Companion-v0.4.1-TEST.zip` was inspected in the current local runtime.
- Its valid JSON manifest was at `chrome-extension/manifest.json`, not ZIP archive root.
- If the user selected the ZIP-extracted outer directory, Chrome could not find the manifest. We did not inspect the user's file picker, so the exact local folder they selected is UNKNOWN.
- Prior manifest was readable and parsed as Manifest V3.

## Fix implemented locally, outside protected source repositories
- Repackaged extension files at the ZIP **root**, including `manifest.json` alongside `background.mjs`, `content.js`, `panel/`, `lib/`, `icons/`.
- Corrected installation instructions; retained test-site and tests. No JavaScript behavioral code changes.
- New conversation ZIP: `AI.AI-Chrome-Companion-v0.4.1-MANIFEST-FIX.zip`.
- SHA-256: `c496c605766a3ea6df65e8f38be941d3b44dca7dac36e86332ba78a5addd3f7a`.
- Size 23490 bytes, 18 files, ZIP CRC `testzip() = None`; original JSON manifest and required declared file references verified.
- Extracted ZIP to clean directory; verified `manifest.json` immediately exists and parses as MV3.
- `node --test .../tests-js/extension.test.mjs` PASS 12/12; JS syntax checks for background/content/panel PASS.
- NOT VERIFIED: Chrome installed extension successfully in actual user's Windows Chrome. No live device result available.

## Provenance and scope
Existing AI-CONTEXT candidate: `AI.AI/PROPOSALS/AAI-20261009-003-chrome-companion`.
Baseline product: AI.AI v0.4.0; generated standalone test ZIP is **not** full Python AI.AI.
This experiment note is evidence-only. Do not modify source snapshot, product repo, `โค้ดโปรเจคปัจจุบัน`, or `goif74945-crypto/NEXY.AI-`.
