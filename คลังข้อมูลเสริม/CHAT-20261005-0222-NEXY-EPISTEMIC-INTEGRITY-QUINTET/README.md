# NEXY Epistemic Integrity Quintet

**Trace:** `CHAT-20261005-0222-NEXY-EPISTEMIC-INTEGRITY-QUINTET`
**Classification:** AI-PROPOSED / Lo4 / SUPPLEMENTAL / NOT CANON
**Protected scope:** no repository whose name contains `NEXY.AI` is modified by this work.

## Five systems
1. ECOF — Epistemic Circularity Firewall
2. DMAG — Decision Monotonicity Auditor
3. PDZA — Policy Dead-Zone Analyzer
4. RKM — Refutation Knowledge Memory
5. ACE — Assumption Closure Engine

The package strengthens epistemic integrity around a deterministic control hub without claiming authority. `AdvisoryIntegrityGate` can only emit advisory READY/FREEZE and never bypasses NEXY authority, verification or JUDGE layers.

## Reproduce
Requires Python 3.11+ and no third-party runtime dependencies.

```bash
python run_all_tests.py
PYTHONHASHSEED=1 python -m unittest discover -s tests -v
PYTHONHASHSEED=777 python -m unittest discover -s tests -v
```

Final local state before persistence:
- compileall PASS;
- 37/37 tests PASS;
- both hash-seed regressions PASS;
- 500 deterministic property iterations embedded;
- targeted secret-pattern scan 0 findings.

## Evidence boundary
E1/E2 local reference evidence only. NEXY integration/runtime/deployment remains NOT_VERIFIED.

Platform immutable ChatGPT conversation ID is not exposed by the available tool surface. The trace above is a project identifier, not an invented platform ID.
