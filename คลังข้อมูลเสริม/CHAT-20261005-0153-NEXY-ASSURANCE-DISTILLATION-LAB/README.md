# NEXY Assurance Distillation Lab

**Classification:** AI-PROPOSED auxiliary research/reference project. This is not canonical NEXY architecture and is not integrated into the NEXY.AI implementation repository.

This lab turns five recurring assurance problems into deterministic, bounded, standalone tools:

1. **Counterexample Distiller (CED)** — shrinks a failing JSON case while preserving declared failure predicates and protected JSON Pointer paths.
2. **Minimal Unsat Constraint Core Finder (MUCF)** — identifies a smallest conflicting constraint set over an explicitly supplied finite candidate universe.
3. **Evidence Freshness Revalidation Planner (EFRP)** — detects evidence invalidated by TTL, version drift, future timestamps, or stale upstream evidence and produces deterministic revalidation order.
4. **Spec Example Conformance Linter (SECL)** — checks whether machine-readable examples contradict declared rules.
5. **Verified Recovery Path Planner (VRPP)** — finds a shortest evidence-gated path from an unsafe/frozen FSM state to a declared safe state without executing the transitions.

## Why it fits NEXY
The source context describes NEXY as verify-first, freeze-on-insufficient-proof, deterministic where relevant, authority-preserving, and provenance-aware. These tools do not replace CORE/JUDGE/LAW. They produce bounded analysis artifacts that a future authorized NEXY adapter could consume.

## Run
Python 3.11+ and the standard library are sufficient.

\`\`\`sh
PYTHONPATH=src python3 tests/test_published_package.py
python3 -m compileall -q src tests
PYTHONPATH=src python3 -m nexy_aqt.cli unsat-core examples/unsat.json
\`\`\`

## Evidence
- Original modular regression suite: 24/24 PASS.
- Exact publish-layout conformance suite: 21/21 PASS.
- Source blobs are content-addressed and matched against the local tested files before commit.
- NEXY runtime integration: NOT_VERIFIED and intentionally out of scope.

## Scope
Only this folder in AI-CONTEXT is writable for this mission. No repository whose name contains \`NEXY.AI\` is modified.
