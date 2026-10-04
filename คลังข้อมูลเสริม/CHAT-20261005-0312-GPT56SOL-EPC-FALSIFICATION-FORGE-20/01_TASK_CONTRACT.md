# TASK CONTRACT — EPC Falsification & Experimental Design Forge 20

## OBJECTIVE
Create a standalone, reusable Lo4 experimental-falsification package containing exactly 20 mechanisms that can later be adapted to NEXY.AI while remaining non-authoritative.

## AUTHORITY SOURCES
1. Explicit user directive defining EPC, Lo4 status, Q64.64 and vote law.
2. NEXY canonical/source context from AI-CONTEXT, source SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
3. Current NEXY implementation observed read-only at 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.
4. AI-CONTEXT execution/security/verification rules.
5. This Lo4 design only after the above.

## AUTHORIZED SCOPE
- create/update files under คลังข้อมูลเสริม/CHAT-20261005-0312-GPT56SOL-EPC-FALSIFICATION-FORGE-20/**
- execute isolated local compilation/tests of those exact bytes
- read NEXY.AI source/tests/evidence for compatibility only
- create a unique append-only vote receipt only when evidence is sufficient

## PROTECTED SCOPE
- every mutation to a repository whose name contains NEXY.AI
- Canon/LAW/CORE/JUDGE runtime state
- production/deployment state
- secrets/credentials
- other chats' namespaces and vote history

## IMMUTABLE REQUIREMENTS
- exactly 20 distinct falsification/experimental-design mechanisms
- checked signed Q64.64 for authoritative metrics
- no authoritative binary floating point
- deterministic stable ordering and serialization
- fail closed on malformed/missing critical inputs, overflow and divide-by-zero
- no hidden time/random/network dependence
- no automatic promotion or Core state mutation
- KEEP/CUT rights obey one-per-chat lifetime rule
- UNKNOWN/WIP never sufficient CUT basis
- CUT is non-destructive disposition only
- Design + Code + Tests + Evidence remain together
- all completion claims require matching fresh evidence

## ACCEPTANCE CRITERIA
AC01 exactly 20 mechanisms implemented and documented.
AC02 Q64.64 checked arithmetic covers add/sub/mul/div/ratio and range errors.
AC03 tests prove deterministic same-input replay.
AC04 tests prove malformed critical evidence fails closed.
AC05 tests cover boundary, fault, assumption, oracle, stopping, counterexample, environment, determinism, resource, version, observability, reproducibility and independence behavior.
AC06 authoritative paths contain no Number/parseFloat/Math.random/Date.now-based decisions.
AC07 strict static/type checks pass.
AC08 unit/negative/property/integration tests execute with zero failures.
AC09 tested source hashes are captured.
AC10 persisted source/tests/design/evidence are read back from GitHub.
AC11 protected NEXY.AI- HEAD remains unchanged by this mission.
AC12 no vote is cast while evidence is WIP/insufficient.

## REQUIRED EVIDENCE
E0 persisted artifact presence/readback.
E1 TypeScript static/type check and forbidden-pattern scan.
E2 unit/property/negative tests.
E3 cross-mechanism integration/replay test.
Hash manifest over exact tested bytes.
Protected repo exact-head recheck.

## STOP CONDITIONS
- required action would mutate NEXY.AI-;
- authority conflict cannot be resolved safely;
- tested bytes differ from persisted bytes without revalidation;
- critical PASS lacks its required evidence class;
- persistence cannot be read back and verified.
