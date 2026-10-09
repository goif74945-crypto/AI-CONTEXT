# AI.AI | User-Controlled Desktop + Android + Browser Agent (v0.3.0)

AI.AI runs on your own computer. It accepts typed commands, optional browser speech-to-text, and **time-limited double-clap activation of reviewed low-risk plans**. It proposes one plan, shows every step for approval, and executes strictly typed capabilities. It **does not** grant an AI unlimited system permissions. No current implementation can reliably perform every on-screen action across every OS and application.

## New in v0.3.0

- Exact active-window guard: `desktop.assert_window`, plus `@window=Title` suffix on desktop click/type/hotkey/scroll/click-text. A mismatch or unavailable window API **aborts without input**. Window detection is platform-dependent and a title is not a security credential.
- Browser-origin boundary: explicitly opened site is pinned during subsequent DOM actions; cross-origin redirects and inspectable external links, forms and popup targets are rejected. Navigation caused by JavaScript and asynchronous redirects cannot be fully prevented by this check.
- Accessible semantic element click: `browser.click_role`, requiring exactly one visible, enabled matching button/link/tab/etc.
- Model grounding gate: rejects LLM-invented coordinates, target labels, URLs, file paths and typed strings absent from the original user request (conservative: may reject legitimate paraphrases).
- Android UI click selects the nearest clickable ancestor when provided and rejects disabled targets; assertion still observes disabled labels.
- Regression suite expanded with adversarial wrong-window, wrong-site, XML, ambiguous UI and untrusted OCR scenarios.

## Carried forward from v0.2.0

