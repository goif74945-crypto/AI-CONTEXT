# TASK CONTRACT — EPC Formal Constitutional Verification Fabric 20

## OBJECTIVE
Produce an isolated, executable, evidence-backed reference package containing exactly 20 formal verification mechanisms for the NEXY Evolutionary Proposal Court (EPC). The package verifies constitutional invariants of the court protocol and must be suitable for later adapter/shadow-verifier integration with NEXY.AI without modifying NEXY.AI in this task.

## TARGET
`คลังข้อมูลเสริม/CHAT-20261005-0312-NEXY-EPC-FCVF20-7A9C/`

## AUTHORITY
1. Explicit current user directive.
2. Canonical NEXY-IGNIS source bytes, SHA-256 `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
3. Current NEXY implementation read-only at `goif74945-crypto/NEXY.AI-@9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
4. Current AI-CONTEXT execution/security/verification laws.
5. This Lo4 proposal after all above.

## AUTHORIZED SCOPE
- create/update files inside this unique AI-CONTEXT namespace;
- run isolated local code/tests with no production/network authority;
- read NEXY source/config/tests for compatibility evidence;
- create one append-only KEEP vote receipt only after evidence sufficiency is proven.

## PROTECTED SCOPE
- any repository whose name contains `NEXY.AI`;
- Canon, LAW, CORE, JUDGE, SWARM runtime state;
- production/deployment systems;
- other chats' namespaces and vote receipts;
- secrets/credentials.

## IMMUTABLE REQUIREMENTS
- exactly 20 distinct mechanisms;
- protocol verification focus, not proposal-quality scoring;
- checked signed Q64.64 quantitative metrics;
- no binary-float authoritative decision path;
- deterministic canonical serialization and ordering;
- no hidden time/random/network dependency;
- KEEP <= 1 and CUT <= 1 per CHAT_ID;
- DEFER/WIP/INSUFFICIENT_EVIDENCE consumes no vote right;
- WIP/UNKNOWN cannot justify CUT;
- historical verdict cannot be changed in place;
- CUT is non-destructive;
- semantic duplicate claims require a concrete target + witness;
- critical evidence is exact-spec/code/context bound;
- score/vote cannot override Canon/Law/JUDGE;
- no automatic promotion or Core mutation;
- invalid transitions fail closed;
- same logical evidence set in a different insertion order yields the same receipt/verdict;
- published bytes must match tested bytes or be re-tested.

## ACCEPTANCE CRITERIA
AC-01: exactly 20 mechanisms documented and implemented.
AC-02: Python package compiles under the available interpreter.
AC-03: Q64.64 boundary/overflow/div-zero tests pass.
AC-04: vote-right automaton rejects second KEEP and second CUT.
AC-05: DEFER does not consume KEEP/CUT rights.
AC-06: WIP and INSUFFICIENT_EVIDENCE cannot produce CUT.
AC-07: prior verdict mutation is rejected.
AC-08: promotion/Core/Canon override events are non-interfering and rejected.
AC-09: CUT never emits delete semantics.
AC-10: duplicate claims without semantic witness are rejected.
AC-11: missing critical evidence produces fail-closed DEFER/NOT_VERIFIED behavior.
AC-12: canonical serialization is insertion-order independent.
AC-13: bounded state exploration proves unsafe states unreachable for the modeled alphabet/depth.
AC-14: a deliberately weakened constitutional rule is detected by regression differential with a reproducible counterexample.
AC-15: minimal counterexample reduction preserves violation.
AC-16: deterministic repeated runs produce identical state-space/result hashes.
AC-17: source/test manifest binds exact bytes.
AC-18: Design + Code + Tests + Evidence + integration guidance are co-located.
AC-19: GitHub read-back verifies publication.
AC-20: NEXY.AI head remains unchanged by this work.

## REQUIRED EVIDENCE
- E0 persisted artifact presence/read-back;
- E1 `compileall` plus source-level float-path scan;
- E2 executed unit/property/negative tests;
- E3 executed cross-component model-check/regression tests;
- deterministic replay/result hash;
- SHA-256 manifest;
- protected-repository re-check.

## STOP CONDITIONS
- a needed action would mutate NEXY.AI;
- authoritative spec/code conflict cannot be resolved;
- implementation can pass only by weakening an immutable requirement;
- exact tested bytes cannot be matched to published bytes;
- KEEP/CUT evidence is insufficient.