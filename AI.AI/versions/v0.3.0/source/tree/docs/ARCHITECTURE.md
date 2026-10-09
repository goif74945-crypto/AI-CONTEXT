# AI.AI v0.3 | System design and authority model

## Trust model

The current operator instruction is the source of intent. The optional LLM planner, OCR snippets, UIAutomator hierarchy, browser page content, voice transcription and GitHub documentation are untrusted *observations*. Their text cannot grant new tools, change the safety policy, or bypass the reviewed plan. User reviews the exact plan and confirms before execution. Desktop/ADB/browser actions run under permissions explicitly granted to the local OS and authorized device.

## Runtime graph

```text
Operator (typing / browser speech / armed double clap)
    -> loopback Web UI
    -> Host/Origin + transient session token checks
    -> rule grammar OR optional LLM with separately opted-in OCR text
    -> strict discriminated tool contracts (30 types, max 24 per plan)
    -> one-time plan (TTL 180 seconds, review + approval)
    -> one-at-a-time executor + best-effort Stop + local metadata-only audit
        -> PyAutoGUI + local Tesseract OCR (optional)
        -> Owner-registered app launcher (argv only)
        -> restricted workspace file APIs + opt-in trusted Python interpreter
        -> Android platform-tools ADB + UIAutomator hierarchy
        -> isolated Playwright Chromium context (optional)
```

## Perception and execution evidence

- On platforms exposing active-window identity (notably Windows), callers can require an exact title per desktop input. OCR click actions recheck the title immediately before clicking.
- Desktop text targets are resolved from a **fresh screenshot**. OCR tokens with confidence below 65 are ignored. Exact Unicode-normalized match is required, and a duplicate/missing target aborts without a click. No automatic retry of a side-effect action.
- Android tap targets prefer an enabled clickable ancestor of the unique label; assertion can observe disabled labels.
- Android exact-text targets use a fresh UI hierarchy (`uiautomator dump`) and coordinate bounds. Bad XML, duplicate matches, and absent/invalid bounds abort the plan. ADB shell operations use argument lists, not a system shell command string.
- Web actions query **live Playwright DOM locators** by exact text, accessible role/name, label or placeholder, require a unique target, and can assert/wait for results. The Playwright objects belong to a single dedicated worker thread.
- DOM actions require a previously approved navigation to the same scheme, host and port. External redirects and inspectable external click targets fail closed; asynchronous redirects and script-triggered navigation are residual risks.
- AI model output is checked against the original operator wording for targets, typed text, requested URLs and paths, as well as strict action schema. This may reject valid paraphrases.
- A plan can use `assert`/`wait` to check observable outcomes but there is **no universal semantic success oracle** for arbitrary applications. Each action result reports only what it actually observed.
- Local audit logs event identifiers, tool names and states, **not content or screen text**. Audit is workspace-writable and is not tamper-proof.

## Exactly one branch and repo boundaries

`AI.AI/main` only for this local source. It is not the existing NEXY.AI product; no changes to NEXY.AI are authorized by this project. The GitHub remote `AI.AI` is absent. The control repo AI-CONTEXT is for evidence reports only.

## Not achieved / production exit gates

1. Real Windows/macOS/Linux graphical-system E2E with multiple displays, scaling, permission dialogs, OCR error rate and OS focus behavior.
2. Real Android on multiple authorized device versions with UIAutomator locale, latency, hierarchy timing, offline fallback and storage policy.
3. Real Chromium semantic actions with interactive session, cookies/login, accessibility, page churn, stale DOM and navigation tests.
4. Speech + clap calibration, false-positive/false-negative, browser vendor privacy and unreliable recognition.
5. Native Android AccessibilityService APK with user-granted per-app control, iOS restrictions, and any remote secure pairing.
6. Stronger OS sandbox for untrusted code, recovery semantics after irreversible operations, full device policy and privacy reviews.

Tests of schemas, mocks or generated images do **not** close these requirements.
