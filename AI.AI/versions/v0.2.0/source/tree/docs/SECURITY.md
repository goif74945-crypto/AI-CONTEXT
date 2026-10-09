# Security review | AI.AI v0.2

## Confirmed controls

- Process HTTP listener loopback `127.0.0.1` only; requests to unexpected Host rejected; state-changing requests require same-site Origin and transient `X-AI-AI-TOKEN`.
- Plan content is schema-checked. Tools/actions outside the closed registry are rejected. User must review and explicitly approve a single-use plan. Expiry is three minutes.
- Side-effect tools (typing, clicking, launching apps, browser navigation/forms, Android gestures) cannot be triggered by clap. Other plan types may be armed for 30 seconds. Browser voice recognition is opt-in and may send audio to a provider.
- Browser automation uses separate Chromium session, not existing browser credentials; no auto-download acceptance. Exact locator uniqueness is checked.
- Desktop OCR and Android XML label selection require a unique grounded match. Missing or ambiguous targets have zero-click behavior in mocked tests. OCR is not guaranteed correct even with a high confidence score.
- Optional screenshot OCR can reach an external LLM **only after separate opt-in**, in addition to AI planning opt-in. Avoid sharing sensitive visible screens.
- Filesystem paths are restricted to workspace. Screenshots are written with atomic replace. Arbitrary script execution disabled by default; registered app launch is owner-configured.
- Android ADB device must be user authorized; serial and package values strictly validated. UIAutomator XML has a size ceiling and rejects declared XML entities.
- Audit file records tool name/step/status/plan ID with no command content or OCR. This is *local diagnostic evidence only*, vulnerable to deletion/modification by the local user or other privileged processes.

## Residual risks and blockers

- **Critical policy:** `AI_AI_ENABLE_CODE_RUN=1` allows Python scripts to act with the local OS user's permissions. Python `-I` is not a system sandbox. Do not use this mode for untrusted generated code.
- **Critical policy:** The user may approve a harmful action (delete through UI, submit form, transfer data). Validation ensures a valid *tool call*, not a proof that all side effects are harmless.
- **Security boundary:** local malware running with user permissions may access loopback services/OS peripherals; this app does not defend against an already-compromised OS.
- **Storage boundary:** verified path resolution and screenshot atomic writes do not eliminate all symlink/hardlink races for arbitrary local attackers or scripts. Do not treat workspace as a secure container.
- **UI identity:** OCR false recognition, wrong window focus, browser transient elements, inaccessible Android elements and screen scaling remain possible. Some system dialogs reject automation.
- **Web:** user-reviewed URLs can still load malicious websites or scripts; isolated context is not a browser exploit sandbox. Screenshots and input may contain sensitive data; do not log them or upload without consent.
- **Execution:** Stop is best-effort. A committed click or submission cannot be undone. If audit write fails before execution, fail closed; if it fails after side effects, result may be uncertain. Manual recovery needed.
- **Device boundaries:** iOS apps cannot be controlled arbitrarily, no native Android AccessibilityService, no remote pairing or platform permission bypass.
- **Verification:** physical desktops/Android devices and real Chromium not tested in this environment. Production certification remains **NOT_VERIFIED**.
