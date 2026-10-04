# Validation Report

## Target
Standalone WOCF reference lab under `คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-WOCF`.

## Environment
- Python: `3.13.5`
- OS observed by sandbox: `Linux 6.18.44 x86_64, glibc 2.41`
- Core runtime dependencies: Python standard library only.

## Exact-byte binding
The Git blob SHA of each executable/test/fixture/schema artifact on branch `wocf-20261005-0137-finalize` was compared with the corresponding locally executed file. All nine verification-critical artifacts matched exactly.

Key blobs:
- `src/wocf.py`: `9a2f0438a7585309a482102974e2ab7a43abe575`
- `tests/test_wocf.py`: `b816ef2148619fa83f9c671861fbba6c3e1a1106`
- `scripts/run_verification.py`: `2cec576a94fa0d838ff87a003d670c844a4159d6`

## Executed verification

```bash
python scripts/run_verification.py
```

Latest observed verifier exit code: `0`.

| Gate | Evidence class | Result |
|---|---:|---|
| Python compile | E1 | PASS |
| JSON fixture/schema parse | E1 | PASS |
| Unit + adversarial suite | E2 | PASS, 18/18 |
| CLI admissible scenario | E2 | PASS, `ALLOW`, exit 0 |
| CLI duplicate/high-overlap scenario | E2 | PASS, `FREEZE`, exit 2 |
| Core dependency/dangerous-call AST audit | E1 | PASS |

The static core audit observed only Python standard-library import roots and no direct builtin dynamic execution calls or selected process/network calls.

## Covered negative paths
Protected repository target; duplicate workstream identity; namespace ancestor collision; write-path ancestor collision; active exclusive-resource collision; completed-workstream resource release; exact concept duplicate; high lexical overlap freeze; moderate overlap warning; read overlap non-blocking; namespace containment; dot traversal; malformed catalog; duplicate catalog ID; deterministic replay; catalog order invariance; CLI freeze semantics.

## Failure loop
The first verification cycle exposed one faulty moderate-overlap fixture. The algorithm was not weakened to satisfy the test. The fixture was corrected to exercise the designed threshold and the complete suite was rerun. See `evidence/failure-and-fix.md`.

## Claim boundary
This proves E1/E2 behavior for the exact byte-bound standalone implementation. It does not prove production NEXY integration, distributed atomic reservation, race-free scheduling, deployment reliability, or semantic novelty beyond deterministic lexical signals.
