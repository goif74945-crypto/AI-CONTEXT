# NEXY Minimum-Disclosure Privacy Compiler Lab (NMDPC)

**Status:** AI-PROPOSED-CONCEPT / reference implementation only  
**NEXY current-build authority:** NONE  
**NEXY.AI implementation status:** NOT_VERIFIED / NOT_MODIFIED

NMDPC is a supplemental R&D project for a deterministic privacy preflight layer. Its job is to compile a task's declared purpose, recipient trust, requested capability, data classification, consent, and retention into a minimal disclosure plan before any payload is sent to another model or processor.

Core output is exactly one of:

- `ALLOW` — required fields may be disclosed as planned;
- `TRANSFORM` — required fields must be masked/tokenized before disclosure;
- `FREEZE` — a material privacy precondition is unresolved or forbidden.

## Why this exists

NEXY's current context already establishes zero-guess, verify-only release, human authority, private-by-default direction, server-side secrets, and data minimization at external-service boundaries. This lab explores one concrete mechanism for enforcing those principles without changing NEXY's current build specification.

## Scope lock

This project exists only under `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/...`.
It does not modify any repository whose name contains `NEXY.AI` and does not promote itself into the 837-row current normalized build matrix.

## Prototype

The Python reference engine is standard-library only. It separates policy metadata from payload values, canonicalizes plans, produces a stable SHA-256 policy fingerprint, never places raw payload values in the plan, and refuses to build a disclosure bundle from a frozen plan.

Run:

```bash
PYTHONPATH=src python validate.py
```

## Evidence boundary

- E0: artifact presence after commit/re-fetch.
- E1: Python compile + JSON fixture parse.
- E2: executed unit/invariant tests for this isolated prototype.
- E3-E6: NOT VERIFIED. No claim is made about NEXY integration, end-to-end UX, runtime enforcement, or deployment.
