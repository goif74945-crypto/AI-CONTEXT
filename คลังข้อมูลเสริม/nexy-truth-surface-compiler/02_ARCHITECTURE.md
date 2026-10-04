# Architecture

## Classification
**AI-PROPOSED REFERENCE ARCHITECTURE / ADVISORY ONLY**

## Pipeline

```text
Claim Envelope
   ↓ validate identity / status / materiality / visibility
Normalize + canonical order
   ↓
Truth Gate
   ├─ material UNKNOWN / CONFLICT / NOT_VERIFIED → blocker
   ├─ material FACT without evidence ref → blocker
   └─ unknown status → blocker (fail closed)
   ↓
Visibility Gate
   ├─ PUBLIC → eligible for surface
   ├─ INTERNAL → excluded from public projection; covered indirectly by input receipt
   └─ SENSITIVE → excluded from public projection; covered indirectly by input receipt
   ↓
Redaction Pass (defense in depth, not a DLP guarantee)
   ↓
Result Capsule
   ├─ decision: RELEASE | FREEZE
   ├─ public facts
   ├─ public uncertainties
   ├─ freeze reasons
   ├─ deduplicated evidence refs
   └─ deterministic input/output SHA-256 receipt
```

## Authority
NXTS is deliberately **non-authoritative**. It receives classifications from upstream. It does not decide whether a source is genuinely authoritative or whether a runtime test actually passed.

## Determinism
- claim order normalized by claim ID;
- evidence refs deduplicated and sorted;
- JSON serialized with sorted keys and fixed separators;
- no timestamps/randomness in compiled output;
- output receipt hashes the capsule before adding `output_sha256`.

## Failure behavior
- malformed envelope: compilation error, CLI exit 64;
- unknown status value: valid envelope but release freezes;
- material truth gap: release freezes;
- non-material inference/assumption: may be surfaced as uncertainty without blocking;
- sensitive/internal text: omitted from public facts/uncertainties.

## Security boundary
The compiler uses allowlisted output fields rather than serializing the original payload. Pattern redaction is defense in depth only. A production design would require a separately verified secret classifier/DLP layer.
