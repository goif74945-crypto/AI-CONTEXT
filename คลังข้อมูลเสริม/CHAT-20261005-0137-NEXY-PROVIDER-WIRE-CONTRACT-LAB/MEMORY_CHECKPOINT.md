# Durable Memory / Continuation Checkpoint

## Current durable state
The standalone **NEXY Provider Wire Contract Lab** has been designed, implemented, tested, and persisted under `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-PROVIDER-WIRE-CONTRACT-LAB/`.

The exact 24-file tested implementation baseline was committed as:
`a0f719abd9c85d1cf19ba5ab107d502940e40b30`

Repository read-back at that commit verified:
- 24 expected files present;
- 0 missing files;
- 0 blob-SHA mismatches;
- 0 extra files in the project snapshot;
- all 24 changed paths were inside the authorized new project prefix.

## Verified implementation state
- Python 3.11 standard-library reference package implemented.
- Canonical provider event model and protocol version `nexy.wire.v1` implemented.
- Fail-closed stream state machine implemented.
- Deterministic event fingerprints and transcript hash chaining implemented.
- Deep defensive payload immutability implemented.
- Tool-call JSON reconstruction and direction checks implemented.
- 18/18 unit, negative-path, regression, and deterministic fuzz-style tests pass.
- `compileall` passes.
- SHA-256 file-manifest verification passes for every manifest-covered file.

## Distinctness rationale
Existing supplemental work inspected before creation covered capability negotiation, provider substitution safety, capability health routing, verification, semantics, and reliability. This lab isolates the lower-level provider event-stream/tool-call/error/usage wire contract those higher layers can depend on.

## Protected boundary
Do not write to any repository whose name contains `NEXY.AI`. Integration remains documentation/interface-only unless the user later provides a separate explicit authorization.

## Resume sequence
1. Read `TASK_CONTRACT.md`, `DESIGN.md`, and `EVIDENCE.md`.
2. Treat `a0f719abd9c85d1cf19ba5ab107d502940e40b30` as the exact tested implementation baseline.
3. Re-run `PYTHONPATH=src python -m unittest discover -s tests -v` before changing semantics.
4. Re-run `python -m compileall -q src tests` and `sha256sum -c FILE_MANIFEST.sha256` after changes.
5. If verification fails, fix the smallest root cause and rerun the complete evidence sequence.
6. Keep provider-specific adapters outside CORE and preserve fail-closed behavior.

## Remaining future work — not part of current completion claim
- official provider adapters pinned to current provider API/SDK versions;
- captured real provider fixtures and conformance suites;
- live NEXY runtime integration behind explicit authorization;
- performance/load characterization and operational SLO evidence.

These remain `NOT_VERIFIED` and must not be inferred from the reference implementation.
