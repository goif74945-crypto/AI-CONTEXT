# Threat model and safety constraints

| Threat | Current measure | Residual risk |
|---|---|---|
| A webpage issues unwanted commands | Loopback binding, Host + Origin check, ephemeral token, strict content type and one-use plan | Malicious software already running as the same OS account can control local services |
| LLM hallucinates dangerous tools | Closed discriminated union; unknown tools/arguments rejected; manual approval | Allowed mouse clicks and hotkeys can still be dangerous; operator must inspect coordinates/context |
| Voice false transcription / audio spoofing | Speech becomes a plan, not an action | Text can still be misunderstood; browser speech may use vendor servers |
| Clap false activation | Manual arming; 30-second expiry; double clap; blocked higher-risk tools | Experimental energy threshold is not a validated classifier; transient noise can trigger it |
| Filesystem escape | Relative resolved paths, symlink check, atomic replacement | TOCTOU symlink race still possible under malicious concurrent local process |
| Script reads network/OS files | Script execution off by default; explicit preview and approval | Trusted scripts still have user OS privileges; `python -I` is NOT a security sandbox |
| Android package / input injection | Strict package and ASCII validation, device selection, subprocess argv not shell=True | Authorized ADB access is powerful; platform-specific shell parsing and Android behavior must be verified on real device |
| Concurrent / repeated action | One-use plan; asyncio single-writer; stop between steps | Direct GUI calls can have irreversible results before stop |
| Cloud exposure | Never binds beyond localhost; no automatic remote pairing | Local device or browser compromise is out of scope |
| Secrets | API key from environment; not committed; subprocess environment allowlist | Optional LLM transmits user prompt data to its provider; avoid sending sensitive commands |

**Blocking production gaps:** consent UX testing, real-device negative tests, Android native implementation, OS sandbox, auditable trace, calibrated acoustic model, anti-replay pairing, app-specific policy, accessibility/privacy compliance. No "100% safe" claim is warranted from source tests alone.
