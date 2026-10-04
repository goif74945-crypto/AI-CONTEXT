# CAWT Evidence

- E1: AST/compileall PASS.
- E2: dangerous authority expansion, conflict handling, duplicate identity rejection, no-change behavior, order determinism PASS.
- Stress: CAWT fingerprint remained stable under 8,000 seeded shuffle iterations used inside the 40,000 combined check suite.
- E3: integrated promotion gate freezes when CAWT reports authority expansion.

Limits: decision corpus quality determines blast-radius coverage. This prototype does not prove complete coverage of all real NEXY authority states.
