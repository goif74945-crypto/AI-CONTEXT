# Microbenchmark Report

> These measurements are local sandbox observations, not NEXY.AI production SLAs.

Environment observed by benchmark:
- Python: 3.13.5
- Platform: Linux 6.18.44 x86_64 (glibc 2.41)
- Repeats per workload: 5

| Workload | Size | Median seconds |
|---|---:|---:|
| C1 sequential contract chain | 5,000 components | 0.0379867020 |
| C2 linear artifact/tool plan | 5,000 steps | 0.0651224160 |
| C3 equal portability dimensions | 5,000 dimensions | 0.0296912620 |
| C4 independent correction scopes | 5,000 corrections | 0.2461681110 |
| C5 ddmin stable core | 200 items, 3-item core | 0.0003581680 |

Raw measurements are in `evidence/benchmark.json`.

## Optimization performed during this mission
C1 initially used repeated full pending-set scans. A local pre-optimization observation for a 2,000-component chain was ~0.243329 seconds. After replacing it with an inverted assumption index, a subsequent same-host observation for 2,000 components was ~0.013771 seconds. These are non-controlled development measurements, useful as direction evidence but not a formal benchmark comparison.

C4 was changed from an all-registry correction-pair scan to first group by exact scope/selector, so independent scopes avoid unnecessary pair comparison. Same-scope conflict output can still be quadratic when the number of actual pairwise conflicts is quadratic.
