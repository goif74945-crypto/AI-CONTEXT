# Verification Evidence

Date: 2026-10-05 (+07 context)
Target: standalone local build intended for `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-PROVIDER-WIRE-CONTRACT-LAB`

## Evidence E1 — static compilation
Command:

```bash
python -m compileall -q src tests
```

Observed: `COMPILEALL_OK`
Status: **PASS (E1)**

## Evidence E2 — unit + negative + deterministic fuzz tests
Command:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Observed after repair loop:
- 18 tests executed
- 18 passed
- 0 failures
- 0 errors

Covered classes:
- canonical JSON key-order stability;
- deep defensive payload immutability;
- invalid identifier rejection;
- non-finite numeric rejection;
- deterministic transcript hash;
- valid text stream;
- valid tool roundtrip;
- 500 deterministic sequence-corruption trials;
- 300 deterministic random tool-fragment trials;
- empty transcript freeze;
- missing open freeze;
- sequence-gap freeze;
- event-after-close freeze;
- open-message-at-close freeze;
- malformed tool JSON freeze;
- tool-result direction mismatch freeze;
- refusal terminal-order freeze;
- unclosed stream freeze.

Status: **PASS (E2)**

## Failure/repair evidence
Initial run: 17/17 tests passed, but review identified two uncovered correctness defects:
1. empty transcript raised a generic `ValueError` rather than a typed freeze;
2. payload immutability was shallow, allowing nested post-construction mutation to change semantic fingerprints.

Repairs:
- empty transcript now raises `WireContractError("EMPTY_TRANSCRIPT", ...)` and the boundary converts it to `frozen=True`;
- payloads are recursively frozen and thawed only for canonical serialization;
- regression tests were added for both defects.

Re-verification: 18/18 tests passed.

## Deterministic replay smoke
A five-event Unicode/Thai text transcript was accepted and produced:

`df588c5bd0a7cfd47019e435b1ad7c8f3918969126a95a7b3dc0d11d54caa6b1`

This proves deterministic behavior for that exact local transcript only.

## Evidence boundaries
PASS does **not** establish:
- compatibility with any live provider;
- official OpenAI/Anthropic/Google API conformance;
- integration with live NEXY runtime;
- deployment readiness;
- performance/SLO claims.

Those remain **NOT_VERIFIED** until provider-specific adapters and integration/runtime evidence exist.

## Verification-harness repair
During final evidence capture, two smoke-harness mistakes were exposed after the 18 unit tests had already passed: (1) an import of a non-public helper name (`transcript_hash`), and (2) an outdated constructor keyword (`seq`) instead of the public `CanonicalEvent(sequence=..., event_type=..., source=...)` contract. The verifier was corrected to use only the public API and the whole final sequence was rerun. These were verifier defects, not library behavior failures, and they ire intentionally preserved in this evidence narrative rather than hidden.

## Durable raw evidence artifacts
- `TEST_RUN.txt` contains the final executed unit/regression/static/smoke commands and observed output.
- `FILE_MANIFEST.sha256` hashes every project file except the manifest itself at manifest-generation time.

## Repository persistence/read-back evidence
The exact 24-file tested baseline was written to `goif74945-crypto/AI-CONTEXT` at commit:
`a0f719abd9c85d1cf19ba5ab107d502940e40b30`

GitHub read-back of that commit established:
- expected project blobs: 24;
- committed project blobs: 24;
- missing: 0;
- blob SHA mismatches: 0;
- extras: 0;
- commit changed paths outside `คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-PROVIDER-WIRE-CONTRACT-LAB/`: 0.

This proves the persisted baseline matched the exact blobs assembled from the locally verified artifact. It does not elevate provider/runtime compatibility beyond the limitations already stated above.
