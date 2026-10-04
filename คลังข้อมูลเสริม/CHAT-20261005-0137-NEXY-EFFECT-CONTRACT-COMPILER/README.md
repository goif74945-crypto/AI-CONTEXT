# NEXY Effect Contract Compiler (NECC)

**Classification:** AI-PROPOSED / RESEARCH PROTOTYPE / NOT NEXY CANON / NOT INTEGRATED INTO NEXY

**Work tag:** `CHAT-20261005-0137-NEXY-EFFECT-CONTRACT-COMPILER`

NECC is a standalone executable research prototype that compiles proposed consequential side effects into deterministic, inspectable effect contracts before execution.

## What was built
- deterministic contract canonicalization + identity;
- source-qualified preconditions/postconditions;
- R0-R5 reversibility law;
- compensation/reconciliation requirements;
- confirmation/irreversible gates;
- `UNKNOWN_SIDE_EFFECT` after dispatch timeout;
- no blind redispatch after ambiguous outcome;
- deterministic dependency-safe plans;
- tamper-evident receipt ledger;
- strict JSON wire boundary + CLI;
- deeply detached/frozen compiled metadata.

## Exact verified tree
The complete locally verified project tree (Design + Code + Tests + Evidence + raw logs) is encoded at:

`bundle/necc_project_bundle.tar.gz.base64`

Decode with:

`base64 -d necc_project_bundle.tar.gz.base64 > necc_project_bundle.tar.gz`

Decoded tar.gz SHA-256:

`dd514ccf27f9302c286e62a4d5a185210add0a92f8b7b606a859c497e8067a6d`

Base64 text Git blob SHA-1:

`5a8bd4b4bb11606cff33b3992345218eb273a397`

The base64 file was read back from `main` and matched the staged exact base64 text byte-for-byte.

## Verification snapshot
Fresh local verification at `2026-10-05T01:54:20+07:00`:
- Python 3.13.5
- 56 / 56 tests PASS
- forced compileall PASS
- deterministic source CLI PASS
- wheel build PASS
- clean venv wheel install/import PASS
- installed-wheel CLI equals source CLI byte-for-byte

Wheel SHA-256:

`b670649dbb6e3851c46eabe162552001f4f1b853e498e4e95041f27132dc6440`

## Protected-scope result
No repository whose name contains `NEXY.AI` was mutated. Any future integration requires a separate explicit integration decision and fresh verification against the then-current NEXY implementation/spec.
