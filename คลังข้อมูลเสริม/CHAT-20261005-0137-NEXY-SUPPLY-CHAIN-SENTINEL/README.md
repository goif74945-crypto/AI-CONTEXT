# NEXY Supply-Chain Sentinel (NSCS)

Status: reference implementation / supplemental research.
Authority: advisory only. It does not override NEXY.AI specifications.
Work ID: `CHAT-20261005-0137-NEXY-SUPPLY-CHAIN-SENTINEL`.

A deterministic, fail-closed local dependency inventory and drift verifier designed to be compatible with NEXY.AI's zero-guess/evidence-first control philosophy.

## Commands

```bash
python -m nexy_supply_chain_sentinel snapshot --input package-lock.json --output snapshot.json
python -m nexy_supply_chain_sentinel diff --baseline approved.json --candidate candidate.json
python -m nexy_supply_chain_sentinel verify --baseline approved.json --input package-lock.json
```

Set `PYTHONPATH=src` when running directly from this folder.

## Decision semantics
- `ALLOW`: all required evidence is valid and policy permits every observed state/drift.
- `FREEZE`: evidence is malformed/incomplete/unsupported, snapshot integrity fails, or policy rejects any observed state/drift.

See `docs/DESIGN.md` and `evidence/VERIFICATION.md`.
