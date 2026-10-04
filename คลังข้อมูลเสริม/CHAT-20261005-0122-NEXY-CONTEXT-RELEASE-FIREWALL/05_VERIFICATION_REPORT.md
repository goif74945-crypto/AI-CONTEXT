# Verification Report — Context Release Firewall Lab

Status: PASS for the standalone reference scope described below.
Classification: E1 + E2 evidence for this lab only.
NEXY.AI integration/runtime/deployment: NOT_VERIFIED.

## Verified target
Local artifact set corresponding to:
`คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-CONTEXT-RELEASE-FIREWALL`

## Environment
Recorded in `evidence/E1_E2_RUN.txt` together with the executed commands and raw results.

## Evidence sequence

### E1 — Python compile/static parse
Command:
`python -m compileall -q src tests scripts examples`

Final result: PASS.

### E1 — Lab structural validation
Command:
`python scripts/validate_lab.py`

Final result: PASS.
Validator checks Python parsing, JSON parseability, adversarial fixture structure/uniqueness, and required artifact presence.

### E2 — Unit/adversarial behavior
Command:
`PYTHONPATH=src python -m unittest discover -s tests -v`

Final result: PASS — 36 tests.

Covered behaviors include:
- public/internal release;
- sensitivity ceiling across the complete 6x6 lattice;
- atomic freeze on blocked required context;
- optional minimization;
- missing/expired data;
- purpose binding;
- compartment boundaries and escalation rejection;
- derived sensitivity/compartment/purpose taint rules;
- derivation cycle/unknown-source rejection;
- noncanonical float rejection;
- trusted, forged, tampered and expired declassification grants;
- blocked-value non-disclosure in receipt;
- unrequested-data receipt non-correlation regression;
- deterministic hash behavior across mapping order;
- identity normalization/control-character hardening;
- fixture manifest integrity.

### E2 — Executable example
Command:
`PYTHONPATH=src python examples/minimal_release.py`

Final result: PASS.
Observed status: `RELEASED`.
Observed payload contains only the explicitly requested `task`; the unrequested secret field is absent.

## Failure/fix history
An earlier test run produced 30 PASS + 1 FAIL in `test_trusted_declassification_can_release`.

Root cause: the test used evaluation time `2026-10-05T01:30:00+07:00`, which is `2026-10-04T18:30:00Z`, while the grant's original `not_before` was `2026-10-05T00:00:00Z`. The engine correctly rejected the grant because it was not active yet. The test expectation was wrong.

Correction:
- adjusted the trusted grant fixture window to actually include the evaluation instant;
- reran the focused test;
- reran full compile, structural validation, and suite.

During this audit, an additional privacy hardening issue was identified: the receipt's context-metadata hash originally committed metadata for every field in the supplied ContextSet, including unrequested fields. Values were not leaked, but this could create unnecessary correlation. The engine was changed so the metadata hash covers only explicitly requested keys. A regression test now proves adding an unrelated unrequested secret does not change receipt/context-metadata hashes.

## Evidence-class boundary
These results prove only behavior of the standalone reference code exercised in this isolated local Python environment.

They do not prove:
- integration into NEXY.AI;
- provider/network privacy;
- cryptographic signer identity;
- production policy correctness;
- deployment hardening;
- provider retention behavior;
- E3/E4/E5/E6 properties.

Those remain NOT_VERIFIED.
