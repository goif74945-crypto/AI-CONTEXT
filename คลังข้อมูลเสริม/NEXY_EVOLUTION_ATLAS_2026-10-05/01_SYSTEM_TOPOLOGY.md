# 01 — System Topology Map

Evidence baseline: NEXY.AI- tree SHA `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.

## FACT: observed macro-surfaces
The repository contains at least these major surfaces: `apps/web`, `packages`, `packages-experimental`, `core-kernel`, `nexy-daemon`, `infra`, `prisma`, `vault`, `tests`, `scripts`, `docs`, `evidence`, CI workflows, Rust/Cargo configuration, and TypeScript/Next.js configuration.

The package manifest exposes verification/build commands including contract/integration/all tests, coverage, lint plus module-boundary checks, DOC-C checks, evidence sealing, Phase-F checks, backend/web/six-system typechecks, static determinism checks, canon-source seal checks, and web build.

README describes a layered architecture involving deterministic reasoning, Lo3 swarm governance, decision synthesis, risk/safety evaluation, execution control, immutable safety kernel, Lo2/USL, deterministic game fabric, robotics, resilience, hardware attestation, and fail-closed FREEZE semantics.

## Architectural topology
1. **Human/API surface** — Next.js web/API routes expose controlled interaction, artifacts, directives, health, auth, freeze/recovery and related operations.
2. **Application/service boundary** — orchestration and policy adapters translate external requests into canonical domain operations.
3. **Canonical decision domain** — deterministic and consensus components produce candidates under explicit constraints.
4. **Authority/ledger domain** — append-only or sealed evidence/state mechanisms preserve authoritative history.
5. **Safety and containment domain** — freeze, sandbox, resource, hardware, and physical safety gates constrain execution.
6. **Experimental domain** — Phase-F / packages-experimental contains capabilities that must not be silently promoted into canonical authority.
7. **Verification domain** — tests, scripts, CI, evidence, and exact-head workflows form a separate proof plane.

## Key insight
NEXY should be reasoned about as **two coupled graphs**, not one codebase:
- Execution Graph: what can cause state/action.
- Proof Graph: what can prove that execution was admissible and correct.

A component may exist in the Execution Graph without having sufficient Proof Graph coverage. That is a maturity gap, not proof of failure.

## UNKNOWN
This atlas does not claim all paths are exercised in production, that every documented subsystem is deployed, or that repository presence equals runtime activation.
