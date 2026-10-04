# NEXY Context Release Firewall Lab

**Status:** reference lab implemented and locally verified; NEXY.AI integration NOT_VERIFIED.

**Classification:** AI_PROPOSED_CONCEPT. This folder is supplemental research and executable reference material. It is not Canon, not DOC-C, and not evidence that NEXY.AI already implements these mechanisms.

Session code: `CHAT-20261005-0122-NEXY-CONTEXT-RELEASE-FIREWALL`

## Why this exists
NEXY's multi-model design needs useful context to cross provider/agent boundaries. AI-CONTEXT security law also requires that external services receive only the minimum context needed.

This lab turns that one-line security principle into an executable deterministic boundary:

```text
explicit context request
+ consumer policy
+ labeled/provenanced context
+ optional trusted declassification grant
=
RELEASED minimal payload + privacy-safe receipt
OR
FROZEN + privacy-safe receipt
```

No LLM decides the release.

## What is implemented
- sensitivity lattice and policy ceiling;
- purpose binding;
- compartments;
- required vs optional context;
- atomic fail-closed release;
- field expiry;
- derived-data sensitivity/compartment/purpose taint checks;
- cycle/unknown-source detection;
- trusted canonical grant digests;
- deterministic canonical JSON + SHA-256 fingerprints;
- privacy-safe receipts without blocked values;
- adversarial fixture catalog;
- unit/adversarial tests;
- validation script.

## Run locally
Requires Python 3.11+ and no third-party packages.

```bash
python -m compileall -q src tests scripts
python scripts/validate_lab.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Folder map
- `00_SESSION_MEMORY.md` — resumable execution checkpoint.
- `01_TASK_CONTRACT.md` — scope/authority/evidence lock.
- `02_ARCHITECTURE.md` — system architecture and semantics.
- `03_PRIVACY_CONTRACT.md` — invariant set.
- `04_ADOPTION_AND_RESEARCH.md` — promotion gates and future work.
- `schemas/context_release.schema.json` — machine-readable interchange shape.
- `src/nexy_crf/` — reference engine.
- `fixtures/adversarial_cases.json` — adversarial/failure catalog.
- `tests/test_firewall.py` — executable E2 evidence source.
- `scripts/validate_lab.py` — local structural validator.
- `examples/minimal_release.py` — minimal executable example.
- `05_VERIFICATION_REPORT.md` — generated after verification loop.
- `99_FINAL_AUDIT.md` — final scope/evidence audit.

## Important limitations
This does **not** provide:
- automatic secret classification;
- production cryptographic identity/signatures;
- endpoint/provider retention guarantees;
- encrypted transport;
- semantic proof that selected context is sufficient for a task;
- live NEXY integration/deployment proof.

Those claims remain NOT_VERIFIED / out of scope.
