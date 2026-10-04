# NCIF Local Validation Report

**Scope:** standalone local reference artifact only
**Environment:** Python 3.13.5 (recorded by verification receipt)
**Status:** PASS for the bounded E1/E2/local checks listed below; NEXY integration NOT_VERIFIED

## Executed checks

- Test-first RED was observed before production implementation: missing `ncif.engine` / `ncif.cli` caused expected failures.
- Unit/adversarial suite: **28/28 PASS** on the latest tested local source.
- Bounded deterministic audit: **6,561 cases / 0 assertion failures**.
- Structural stress audit: **PASS**, including deep lineage of 5,000 nodes and a 5,000-vote / 500-root wide graph.
- Python `compileall`: PASS.
- JSON fixture/schema parsing: PASS.
- CLI independent consensus: exit 0 / candidate.
- CLI correlated pseudo-consensus: expected exit 2 / freeze.
- One-command verification receipt: `evidence/verification.json`, overall PASS, 7 checks.

## Defects found and repaired during review

### D1 — recursive lineage traversal

A 1,500-node adversarial lineage produced a real `RecursionError` after the fixture was arranged to defeat cache-order masking.

Repair: replaced recursive ancestry propagation with deterministic iterative topological processing. Focused failure reproduced before repair, then passed after repair. Regression suite and bounded audit were rerun.

### D2 — raw provenance metadata in diagnostics

A leakage test proved result serialization contained raw `source_identity` / `correlation_keys`.

Repair: introduced domain-separated SHA-256 equality tokens for those fields in diagnostics. The failing test then passed; regression and bounded audits were rerun.

## Tooling limitations

`ruff`, `mypy`, and `pyright` were not located in the local PATH and were **not run**. The artifact intentionally uses Python standard library only, but absence of those tools is not evidence that lint/type checks would pass.

## Claim boundary

These results demonstrate bounded behavior of this standalone implementation. They do not prove:

- correctness of external provenance assertions;
- NEXY.AI integration;
- production performance/security;
- runtime/deployment readiness;
- detection of undeclared hidden common causes.
