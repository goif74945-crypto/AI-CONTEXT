# Requirement / Evidence Ledger

| ID | Requirement | Evidence target | Current local target |
|---|---|---|---|
| R01 | No Python float accepted authoritatively | E2 | `test_float_forbidden`, `test_float_api_freezes` |
| R02 | Exact decimal/rational parsing | E2 | `test_exact_decimal`, `test_rational_literal` |
| R03 | Exact dimensional unit conversion | E2 | conversion + all pair round-trip tests |
| R04 | Affine temperature conversion correct | E2 | Fahrenheit/Celsius tests |
| R05 | Uncertainty uses delta conversion only | E2 | temperature delta test |
| R06 | Cross-dimension/unknown units freeze | E2 | negative unit tests |
| R07 | Inclusive/exclusive bounds deterministic | E2 | boundary tests |
| R08 | Full interval inside => ACCEPT | E2 | uncertainty inside test |
| R09 | Full interval outside => REJECT | E2 | uncertainty outside test |
| R10 | Boundary overlap => FREEZE | E2 | overlap test |
| R11 | Rounding/quantization explicit | E2 | rounding and quantization tests |
| R12 | Key order does not change result | E2 | determinism test |
| R13 | CLI executes fixture end-to-end locally | local integration | CLI fixture tests + validation artifact |
| R14 | Persisted artifacts can be re-read | E0 | pending GitHub read-back |
| R15 | No NEXY.AI repository mutation | repository audit | pending final mutation audit |

| R16 | Signed-128 projection exact or FREEZE | E2 | `test_fixed128.py` |
| R17 | DOC-C 0.85/0.90 threshold examples are exact at 0.01 quantum | E2 | source-grounded projection tests |
| R18 | Rational representation never silently substitutes for Core fixed-point law | design review | `NEXY_COMPATIBILITY.md` |
