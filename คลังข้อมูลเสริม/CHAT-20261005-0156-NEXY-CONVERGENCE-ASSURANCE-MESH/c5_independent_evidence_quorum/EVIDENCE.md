# C5 Evidence

- Two producer/domain-disjoint E3 witnesses satisfy a 2-witness quorum: **E2 PASS**.
- Shared failure domain freezes: **E2 PASS**.
- Shared producer freezes: **E2 PASS**.
- Derived evidence inherits parent failure domain and cannot fake independence: **E2 PASS**.
- Dependency cycle blocks: **E2 PASS**.
- Lower evidence class excluded: **E2 PASS**.
- 150 deterministic random simple quorum cases match an independent pairwise oracle: **E2 PASS**.

Raw runs: `../evidence/test-seed-1.txt`, `../evidence/test-seed-777.txt`.
