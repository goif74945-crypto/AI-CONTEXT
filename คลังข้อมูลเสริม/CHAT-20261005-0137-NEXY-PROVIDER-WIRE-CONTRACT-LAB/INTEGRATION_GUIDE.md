# NEXY Integration Guide

Status: reference only. No NEXY.AI code was modified.

## Boundary ownership
- Provider adapter owns provider-specific parsing.
- `nexy_wire` owns canonical structural validity and transcript integrity.
- NEXY policy/JUDGE remains responsible for semantic authorization and release.

## Minimal integration pseudoflow

```text
raw provider event
  -> provider adapter
  -> CanonicalEvent[]
  -> WireBoundary.validate(transcript)
     -> accepted=false => FREEZE / preserve evidence
     -> accepted=true  => hand canonical transcript to existing NEXY verification path
```

## Required adapter conformance before production adoption
1. Pin provider API/SDK version.
2. Build fixtures from official provider documentation and captured test traffic.
3. Prove event-order mapping and tool-call reconstruction.
4. Prove refusal/error/timeout handling.
5. Prove usage normalization semantics or mark usage UNKNOWN.
6. Run malformed-event and truncated-stream tests.
7. Run provider-version drift canaries.
8. Record exact provider/model/version evidence.

Until those steps exist for a provider, compatibility is **NOT_VERIFIED**.
