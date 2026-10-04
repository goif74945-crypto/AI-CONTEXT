# Requirement Ledger

R01 additive-only mission folder.
R02 zero mutation to NEXY.AI-named repositories.
R03 explicit lifecycle and bounded lease.
R04 FILE/TREE structural write collision.
R05 protected-scope collision.
R06 exclusive-resource collision.
R07 exclusive-authority collision.
R08 declared overlap only.
R09 missing critical declarations reject.
R10 explicit timezone-aware clock.
R11 inactive incumbents ignored.
R12 registry-order invariance.
R13 controlled-tag normalization.
R14 severity lattice PROCEED < COEXIST < DECONFLICT < FREEZE.
R15 full-state SHA-256 decision seal.
R16 negative-path tests.
R17 fixture corpus includes high-overlap distinct-path case.
R18 exact committed E0/E1/E2 before COMPLETE.

R01-R17 are implemented in the durable core. R18 is pending post-write verification.