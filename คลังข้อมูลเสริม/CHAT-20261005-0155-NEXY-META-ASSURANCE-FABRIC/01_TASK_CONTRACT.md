# Task Contract — NEXY Meta-Assurance Fabric

Status: LOCKED
Chat reference: CHATREF-20261005-0155-NEXY-META-ASSURANCE-FABRIC
Mission ID: MISSION-NEXY-META-ASSURANCE-20261005-0155-A
Authority: explicit user request + AI-CONTEXT execution kernel/rules
Repository: goif74945-crypto/AI-CONTEXT
Branch: main
Write root: `คลังข้อมูลเสริม/CHAT-20261005-0155-NEXY-META-ASSURANCE-FABRIC/`

## OBJECTIVE
Design, implement, execute tests for, and preserve evidence for five high-value future systems that are compatible in principle with NEXY.AI's deterministic, verify-only, freeze-on-insufficient-evidence philosophy, while never modifying a NEXY.AI repository.

## REQUIRED OUTPUT
For each of five concepts:
- proposal/design document;
- deterministic standalone implementation;
- executable tests including negative paths;
- executed test evidence;
- limitations and integration boundary.

Mission-level:
- temporary mission memory;
- requirement/evidence ledger;
- final completion record;
- durable resume point.

## INPUTS
- AI-CONTEXT root INDEX.md
- AI-EXECUTION-KERNEL.md
- relevant rules/workflows
- projects/NEXY.AI/overview.md
- supplementary folder index/listing
- direct collision-search results

## IN SCOPE
Only additive files under `คลังข้อมูลเสริม/CHAT-20261005-0155-NEXY-META-ASSURANCE-FABRIC/`, plus a minimal additive index entry if needed for discoverability.

## PROTECTED / OUT OF SCOPE
- Any repository whose name contains `NEXY.AI`: no writes, deletes, renames, commits, pushes, merges, branches, settings, workflows, issues, PR mutations, or any other data-changing action.
- Existing supplementary projects: read-only for collision detection.
- Production deployment and claims of real NEXY integration.
- Changing canonical NEXY requirements.

## IMMUTABLE REQUIREMENTS
R1. Exactly five distinct concepts.
R2. Every concept is explicitly labeled PROPOSAL.
R3. Every concept has real code, not placeholder/pseudocode.
R4. Every concept has executable tests.
R5. Negative/failure behavior is tested.
R6. Runtime PASS claims require actual test execution.
R7. Core algorithms are deterministic for identical inputs.
R8. Core modules fail closed for invalid/insufficient inputs.
R9. No hidden network, clock, randomness, database, environment, or process I/O in core logic.
R10. No NEXY.AI repository mutation.
R11. Preserve design + code + test + evidence in the work folder.
R12. Collision checks must be recorded with bounded wording.
R13. A final read-back verifies durable persistence.
R14. Any integration claim is limited to interface compatibility proposal, not implemented NEXY functionality.

## FIVE CONCEPTS
C1 — Metamorphic Verification Synthesizer (MVS)
Purpose: verify systems when a complete expected-output oracle is unavailable by checking deterministic relations between transformed inputs/outputs.
Distinctive value: gives NEXY a legal verification path for classes of computations where exact expected values are expensive or unknown but invariant relations are authoritative.

C2 — Conservation-Law Ledger (CLL)
Purpose: verify that declared conserved quantities/rights/resources remain balanced across multi-step state transitions.
Distinctive value: catches silent creation/destruction of budget, quota, ownership units, capability counts, or other conserved state.

C3 — Minimal Proof Witness Extractor (MPWE)
Purpose: derive a deterministic minimal evidence subset that covers every required claim, with stable tie-breaking and explicit uncovered requirements.
Distinctive value: shrink evidence surfaced to users/agents without weakening claim coverage.

C4 — Behavioral Fingerprint Kernel (BFK)
Purpose: canonically fingerprint scenario→outcome behavior across versions and identify precise semantic drift independently of implementation layout.
Distinctive value: compatibility/regression detection based on observable behavior rather than file diffs.

C5 — Specification Mutation Sentinel (SMS)
Purpose: mutation-test policy/specification gates by generating controlled illegal variants and proving that validators reject them.
Distinctive value: tests whether NEXY's guardrails actually detect requirement violations rather than merely passing the happy path.

## ACCEPTANCE CRITERIA
A1. Five proposal docs exist.
A2. Five implementation modules exist and import cleanly.
A3. Unit test suite exercises all five modules.
A4. At least one negative-path test per module.
A5. Local executed suite returns zero failures.
A6. Test evidence includes command, environment, observed result, and limitations.
A7. GitHub read-back proves the persisted source/test/docs exist.
A8. Completion record maps R1-R14 to evidence/status.
A9. No protected repository mutation occurs.

## REQUIRED EVIDENCE
- E0: GitHub file presence/read-back.
- E1: Python compile/import checks.
- E2: executed unittest behavior tests.
No E3-E7 integration/runtime/deployment claims are authorized or required.

## RISKS
- Concept collision with differently named prior work: mitigated by folder enumeration + keyword searches; residual semantic collision remains possible and must be stated.
- Local test evidence not bound to GitHub commit: mitigate by generating local files from the exact persisted content or re-fetching and re-running when feasible; otherwise state limitation.
- Direct-to-main concurrent writers: use unique folder to avoid path conflict, then read back.

## STOP / FREEZE CONDITIONS
- Any required action would mutate NEXY.AI repository.
- Target identity becomes uncertain.
- Existing file collision appears at the chosen path.
- Required runtime proof cannot be executed.
- Authoritative project rule conflicts with this contract.
- A concept cannot be distinguished from existing work after inspection.

## COMPLETION RULE
COMPLETE is legal only when R1-R14 are all PASS or explicitly non-blocking with no material NOT_VERIFIED, all required files are persisted and read back, tests pass, and protected scope remains untouched.
