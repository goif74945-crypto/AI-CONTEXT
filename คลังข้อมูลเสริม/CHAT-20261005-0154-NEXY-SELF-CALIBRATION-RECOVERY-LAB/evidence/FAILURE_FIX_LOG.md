# Failure → Fix → Re-test Log

| ID | Observed defect/failure | Root cause | Correction | Re-test status |
|---|---|---|---|---|
| F01 | Iterable validation could occur after iterator consumption | normalization order | materialize once, validate mappings first | PASS |
| F02 | Duplicate sequence values could make ddmin remove wrong occurrence | value-based chunk location | explicit index ranges | PASS |
| F03 | `True` and `1` could collapse in mined atoms | Python equality/hash semantics | typed scalar tags | PASS |
| F04 | NaN/Infinity could enter deterministic trace model | missing finite-number guard | reject non-finite float | PASS |
| F05 | Duplicate PauseSafe step IDs were accepted | missing identity uniqueness check | explicit duplicate rejection | PASS |
| F06 | ddmin core alone did not guarantee arbitrary-predicate 1-minimality | algorithm contract stronger than core reduction phase | deterministic post-proof single-removal loop | PASS |
| F07 | Direct benchmark script could not import root packages | Python script path semantics | canonical module invocation, no runtime path hack | PASS |
| F08 | Test name claimed 64 trigger pairs while exhaustive matrix is 28 | inaccurate test label | rename to exact 28-pair claim | PASS |
