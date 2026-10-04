# NEXY ProofGraph Lab — Design

> **AI-PROPOSED / EXPERIMENTAL / NOT CANON**

## Objective

Add a model-independent preflight layer for AI-CONTEXT so future AI sessions can detect stale authority bindings, denominator drift, broken references, proposal/canon confusion, and likely downstream impact before using context for NEXY work.

## Authority

The tool is subordinate to the AI-CONTEXT Execution Kernel and NEXY project authority. It reads policy values from an explicit JSON policy. It is not itself a canonical source of NEXY requirements.

## Architecture

```text
FILESYSTEM CORPUS
   ↓
documents.py  → normalized UTF-8 documents + SHA-256
   ↓
   ├── graph.py     → local Markdown dependency edges → reverse impact closure
   ├── rules.py     → deterministic findings PG001..PG007
   └── lockfile.py  → truth-lock manifest / stale-authority verification
   ↓
cli.py → scan / graph / impact / lock / verify-lock
```

## Invariants

1. No network dependency.
2. No arbitrary code execution while scanning.
3. No mutation of scanned files.
4. Credential findings never echo the candidate token.
5. Truth-lock paths cannot escape the selected root.
6. Current NEXY denominators come from policy, not hidden code constants in rules.
7. `215` is permitted when explicitly historical/deprecated/provenance context is present and rejected when framed as current truth.
8. A clean scan is never reported as proof of implementation/runtime/deployment correctness.

## Failure model

- unreadable/non-UTF-8 text: skipped by corpus loader;
- oversized text: skipped by configured byte ceiling;
- invalid policy: fail closed via JSON/key/type error;
- invalid truth lock: verification fails;
- missing locked file: verification fails;
- changed locked file: verification fails with expected/observed hash;
- broken local Markdown target: ERROR;
- current-truth use of deprecated 215 count: CRITICAL;
- likely credential signature: CRITICAL with redacted fingerprint.

## Security boundary

The scanner treats file contents as data. It does not evaluate Markdown, execute code, load Python plugins, expand shell substitutions, or follow external URLs. This reduces prompt-injection and supply-chain exposure for the auxiliary analysis layer.

## Evidence model

- parser/rule behavior: E2 unit tests;
- CLI composition: E3-like local process integration test;
- repository insertion: E0 presence + exact commit SHA after write;
- whole NEXY behavior: explicitly NOT_VERIFIED by this project.
