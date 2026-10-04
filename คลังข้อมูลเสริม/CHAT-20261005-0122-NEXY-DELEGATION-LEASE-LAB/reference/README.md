# NEXY::LEASE reference prototype

Status: AI-PROPOSED / REFERENCE-ONLY / NOT CANONICAL / NOT PRODUCTION

This package models a deterministic, fail-closed authority lease bound to a concrete action plan fingerprint.

Core properties:
- no system clock reads in the policy engine; callers supply a logical tick;
- no randomness in policy decisions;
- plan drift blocks execution;
- resource/verb/effect/budget overreach blocks execution;
- high-impact effects require an explicit second gate;
- child leases can only narrow authority;
- novel child wildcard scopes are rejected when subset proof is not trivial;
- decision and state mutation are separate operations;
- optional append-only hash-chain journal provides tamper-evident sequencing for prototype evidence.

Run tests:

```bash
cd reference
PYTHONPATH=src python -m unittest discover -s tests -v
```

Static compile:

```bash
cd reference
PYTHONPATH=src python -m compileall -q src tests examples
```
