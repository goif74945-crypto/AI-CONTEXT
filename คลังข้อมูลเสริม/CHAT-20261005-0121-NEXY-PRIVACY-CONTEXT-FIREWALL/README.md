# NEXY Privacy Context Firewall (PCF) Lab

> **Status:** `AI_PROPOSED_SUPPLEMENTAL_CONCEPT`
>
> This directory is an independent engineering reference. It is **not** proof that NEXY currently implements these behaviors, and it does not promote itself into canonical NEXY requirements.

## Purpose

NEXY is designed to coordinate multiple AI models, tools, project context, and a persistent Vault. That creates a hard boundary problem: useful context often contains substantially more information than a particular provider or tool needs.

PCF is a deterministic pre-egress compiler. Before a context package is sent to a provider/tool, PCF receives explicit policy metadata and returns exactly one of:

- `ALLOW`: a purpose-minimized payload plus bounded retention leases and an HMAC receipt; or
- `FREEZE`: no payload, explicit violation codes, and receipt-safe metadata only.

It deliberately does **not** infer privacy classification from raw content. Missing authority is a freeze condition, not an invitation to guess.

## Security model in one sentence

**Classify explicitly, minimize by declared purpose, enforce destination limits, deny unsafe egress, bound retention, and prove the decision without logging denied values.**

## Reference implementation

The implementation is dependency-free Python 3.11+ and lives under `src/nexy_pcf/`.

```text
Context Envelope + Destination Profile + Active Policy + HMAC Key
                         |
                         v
                compile_context(...)
                         |
            +------------+------------+
            |                         |
          ALLOW                     FREEZE
  minimized payload          payload = null
  retention leases           typed violations
  field decisions            safe field decisions
  HMAC receipt               optional HMAC receipt
```

## Run verification

```bash
PYTHONPATH=src python scripts/verify.py
```

## CLI

```bash
export NEXY_PCF_RECEIPT_KEY='replace-with-32-byte-or-longer-secret'
PYTHONPATH=src python -m nexy_pcf.cli \
  --envelope fixtures/envelope-allow.json \
  --destination fixtures/provider-alpha.json \
  --policy fixtures/policy.json
```

Exit codes:
- `0`: `ALLOW`
- `2`: `FREEZE` or input-load failure

## What this lab proves

The local verification suite can establish E1 static and E2 unit behavior for this isolated reference implementation. It cannot establish NEXY integration, production privacy, provider behavior, legal compliance, deployment safety, or live data handling.

## Files

- `02_ARCHITECTURE.md`: architecture and state semantics.
- `03_POLICY_AND_DATA_MODEL.md`: field, policy, destination, receipt contracts.
- `04_INTEGRATION_CONTRACT.md`: proposed NEXY integration boundary.
- `05_THREAT_MODEL.md`: abuse cases, controls, and residual risks.
- `06_AI_PROPOSED_FUTURE_IDEAS.md`: explicitly non-canonical extensions.
- `07_ACCEPTANCE_AND_TEST_MATRIX.md`: requirement-to-evidence mapping.
- `08_PERFORMANCE_AND_INVARIANTS.md`: determinism and complexity properties.
- `schemas/`: machine-readable structural contracts.
- `fixtures/`: non-production verification inputs.
- `tests/`: unit and CLI regression tests.
