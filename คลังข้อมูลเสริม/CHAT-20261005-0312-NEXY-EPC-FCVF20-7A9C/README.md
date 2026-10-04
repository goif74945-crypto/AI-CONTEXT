# NEXY EPC Formal Constitutional Verification Fabric 20 (FCVF-20)

**Status class:** Lo4 AI proposal / experimental / non-canonical / non-governing  
**Durable CHAT_ID:** `CHAT-20261005-0312-NEXY-EPC-FCVF20-7A9C`  
**Protected target:** `goif74945-crypto/NEXY.AI-` is read-only for this work.

FCVF-20 is a standalone reference verifier for the proposed **NEXY Evolutionary Proposal Court (EPC)**. It does not decide which proposal is "best" and it cannot promote anything. Its job is narrower and more hostile: model the court protocol as a deterministic finite-state system, try to drive it into constitutionally forbidden states, and emit reproducible counterexamples if a rule weakening makes a forbidden state reachable.

## Authority pins

- NEXY-IGNIS canonical source SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- NEXY implementation repository: `goif74945-crypto/NEXY.AI-`
- NEXY branch: `NEXY.ai`
- NEXY exact commit inspected: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- AI-CONTEXT is the only writable repository for this package.

The canonical source and current implementation both preserve authority separation: external/auxiliary layers may propose or assist, but protected state and final adjudication remain outside FCVF. Current NEXY code also uses signed Q64.64/fixed128 arithmetic on authoritative numeric paths. FCVF mirrors those constraints for its protocol-integrity metrics.

## What this package proves in its modeled scope

FCVF-20 enforces one KEEP and one CUT per `CHAT_ID`, keeps DEFER non-consuming, rejects CUT from WIP/insufficient-evidence states, rejects retrospective verdict rewrites, prevents promotion/Core/Canon authority escalation, constrains CUT to non-destructive dispositions, requires semantic duplicate witnesses, requires exact provenance closure for votes, uses canonical deterministic serialization, uses checked signed Q64.64 metrics, and explores a bounded reachable state space for invariant violations.

It also contains a constitutional regression differential: deliberately weaken a rule, then require the verifier to find and minimize a trace that is safe under the strict constitution but unsafe under the weakened one. A test suite that cannot catch an intentionally inserted defect is mostly a decorative green rectangle.

## Package layout

- `src/epc_fcvf/q64.py` — checked signed Q64.64 substrate.
- `src/epc_fcvf/model.py` — immutable EPC state/event/vote/evidence model.
- `src/epc_fcvf/engine.py` — strict constitutional transition function and weak-model knobs used only for regression proofs.
- `src/epc_fcvf/systems.py` — registry of exactly 20 constitutional verifier systems.
- `src/epc_fcvf/modelcheck.py` — bounded exhaustive explorer and minimal counterexample reducer.
- `src/epc_fcvf/regression.py` — strict-vs-weakened constitutional differential.
- `src/epc_fcvf/canonical.py` — deterministic canonical JSON and hashes; binary floats rejected.
- `src/epc_fcvf/fixtures.py` — exact pinned deterministic evidence fixtures.
- `src/epc_fcvf/cli.py` — reference end-to-end execution.
- `tests/` — unit, negative, formal-property, model-check and vote-contract tests.
- `evidence/` — captured execution evidence generated from exact tested bytes.

## Integration boundary

FCVF is intended to sit **before** any future NEXY promotion/adjudication boundary as a shadow verifier or CI/preflight component. Its only safe output is evidence such as `PASS`, `BLOCK`, `COUNTEREXAMPLE`, or an advisory witness. It has no API for changing NEXY Core state, Canon, JUDGE state, production state, branches, or repositories.

See `02_ARCHITECTURE_AND_20_SYSTEMS.md`, `04_NEXY_INTEGRATION_CONTRACT.md`, and `05_EPC_VOTE_PROTOCOL.md` for the full contracts.
