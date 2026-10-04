# NEXY Active Truth Operations Quintet (ATOQ)

Status: AI_PROPOSED / EXPERIMENTAL / NOT_NEXY_CANON

Durable chat reference: CHAT-NEXY-ACTIVE-TRUTH-OPS-Q5-20261005-A
Platform-native chat ID: UNKNOWN_NOT_EXPOSED_BY_AVAILABLE_TOOLING

## Boundary
This project is stored only in goif74945-crypto/AI-CONTEXT under this namespace.
The implementation repository goif74945-crypto/NEXY.AI- was used READ-ONLY as compatibility evidence.
No claim in this project means NEXY.AI currently implements, runs, deploys, or endorses these systems.

## Five systems
1. AEAP — Active Evidence Acquisition Planner
   Plans the smallest lawful bounded set of evidence-producing probes needed to satisfy explicit evidence needs. It does not execute probes and never fabricates evidence.

2. RCTC — Runtime Contract Telemetry Compiler
   Compiles an externally APPROVED invariant and declared event schema into a deterministic pure monitor. Candidate invariants are blocked until authority promotion occurs outside this component.

3. IDW — Invariant Discovery Workbench
   Mines accepted/rejected scalar trace observations for descriptive candidate invariants, preserving support and counterexample trace IDs. Output is always CANDIDATE_ONLY.

4. CDPP — Causal Diagnostic Probe Planner
   Selects a deterministic bounded set of explicitly declared diagnostic probes whose predicted outcomes distinguish declared hypotheses. It never invents hypotheses, predictions, or a winning root cause.

5. CRG — Contract Retirement Gate
   Determines whether an obsolete contract/interface is only a RETIRE_CANDIDATE after consumer, usage-window, replacement, rollback, authority and freshness gates pass. It never deletes anything.

## Cross-system authority law
IDW cannot feed an enforceable rule directly to RCTC. An external authorized promotion record is mandatory.
AEAP and CDPP are planning systems, not executors.
CRG RETIRE_CANDIDATE is a decision artifact, not deletion authorization.
RCTC evaluation is pure and does not emit alarms or mutate NEXY state.

## Determinism and failure law
Equivalent canonical input yields the same structural result and SHA-256 fingerprint.
Malformed or materially insufficient input fails closed.
Library core performs no filesystem, network, database, subprocess, process-control, model or hidden I/O.

## Tested reference implementation
The exact source/tests/config bytes that passed local verification are stored as five base64 text parts under bundle/.
See 05_BUNDLE_MANIFEST.md for reconstruction and hashes.

## Verification summary
Environment: Node v22.16.0, npm 10.9.2, TypeScript 5.8.3, Python 3.13.5.
E1 strict TypeScript typecheck: PASS, zero diagnostics.
E1 static audit: PASS.
E2 unit/adversarial: 26/26 PASS.
E2 property/invariance: 5/5 PASS.
E3 integration: 2/2 PASS.
Full regression: 33/33 PASS, 0 fail, 0 skipped, 0 todo.

These are local E1/E2/E3 proofs for this standalone reference implementation only. They are not NEXY E4/E5/E6 runtime/deployment proof.
