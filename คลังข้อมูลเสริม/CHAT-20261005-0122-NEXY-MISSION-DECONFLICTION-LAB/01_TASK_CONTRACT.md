# Task Contract

OBJECTIVE: design, implement, test and persist a non-canonical deterministic concurrent-mission deconfliction reference engine.

IN SCOPE: this new folder, architecture, schema, fixtures, executable Python, tests and verification evidence.

OUT OF SCOPE: mutation to any repository whose name contains NEXY.AI; mutation to sibling supplemental work; production deployment; automatic cancellation; lock stealing.

IMMUTABLE:
hard write/protected/resource/authority collision => FREEZE;
critical missing declarations => reject;
timezone-aware explicit time only;
finite bounded leases;
declared metadata only for overlap;
registry order must not affect decision hash;
no hidden fallback or model inference.

EVIDENCE:
E0 persisted artifacts fetch back.
E1 exact committed Python compiles and JSON parses.
E2 exact committed tests pass.
No E3-E7 claim.

STOP: freeze if writes escape this folder, authority conflicts, or exact committed verification cannot be obtained.