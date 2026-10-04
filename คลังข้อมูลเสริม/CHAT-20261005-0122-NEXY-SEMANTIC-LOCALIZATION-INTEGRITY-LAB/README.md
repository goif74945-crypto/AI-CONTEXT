# NEXY Semantic Localization Integrity Lab

**Status:** `AI_PROPOSED_CONCEPT_NOT_ADOPTED`  
**Repository target:** `goif74945-crypto/AI-CONTEXT` only  
**Production NEXY.AI implementation:** `NOT_VERIFIED / NOT MODIFIED`

This lab is a deterministic reference gate for detecting high-risk semantic drift when authoritative or user-visible NEXY text is localized between English and Thai.

It does **not** claim to prove full translation correctness. It protects a narrower, testable set of invariants whose accidental translation drift can alter authority, safety, execution semantics, or user trust:

- numbers and percentages;
- semantic units such as milliseconds vs seconds;
- template placeholders;
- URLs and email addresses;
- hashes, UUIDs, backtick identifiers, UPPER_SNAKE identifiers;
- canonical NEXY state/role tokens such as `FREEZE`, `PASS`, `OWNER`, `RUN`;
- explicit protected literals supplied by a caller;
- normative modality classes: prohibition, obligation, permission, recommendation;
- negation polarity;
- supported-language boundary.

The output decision is intentionally binary: `PASS` or `FREEZE`. Any `BLOCK` issue produces `FREEZE`.

## Why this exists

NEXY's source-grounded principles require explicit authority, no silent guessing, visible failure, deterministic behavior, and one legal verified output or freeze. Localization is a place where seemingly harmless wording changes can silently weaken a prohibition, strengthen permission into obligation, change a timeout unit, mutate an identifier, or remove a freeze state. This lab tests whether a small deterministic gate can catch those classes of drift before localized text is treated as trustworthy.

## What this does not do

- no machine translation;
- no LLM semantic scoring;
- no claim of linguistic completeness;
- no production integration;
- no mutation of any repository whose name contains `NEXY.AI`;
- no adoption of this proposal into NEXY law;
- no unsupported language pair is treated as verified.

## Run

```bash
npm run check
node src/cli.js fixtures/pass-en-th.json
node src/cli.js fixtures/freeze-number-drift.json
```

Exit code from CLI:
- `0`: PASS
- `3`: FREEZE
- `2`: invalid CLI/input execution

## Evidence boundary

Local reference implementation can reach E0/E1/E2 evidence. It cannot establish NEXY production behavior, integration, deployment, or user impact without separate authorized work.
