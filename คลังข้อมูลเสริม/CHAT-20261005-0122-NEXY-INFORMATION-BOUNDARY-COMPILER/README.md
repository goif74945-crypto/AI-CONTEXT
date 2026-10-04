# NEXY Information Boundary Compiler (NIBC) — Supplemental R&D Package

Status: AI-PROPOSED / SUPPLEMENTAL / REFERENCE PROTOTYPE

Execution code: `CHAT-20261005-0122-NEXY-INFORMATION-BOUNDARY-COMPILER`

Platform-native ChatGPT conversation ID: `UNKNOWN / NOT EXPOSED BY AVAILABLE TOOLS`

## Purpose

NIBC explores a deterministic, fail-closed information-flow policy compiler for NEXY-oriented R&D. It evaluates explicit policy + request inputs and returns one controlled outcome: `ALLOW`, `DENY`, or `FREEZE`.

The reference package covers information boundaries across core, agents/tools, external models, durable memory/vault, export/share, retention, minimization, provenance, and deletion obligations.

This is an AI-proposed supplemental concept. It is not promoted into canonical NEXY requirements, and it is not evidence that NEXY.AI currently implements these controls.

## Exact tested package

The exact locally validated 22-file package is stored as:

- `NIBC-REFERENCE-PACK.tar.gz`
- byte length: `26121`
- SHA-256: `504ab478cf517ebff014890d97b5e39d822df227255729ec39be13e11f7389a1`
- archive member count: `22`

Extract after cloning AI-CONTEXT:

```bash
mkdir NIBC-REFERENCE-PACK
tar -xzf NIBC-REFERENCE-PACK.tar.gz -C NIBC-REFERENCE-PACK
cd NIBC-REFERENCE-PACK
python -m pip install -r requirements-dev.txt
python tools/validate.py
```

## Local validation snapshot

The package-local validator recorded:

- Python `3.13.5`
- jsonschema `4.26.0`
- coverage `7.13.3`
- 41 unit/adversarial tests: PASS
- Draft 2020-12 schema checks: PASS
- Python AST checks: PASS
- `src/nibc.py` branch coverage: `99.451%` against a project-local `98%` gate
- critical content SHA-256 values recorded in `execution-evidence.json`

Coverage is reachability evidence, not correctness proof.

## Evidence boundary

Proven for the standalone reference prototype:
- E0 presence after repository read-back
- E1 syntax / JSON / schema checks from the exact archived package
- E2 executed unit/adversarial behavior from the exact archived package

Not proven:
- NEXY.AI integration (E3)
- user-flow behavior (E4)
- production/runtime behavior (E5)
- deployment (E6)
- legal/privacy compliance
- real-provider deletion completeness

## Mutation boundary

This package is published only under `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/`.

No repository whose name contains `NEXY.AI` is an authorized mutation target for this publication.
