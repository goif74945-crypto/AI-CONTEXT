# Test evidence register, 2026-10-09

| Check | Mode | Result |
|---|---|---|
| Schema validation, parser and payload rejection | Python pytest | PASS (see current test run) |
| Local filesystem write/read + traversal/symlink rejection | Python pytest on real filesystem | PASS (see current test run) |
| Trusted Python script run/exit failure/cancel/timeout | Python pytest using real interpreter | PASS (see current test run) |
| REST plan approval, token, exact plan use and cross-Origin denial | FastAPI TestClient | PASS (see current test run) |
| Real localhost server HTTP plan -> write -> read | uvicorn + httpx | PASS |
| Web UI JavaScript syntax | Node.js `node --check` | PASS |
| Android ADB argument safety | Unit tests with mocked ADB | PASS; REAL_DEVICE_NOT_TESTED |
| GitHub repository remote creation | Connected tools | BLOCKED: no create-repository capability exposed; not created |
| GitHub Actions CI | Authenticated GitHub | NOT_EXECUTED: requires remote repository |
| Real desktop mouse/keyboard control | User hardware | NOT_VERIFIED |
| Microphone / speech recognition / double-clap detector | User hardware | NOT_VERIFIED |
| Native standalone Android control | APK | NOT_IMPLEMENTED |
| Browser-driven UI live test | Headless Chromium | BLOCKED in tool environment: ERR_BLOCKED_BY_ADMINISTRATOR, not a proven UI defect |

A test PASS applies to exactly the tested boundary, never to the full hardware/software integration. The source is a bootstrap implementation, not a complete cross-platform autonomy product.