- **30 typed actions**: desktop mouse/keyboard/screenshot, **local OCR click/verify/wait by unique visible text**, registered-app launch, workspace file operations, opt-in trusted Python execution, Android ADB tap/text/open/swipe/system key/screenshot/**UIAutomator exact-text tap/verify**, and **Playwright browser navigation, semantic text click, form fill, wait/assert, screenshot**.
- Up to **24 approved steps per plan** with ordered execution, stop between steps, explicit text verification, no blind retries after an uncertain mutation.
- **Optional OCR evidence for AI planning**: opt-in checkbox. The OCR runs locally, but selecting *Share visible OCR with AI* transmits extracted screen text to the configured model provider. Without that option, **screenshots and OCR results are not uploaded by AI.AI**.
- **Local audit events** for proposed plans, execution steps, stop and failure; excludes command contents, OCR text and input values. This local file can be tampered with by the OS user, so it is *not cryptographic audit evidence*.
- Newly created desktop/browser screenshots use atomic replacement to prevent following an existing screenshot symlink. Android screenshots validate PNG headers and a size bound.

## Install on Windows / Linux / macOS

1. Install Python 3.11+ and Git, unpack the ZIP, and open a terminal inside the `AI.AI` folder.
2. Create a venv with `python -m venv .venv`, activate it, and run `python -m pip install -e '.[test]'`.
3. Run `python -m ai_ai.main` and open `http://127.0.0.1:8765` **on the same computer**.
4. Type commands (one line per action), click **Generate plan**, carefully inspect, then click **Approve & execute**. Each plan is single-use and expires in 180 seconds.
5. For optional OCR: install `python -m pip install -e '.[vision]'` and the external **Tesseract OCR executable** for your OS. English is the default (`AI_AI_OCR_LANG=eng`). For Thai, install Thai Tesseract language data and set `AI_AI_OCR_LANG=eng+tha`; accuracy depends on font/language/model.
6. For optional DOM browser: install `python -m pip install -e '.[browser]'`, then `python -m playwright install chromium`. An interactive graphical session is needed by default. `AI_AI_BROWSER_HEADLESS=1` is optional for testing in supported servers. If Playwright cannot download Chromium but a trusted system Chromium is installed, set `AI_AI_BROWSER_EXECUTABLE` to its existing **absolute path**, e.g. `/usr/bin/chromium`.
7. For optional natural language planning: install `python -m pip install -e '.[llm]'`, set `OPENAI_API_KEY` as an environment variable, then select **AI interpretation**. The model only *proposes* actions and still requires confirmation.
8. For Android, connect a phone using **authorized USB debugging**, install Android SDK platform-tools (`adb devices` must show `device`). No native Android APK has been built. Android actions run from the computer via ADB.
9. Trusted Python script execution is **OFF by default**. Set `AI_AI_ENABLE_CODE_RUN=1` only for code and workspace you trust. **Python -I is not a security sandbox.**
10. To run automated tests: `python -m pytest -q`.

**Windows example of setting an optional variable in PowerShell:** `$env:AI_AI_OCR_LANG='eng+tha'`. Linux/macOS shell example: `export AI_AI_OCR_LANG='eng+tha'`. The `.env.example` file is documentation; it is not automatically loaded.

## Command grammar

```text
เปิด notepad
พิมพ์ สวัสดี
คลิกข้อความ Save @window=Notepad
ตรวจหน้าต่าง Notepad
ตรวจข้อความ Done
รอข้อความ Ready :: 5
จับภาพ
เปิดแอป vscode
เว็บเปิด https://example.org
เว็บคลิก Continue
เว็บคลิกบทบาท button :: Continue
เว็บตรวจURL https://example.org/result
เว็บกรอก Search :: research query
เว็บตรวจ Results
เว็บรอ Results :: 5
เว็บจับภาพ
มือถือเปิด com.android.settings
มือถือปัด 500 900 500 250 450
มือถือกด BACK
มือถือคลิกข้อความ Settings
มือถือตรวจข้อความ Settings
มือถือจับภาพ
เขียนไฟล์ hello.py :: print(2+3)
รันไฟล์ hello.py
```

All grammar has an equivalent English form (see `ai_ai/planner.py`). `เปิดแอป vscode` works **only** if its alias is registered, e.g. the owner's `AI_AI_APP_ALLOWLIST_JSON={"vscode":["code"]}` environment variable. Aliases launch exact argv without `shell=True`. A command opening an arbitrary unregistered executable is rejected.

## Real boundary vs. promises

| Capability | Status |
|---|---|
| Strict parser, approval, local HTTP API, audit log, workspace/file/script tests | Implemented and locally tested |
| OCR on a generated sample image | Locally tested with installed Tesseract |
| Browser DOM operations | Real headless Chromium DOM interactions (injected HTML: fill, click role, assert, screenshot and negative click guards) **passed**; Chromium HTTP navigation is **BLOCKED by environment policy**, not verified |
| Desktop real mouse/keyboard on your PC | Requires OS permissions and on-device testing; **NOT VERIFIED** |
| Android ADB actions and UIAutomator on your actual phone | Requires a connected, authorized device; **NOT VERIFIED** |
| Web Speech API and acoustic double-clap | Included but microphone classification **NOT VERIFIED** |
| Standalone Android control via AccessibilityService / iPhone cross-app operations | **NOT IMPLEMENTED** |
| Autonomous long-running self-monitoring, general OS sandbox, full visual computer-use AI | **NOT IMPLEMENTED** |
| GitHub repository `AI.AI` | **NOT CREATED ON GITHUB**; local single-branch Git repository supplied |

## Security policy

The server binds only to loopback; checks Host and Origin; uses an ephemeral token, strict tool schemas, one-time plans and an explicit approval literal. Unsafe/side-effect actions are **not** eligible for clap activation. Screen text from OCR, Android accessibility XML and web page text are *untrusted evidence*, not instructions. The model may still make errors. Browser automation starts in a fresh isolated Playwright context, not in your existing signed-in browser account. The browser can access external websites; review destination and actions carefully. Scripts run with the OS user's privileges if explicitly enabled. Stop is best effort between actions and cannot undo completed actions. Detailed limitations: `docs/SECURITY.md`.

Architecture: `docs/ARCHITECTURE.md`. Test evidence and remaining gaps: `docs/EVIDENCE.md`. Development ledger: `docs/V0.2-AUDIT.md`.

**Branch policy:** local repository branch **`main` only**. No code change was made to `goif74945-crypto/NEXY.AI-`. GitHub repository creation remains unavailable via the tools of this chat.
