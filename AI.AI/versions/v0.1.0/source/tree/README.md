# AI.AI · Local Device Agent (v0.1.0)

A **real, locally hosted prototype** that converts typed or spoken instructions to verified device actions. A double-clap can launch an eligible, explicitly approved pending plan. All operations run under the permissions of the local OS user, not via unrestricted cloud remote control.

## Status / honesty

- **Working source:** FastAPI local server, responsive web console, deterministic command parser, strict action validation, one-time plans, approval gate, emergency stop between actions, workspace-contained file operations, optional trusted Python script execution, Desktop GUI adapters, Android ADB adapters, optional OpenAI intent planner, browser-based speech input and experimental double-clap activation.
- **Depends on your machine:** desktop click/type/screenshot and ADB actions are only operational on a machine with a graphical session, granted OS permissions, Android platform-tools and an authorized connected device respectively. We cannot validate your physical phone/PC here.
- **Not included:** native Android on-phone AccessibilityService, iOS cross-app control, remote network pairing, reliable clap classifier, background service, production-grade LLM computer-use visual planning, script sandbox or permissionless control of arbitrary apps. Browser speech recognition is browser-dependent and may send audio to a provider. This is not production-ready autonomy.

## Setup

1. Install Python 3.11+ and Git. Open a terminal in this folder.
2. Create environment: `python -m venv .venv` and activate it.
3. Install: `pip install -e '.[test]'`. Optional AI planner: `pip install -e '.[test,llm]'`.
4. Run `python -m ai_ai.main` then open **http://127.0.0.1:8765** on the *same machine*.
5. Type `เปิด notepad`, `พิมพ์ สวัสดี`, `คลิก 500 300`, or click **Speak**, then **Generate plan**, inspect the steps, and click **Approve & execute**.
6. For a safe single-action demonstration: `จับภาพ` -> Generate plan -> **Arm double-clap**, clap twice within 30 seconds. Microphone permission required. The detection algorithm is experimental.
7. For Android: install Android SDK platform-tools, connect a device with USB debugging **and approve the RSA authorization prompt on the phone**. Execute `adb devices`, then enter `มือถือแตะ 200 400` or `มือถือเปิด com.android.settings`. This controls Android **from a connected computer**, not standalone on-device.
8. Optional natural language: set `OPENAI_API_KEY` in the process environment (never commit it) and select **AI interpretation**. Exact grammar works without any API key.
9. Trusted Python scripts: use `AI_AI_ENABLE_CODE_RUN=1` **only on a machine where you trust every workspace script**. The interpreter `-I` option is NOT a security sandbox.

Use `pytest` to run contract, policy, API and local integration tests.

## Commands

- `พิมพ์ Hello world` or `type Hello world`
- `คลิก 500 300` or `click 500 300`
- `กด ctrl+s` or `hotkey ctrl+s`
- `จับภาพ` or `screenshot`
- `เปิด notepad` or `open notepad` (`calculator`, `browser` available)
- `เขียนไฟล์ hello.py :: print(1+1)` or `write hello.py :: print(1+1)`
- `อ่านไฟล์ hello.py` or `read hello.py`
- `รันไฟล์ hello.py` or `run hello.py` (must explicitly enable trusted code execution)
- `มือถือแตะ 500 500` or `android tap 500 500`
- `มือถือพิมพ์ hello` or `android text hello` (basic ASCII only, via ADB)
- `มือถือเปิด com.android.settings` or `android open com.android.settings`

One instruction per line; executes in given order. Unicode Thai typing on desktop uses clipboard, requiring a working system clipboard. `pyautogui` emergency failsafe: move pointer to the upper-left corner.

## Security boundaries

- Server binds `127.0.0.1` only; validates Host + Origin, requires an ephemeral session token and explicit exact-plan approval; no CORS enabled.
- Planner output is **untrusted** and validated as a strict discriminated union of the 12 permitted actions. Invalid/unknown instructions fail closed. No arbitrary shell action exists in the planner.
- Plans are one-use and expire after 180s. Double-clap must be armed manually for 30s and is blocked for writing/running code and Android changes. It is never always-listening.
- File access restricted to `workspace/` with checked real paths and atomic replacement. Treat symlink races and native GUIs as a local-trust boundary, not a robust isolated container.
- `code.run` can execute real Python under the user's privileges and can access the network/filesystem despite workspace path restrictions. It is opt-in for **trusted** code only. Python does not provide a reliable OS sandbox.
- Stop checks between actions; long-running code supports cancellation/timeout. GUI and ADB calls may finish before Stop takes effect. Never rely on this as an emergency electrical/safety control.
- No secret keys in source. No SMS/calls, admin elevation, hidden spying, credential extraction or background persistence.

## Architecture

```
Web UI (text, browser speech, double-clap)
    -> localhost API (token, Origin, Host)
    -> deterministic / optional LLM proposal
    -> schema validation + one-time reviewed plan
    -> single-writer execution + cancellation
    -> Desktop GUI | local workspace | trusted script | Android ADB
```

## Planned production phases (NOT yet implemented)

1. Native Android AccessibilityService with consent and Play policy compliance, per-app capability grants, iOS accessibility-aware limitations.
2. Desktop vision planner (screen grounding/coordinate verification), error retries and multi-app workflows with audit evidence.
3. Signed pairing protocol to control desktop from phone over trusted network, per-device session authorization and full audit log.
4. Offline speech transcription and calibrated clap-classification training/false-positive tests.
5. OS-level sandbox for code execution, proper policy engine, reproducible end-to-end device tests, CI release gates.

**Repository policy:** exactly one branch, `main`. No mutation to NEXY.AI or AI-CONTEXT occurs as part of this project.
