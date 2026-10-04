# Remote Index — NEXY Operator Contract Compiler

Work ID: `CHAT-20261005-0121-NEXY-OPERATOR-CONTRACT-COMPILER`
Classification: **AI_PROPOSAL / supplemental reference implementation / NOT current NEXY.AI runtime truth**

## Remote payload
`NOCC_FULL_SOURCE.tar.gz` is the exact verified source bundle produced by this execution.

Bundle SHA-256:
`920e3fcd795e75ac320bc05299d2873a42fac925a60d4100c10810b77ad00141`

Git blob SHA:
`9dc73896c5533b46a9b5fe6f433922d30212f858`

The Git blob SHA was independently reproduced locally with `git hash-object` before publication.

## Bundle contents
The archive contains 30 regular files, including:
- complete Python reference implementation under `src/nexy_operator_contract/`;
- unit, negative-path, permission, determinism and matrix tests;
- input/output schemas;
- four reproducible fixtures;
- policy matrix generator;
- generated 120-scenario policy matrix;
- evidence record;
- architecture specification;
- policy model;
- requirement/evidence ledger;
- adoption plan;
- 10 explicitly marked AI-proposed future-system ideas;
- final audit;
- SHA-256 manifest.

## Verification observed before publication
- Python 3.13.5
- `python -m compileall -q src tests tools` -> PASS
- `PYTHONPATH=src python -m unittest discover -s tests -v` -> 36/36 PASS
- `PYTHONPATH=src python tests/test_matrix.py -v` -> 12/12 PASS
- JSON parse validation -> PASS
- policy matrix -> 120 scenarios
- matrix semantic digest -> `18582b915709a4a30f1955b063456b341c5a197f14828494dd0d5ff04111022c`

Evidence level is E1/E2 only. NEXY.AI integration/runtime/browser/deployment is **NOT_VERIFIED / NOT_PERFORMED**.

## Extract
```bash
mkdir nocc && tar -xzf NOCC_FULL_SOURCE.tar.gz -C nocc
cd nocc
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Authority boundary
This work does not modify or redefine any NEXY.AI authoritative specification. Adoption requires explicit future spec promotion and higher-layer integration evidence.

## Protected-scope statement
No repository whose name contains `NEXY.AI` was intentionally mutated by this execution. All writes were directed only to `goif74945-crypto/AI-CONTEXT` under this isolated supplemental namespace.
