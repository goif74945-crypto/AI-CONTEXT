# Evidence Index

Classification: standalone Lo4 reference implementation only.

| Claim | Evidence class | Artifact | Status |
|---|---|---|---|
| Python source/tests parse and bytecode-compile | E1 | `STATIC_COMPILE.txt` | PASS |
| Focused, negative, algebraic and regression behavior | E2 | `UNIT_TESTS.txt` | PASS, 49 tests |
| Five systems compose and preserve conflict | E3-local | `INTEGRATION_TEST.txt` | PASS, 2 integration tests |
| Reference core avoids forbidden network/subprocess/dynamic execution/environment reads under the implemented AST policy | E1-static security boundary | `SECURITY_BOUNDARY.txt` | PASS |
| Persisted source equals locally tested source | E0 + identity | repository read-back + `SHA256SUMS.txt` | PENDING until publication/read-back |
| NEXY.AI runtime integration | E3/E4 | none | NOT_VERIFIED |
| Production/deployment | E5/E6 | none | NOT_VERIFIED |

The AST security test is not a complete security audit. It proves only the explicit static boundary encoded in `tests/test_security_boundary.py`.
