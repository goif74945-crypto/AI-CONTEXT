# NEXY Operator Experience Compiler (OXC) Lab

Status: **EXPERIMENTAL / AI-PROPOSED / NOT NEXY CANON**  
Work reference: `CHAT-20261005-0120-NEXY-OXC-LAB`  
Storage: `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม`  
Protected implementation repositories: every repository whose name contains `NEXY.AI` remains no-touch for this work.

## What this is

OXC is a deterministic reference layer that compiles authoritative Core state into an operator-facing presentation plan.

It is designed to solve a product problem without creating a second authority system:

> NEXY may be strict and internally complex, while the human-facing surface should expose only the amount of complexity necessary to act safely and understand truth.

OXC therefore consumes already-authoritative facts such as system state, truth status, backend action permission, role, allowed states and risk metadata. It may **narrow, explain, order and add confirmation friction**. It may never grant authority or rewrite truth.

## Why this is distinct from existing supplemental work

At the start of this session, the supplemental tree contained 350 entries and was dense in evidence engineering, verification, epistemic control, context integrity, counterfactual assurance, reliability, security and capacity economics.

A filename-level uniqueness scan found no dedicated supplemental pack centered on deterministic operator-experience compilation, adaptive disclosure and presentation-only preferences.

This is evidence of a useful gap, not proof that no semantically similar idea exists anywhere in all project prose.

## Core capabilities

1. **Truth-Preserving Surface Compilation** — mandatory state/truth signals are carried to the surface.
2. **Authority Narrowing** — backend, role, state, mode and truth constraints can only disable/hide actions, never promote denied actions.
3. **Risk/Friction Compilation** — risk and reversibility produce acknowledgement/confirmation requirements.
4. **Progressive Disclosure** — presentation detail adapts while critical states force sufficient diagnostics.
5. **Ephemeral Preference Envelope** — detail, density, language, motion and friendly tone are presentation-only.
6. **Fail-Closed Contract Boundary** — unsupported/invalid contract values are rejected rather than guessed.

## Reference implementation

See `reference/`.

The implementation is intentionally zero-dependency TypeScript and avoids clock, randomness, filesystem, network, environment and hidden I/O in the compiler core.

## Evidence summary

Local sandbox verification before Git publication:

- TypeScript 5.8.3: PASS
- Node.js v22.16.0 tests: 15/15 PASS
- 576-case policy matrix: backend-denied mutation never promoted to ENABLED
- 36 preference combinations: action authorization projection remained identical
- transferred Git blob IDs exactly matched local `git hash-object` values for all six source/config/test files

See `08_VALIDATION_REPORT.md` for exact evidence and limitations.
