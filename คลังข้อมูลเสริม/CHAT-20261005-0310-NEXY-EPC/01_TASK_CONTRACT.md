# 01 — Task Contract

## OBJECTIVE
Design, implement, test, repair, and evidence a major standalone NEXY Evolutionary Proposal Court (EPC) reference system containing 20 implemented Lo4 chamber concepts that can be adapted to NEXY.AI later without changing NEXY.AI now.

## TARGET
คลังข้อมูลเสริม/CHAT-20261005-0310-NEXY-EPC

## AUTHORIZED_SCOPE
- Read current AI-CONTEXT.
- Read goif74945-crypto/NEXY.AI- only for source/code evidence.
- Create new files under คลังข้อมูลเสริม/CHAT-20261005-0310-NEXY-EPC/**.
- Create central append-only vote artifacts under คลังข้อมูลเสริม/VOTES/** after the candidate has adequate verification evidence.
- Execute the standalone implementation in isolated/local build environments.

## PROTECTED_SCOPE
- goif74945-crypto/NEXY.AI-: NO WRITE, NO DELETE, NO BRANCH, NO COMMIT, NO PUSH, NO MERGE, NO PR, NO SETTINGS, NO WORKFLOW MUTATION.
- Existing supplemental projects: read-only; no overwrites or cleanup.
- Canon/DOC-B/DOC-C/NEXY CORE/JUDGE/LAW state: EPC has no authority to modify or override them.

## AUTHORITY_SOURCES
1. Current user directive.
2. NEXY-IGNIS canonical source identity recorded by AI-CONTEXT.
3. DOC-B as system law and DOC-C as current build spec per NEXY context.
4. Actual NEXY code at branch NEXY.ai commit 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.
5. AI-CONTEXT Execution Kernel and verification/security rules.

## PRECONDITIONS
- AI-CONTEXT is writable through the connected GitHub capability.
- Project path is unique at creation.
- C++20 GCC/Clang and Boost multiprecision are available in the isolated local runtime.
- Protected NEXY repository remains read-only.

## IMMUTABLE REQUIREMENTS
- 20 distinct chamber concepts must be implemented, not documentation-only placeholders.
- Authoritative EPC numeric decisions use signed Q64.64; no float authority.
- Arithmetic overflow/divide-zero fails closed.
- Same candidate + same evidence + same policy yields the same result.
- Court output is advisory_only=true and authoritative=false.
- WIP/UNKNOWN cannot become CUT merely because evidence is sparse.
- Semantic duplicate CUT evidence requires concrete path + function/module + Canon reference + commit + semantic basis.
- One CHAT_ID may cast KEEP once and CUT once for its lifetime.
- Vote revision never adds vote rights and never silently rewrites prior verdict.
- CUT never physically deletes candidate data.
- No automatic promotion into NEXY.AI.
- FACT / ASSUMPTION / UNKNOWN remain explicit.

## REQUIRED_EVIDENCE
- E0 presence/read-back.
- E1 dual-compiler static/build verification.
- E2 executed unit and deterministic/property tests.
- E2 negative-path arithmetic/authority/vote-right tests.
- Sanitizer execution where supported.
- Exact persisted-byte hashes and re-execution after persistence.
- E3 actual NEXY integration remains NOT_VERIFIED and out of current mutation scope.

## ACCEPTANCE CRITERIA
- TDD red evidence exists before implementation.
- GCC and Clang builds succeed with warnings treated as errors.
- All unit/property tests pass.
- Tests cover all 20 chambers and user vote invariants.
- Sanitizer run has no detected runtime errors.
- Persisted GitHub files read back and hash-match tested local bytes.
- No protected NEXY mutation occurs.
- A KEEP vote, if cast, contains every user-required field and binds exact Spec/NEXY/AI-CONTEXT identities.

## STOP_CONDITIONS
- Protected scope would be touched.
- Target identity changes ambiguously.
- Relevant Canon conflict cannot be resolved.
- Required verification cannot be executed.
- Persistence read-back differs from intended bytes.

## DELIVERABLES
Design + 20 concept catalog + C++20 implementation + tests + examples + failure/threat model + integration contract + TDD evidence + final execution evidence + exact hashes + durable execution record + EPC vote evidence.
