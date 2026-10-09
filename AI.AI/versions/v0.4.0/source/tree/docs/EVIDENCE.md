# AI.AI v0.2 | Test evidence register, 2026-10-09

| Evidence category | Status | Scope |
|---|---|---|
| 114 automated tests | **PASS locally** | `python -m pytest -q`; includes schema, UI grounding, HTTP, local file/subprocess, app launcher, browser mock, Android mock and adversarial/negative cases |
| JS syntax | **PASS** | `node --check ai_ai/web/app.js` |
| Python module compile | **PASS** | `python -m compileall -q ai_ai tests` |
| Real Tesseract OCR | **PASS (synthetic image)** | Local Tesseract recognized a generated `SAVE` image and satisfied confidence threshold |
| Wheel package build/install | **PASS** | Built v0.2 wheel, installed in a separate target directory and imported package successfully |
| UI resources in built wheel | **PASS** | `/`, `/app.js`, `/app.css` HTTP responses from installed package |
| Real HTTP server and user effect | **PASS** | Spawned actual uvicorn `127.0.0.1:18473`; created one-time plan; executed file write; read file back; confirmed audit event |
| Real Chromium GUI | **BLOCKED** | Chromium executable absent; Playwright download failed with `EAI_AGAIN` DNS errors on CDN hosts |
| Actual desktop OCR clicks and app focus | **NOT_VERIFIED** | No authorized interactive desktop session available |
| Actual Android UIAutomator / ADB | **NOT_VERIFIED** | No connected authorized handset |
| Actual browser voice/double clap | **NOT_VERIFIED** | No user microphone tested |
| iOS/native Android APK | **NOT_IMPLEMENTED** | Not supplied in source |
| Remote GitHub AI.AI/CI | **NOT_EXECUTED** | Repo not created with available GitHub tool actions |

These PASS statuses certify the test surfaces described, not universal OS automation, model intelligence, accuracy, safety or product completeness. See `V0.2-AUDIT.md` and `SECURITY.md`.

## v0.4 engineering update (2026-10-09)

See `docs/V0.4-ENGINEERING-AUDIT.md` for nine added tool contracts, bounded UI inspections, stale-target checks, preflight plan assurance, stop-race handling, request-origin enforcement and present hardware/network blockers. Version 0.4 evidence is always tied to the current source commit and generated archive; prior tests and snapshots are not substitutes for new execution evidence.
