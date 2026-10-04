from __future__ import annotations

from nexy_interchange import build_envelope, canonical_text, verify_envelope

payload = {
    "status": "FREEZE",
    "reason": "insufficient evidence",
    "requirements": ["R-17", "R-22"],
}

envelope = build_envelope(
    kind="nexy-decision",
    schema_version="1.0.0",
    payload=payload,
    provenance={"source": "example", "authority": "user-law"},
    observed_at="2026-10-05T01:42:00+07:00",
)

assert verify_envelope(envelope)
print(canonical_text(envelope))
