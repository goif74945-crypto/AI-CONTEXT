# Design — Canonical Provider Wire Boundary

## Purpose
Create a deterministic event contract between provider adapters and NEXY-facing orchestration so provider-specific streaming differences cannot silently alter CORE semantics.

## Non-goals
- This is not an official adapter for OpenAI, Anthropic, Google, or any other provider.
- It does not authorize model output.
- It does not replace NEXY::JUDGE, policy, safety, capability negotiation, or provider behavioral evaluation.
- It does not modify the NEXY.AI implementation repository.

## Architecture

`Provider SDK/API -> provider-specific adapter (future) -> CanonicalEvent -> StreamValidator -> TranscriptReplayer -> WireBoundary -> candidate input to NEXY orchestration`

The lab implements the canonical layer only.

## Canonical event language
- `stream.open`
- `message.start`
- `text.delta`
- `message.end`
- `tool.call.start`
- `tool.argument.delta`
- `tool.call.end`
- `tool.result`
- `usage`
- `refusal`
- `error`
- `stream.close`

## Key invariants
1. Sequence numbers start at zero and are contiguous.
2. `stream.open` is first and unique.
3. `stream.close` is final.
4. Stream identity cannot change after open.
5. Text deltas require an open message.
6. Tool argument fragments require a known open tool call.
7. Tool arguments must decode to a JSON object before tool-call completion is accepted.
8. Tool results travel `core_to_provider`; provider events travel `provider_to_core`.
9. Refusal/error enters terminal mode and must be followed immediately by close.
10. Open messages/tool calls block close.
11. Usage is optional but unique and non-negative when present.
12. Canonical JSON rejects non-finite numbers and non-JSON values.
13. Transcript fingerprints are deterministic and hash-chained.
14. Any contract violation freezes the boundary rather than guessing a repair.

## Failure model
A violation raises a typed `WireContractError` internally and becomes `BoundaryResult(accepted=False, frozen=True, error_code=...)` at the NEXY-facing boundary.

No auto-reordering, missing-event synthesis, best-effort JSON repair, or fallback parsing is allowed.

## Security/trust boundary
Raw provider events are untrusted input. Provider adapters must validate and translate externally. This package deliberately accepts only already-canonical events. Optional `raw_digest` supports provenance without persisting raw provider content.

## Integration shape
A future provider adapter should:
1. parse provider-native event;
2. validate provider-native required fields;
3. map to one or more `CanonicalEvent` objects;
4. include `raw_digest` of the sanitized/raw event when policy allows;
5. feed canonical events through `WireBoundary`;
6. expose only accepted transcripts downstream.

Provider adapters remain replaceable. CORE does not need vendor-specific event classes.

## Versioning
Protocol is currently `nexy.wire.v1`. Incompatible semantic changes require a new protocol version. Unknown protocol versions fail closed.
