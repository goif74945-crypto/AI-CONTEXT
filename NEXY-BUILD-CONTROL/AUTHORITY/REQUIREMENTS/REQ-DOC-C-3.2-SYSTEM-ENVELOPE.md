REQ_ID: REQ-DOC-C-3.2-SYSTEM-ENVELOPE
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_PAGE: UNKNOWN
SPEC_LINES: extracted paragraphs 9994-10012
SPEC_TEXT: Final DOC-C §3.2 SystemEnvelope<T> defines top-level status, state, timestamp, request_id, trace_id, correlation_id?, version, duration_ms?, data?, error?; error contains code, message, source, recoverable.
AUTHORITY_CLASS: DOC-C BUILD SPEC
EXPECTED_BEHAVIOR: Canonical SystemEnvelope schema/builder match that field set.
FORBIDDEN_BEHAVIOR: Canonical SystemEnvelope must not emit unsupported top-level extensions absent from final DOC-C.
AFFECTED_SYSTEMS: contracts; API wire envelope
DEPENDENCIES: DOC-C §3.1 core types
IMPLEMENTATION_PATHS: packages/contracts/envelope.ts
TEST_PATHS: tests/contract/envelope.test.ts
STATUS: MISMATCH
LAST_VERIFIED_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
