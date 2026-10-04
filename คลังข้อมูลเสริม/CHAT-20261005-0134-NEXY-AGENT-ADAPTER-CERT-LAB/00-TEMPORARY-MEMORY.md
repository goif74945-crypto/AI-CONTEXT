# Temporary Execution Memory / Resume Point

Session/work code: `CHAT-20261005-0134-NEXY-AGENT-ADAPTER-CERT-LAB`

## Objective
Build a unique, useful, executable NEXY-compatible supplemental project inside AI-CONTEXT only. Do not write NEXY.AI.

## Scope lock
- Writable: `AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0134-NEXY-AGENT-ADAPTER-CERT-LAB/**`
- Protected: every repository/path outside that project folder; especially any repository whose name contains `NEXY.AI`.

## Current design
Standalone AgentAdapter manifest validator + deterministic failure-semantics simulator + TypeScript mirror.

## Local verified state
- Python unit tests: 22/22 PASS.
- TypeScript strict typecheck: PASS.
- TypeScript assertions: 9/9 PASS.
- Cross-language parity: 10/10 scenarios identical.
- JSON Schema fixture expectations: 4/4 matched.
- CLI exit semantics: positive=0, negative validation=2.

## Known boundary
This is standalone preflight tooling. No NEXY.AI implementation/runtime/deployment claim is established. Real NEXY integration would require explicit authorization plus E3/E5/E6 evidence as applicable.

## Next action
Publish this folder only to `goif74945-crypto/AI-CONTEXT`, then fetch the remote folder/key files and verify upload integrity. Do not edit shared index files unless separately authorized/needed.
