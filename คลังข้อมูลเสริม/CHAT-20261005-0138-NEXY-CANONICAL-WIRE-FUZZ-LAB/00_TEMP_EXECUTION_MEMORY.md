# Temporary Execution Memory — Canonical Wire & Boundary Fuzz Lab

Status: ACTIVE CHECKPOINT
Internal chat/work reference: `CHAT-20261005-0138-GPT56SOL-NCWFL-01`
Platform conversation ID: UNKNOWN / not exposed to the available tools
Target repository: `goif74945-crypto/AI-CONTEXT`
Authorized path: `คลังข้อมูลเสริม/CHAT-20261005-0138-NEXY-CANONICAL-WIRE-FUZZ-LAB/`
Protected repository class: any repository whose name contains `NEXY.AI`

## Current objective
Create an additive-only advisory lab that explores deterministic canonical serialization and hostile boundary parsing for possible future NEXY.AI integration, without changing any NEXY.AI repository.

## Locked decisions
- This lab is AI-PROPOSED / ADVISORY, never current NEXY law.
- Core reference implementation is pure and has no clock/RNG/network/filesystem/env/process I/O.
- Accepted semantic values: null, bool, signed i128 integer, NFC UTF-8 string, list, string-keyed map.
- Float/NaN/Infinity/non-NFC/lone-surrogate/duplicate-key/overflow/unknown-type inputs fail closed.
- Canonical map ordering is lexicographic UTF-8 byte order of NFC keys.
- Integer wire encoding is exactly 16-byte signed big-endian two's complement.
- Wire version marker is `NCW1`.
- Decoder rejects non-canonical map ordering and trailing bytes.
- Strict JSON parser detects exact duplicate keys and NFC-equivalent key collisions before conversion to dict semantics.
- Resource limits are explicit policy values and include raw JSON text size before parsing.

## Verification checkpoints
- Initial implementation: 29/29 unittest cases PASS.
- Re-audit found tuple/list type-collapse and raw JSON pre-parse size gap.
- Repair applied: tuple rejected; max_json_text_bytes added.
- Expanded verification: 35/35 PASS.
- Golden vectors + exhaustive small-domain tests added.
- Current local verification: 39/39 PASS.
- Python compileall: PASS.

## Next actions
1. Persist docs + code + tests + evidence into isolated AI-CONTEXT folder.
2. Use atomic Git data commit to avoid partial multi-file state.
3. Re-fetch committed files and compare SHA-256 against local manifest.
4. Record implementation commit and verification seal.
5. Final audit protected-scope mutation: must remain zero NEXY.AI writes.

## Resume rule
If another model resumes, do not redesign the wire format silently. Any change to tags, integer representation, ordering, normalization, limits, or hash-domain semantics is a versioned proposal requiring new golden vectors and full regression execution.
