# NEXY Canonical Wire & Boundary Fuzz Lab

**Status:** ADVISORY / AI-PROPOSED / ADDITIVE-ONLY / REFERENCE IMPLEMENTATION  
**Internal chat/work reference:** `CHAT-20261005-0138-GPT56SOL-NCWFL-01`  
**Platform chat ID:** UNKNOWN because the host does not expose it to the available tools.  
**Storage:** `goif74945-crypto/AI-CONTEXT` only.  
**NEXY.AI repository mutation:** FORBIDDEN and not required.

## Mission
Explore one narrow but high-leverage question for future NEXY work:

> Can a boundary turn supported semantic values into one unambiguous byte representation, while rejecting ambiguity and malformed inputs before they can enter an authority-bearing path?

The lab provides a deterministic reference codec (`NCW1`), strict JSON admission boundary, negative-path mutation corpus, golden vectors, and verification model. It is deliberately isolated from NEXY production source.

## Why this is distinct from neighboring labs
This work does **not** attempt to decide intent, calculate requirement blast radius, define authority, manage privacy, model partial execution, or produce user-facing trust UX. It focuses on the representation boundary underneath those systems:

`external representation -> strict admission -> canonical semantic domain -> canonical wire -> stable hash`

## Source-grounded motivation
`FACT_PROJECT` from AI-CONTEXT NEXY context:
- NEXY favors one legal verified output or freeze/silence rather than guessing.
- Determinism is a core design target.
- The locked source describes canonical binary WAL encoding with fixed schema/endian, length framing, and SHA-256.
- The locked source forbids floating point in Core and describes signed 128-bit canonical arithmetic.
- Replay/order behavior must not depend on incidental runtime ordering.
- Verification claims must be tied to the matching evidence class.

`PROPOSAL` in this lab:
- `NCW1` tags and exact byte layout.
- NFC-as-admission policy for strings.
- Strict JSON duplicate-key/NFC-collision rules.
- Default resource limits.
- Hash domain string.

Those proposals are **not current NEXY requirements** and must never override NEXY canonical source/spec.

## Current reference behavior
Supported semantic types:
- `null`
- `bool`
- signed 128-bit integer
- NFC Unicode string encoded as strict UTF-8
- list
- string-keyed map

Rejected:
- floats, NaN, Infinity;
- integers outside signed i128;
- non-NFC text;
- invalid Unicode scalar text / lone surrogates;
- tuple/bytes/custom object type collapse;
- non-string map keys;
- duplicate JSON keys;
- NFC-equivalent JSON key collisions;
- malformed/truncated/non-canonical wire;
- policy resource-limit violations.

## Verification snapshot
Local sandbox evidence before persistence:
- `python -m compileall`: PASS
- `python -m unittest discover`: **39/39 PASS**
- includes 720 map-order permutations
- includes locked golden vectors
- includes deterministic malformed-wire mutations
- includes exhaustive generated small-domain round-trip/idempotence cases
- includes static forbidden-I/O import scan over core modules

See `evidence/` and `FINAL_AUDIT.md` for exact evidence and limitations.
