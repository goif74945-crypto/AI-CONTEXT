# Second Independent Review — TASK-DOC-C-INCIDENT-PRIORITY-AUTHORITY-001

REVIEW_ID: RVW-DOC-C-INCIDENT-PRIORITY-C-SOL-20261005-1916-V8-AUDIT
TASK_ID: TASK-DOC-C-INCIDENT-PRIORITY-AUTHORITY-001
FINDING_ID: FINDING-DOC-C-INCIDENT-PRIORITY-AUTHORITY-001
REVIEWER_CHAT: C-SOL-20261005-1916-V8-AUDIT
ROLE: INDEPENDENT_SPEC_AUTHORITY_REVIEWER / RED_TEAM
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_MUTATION: NONE

## AUTHORITY
AUTHORITY_MAP states that build obligation comes from DOC-C only and historical/superseded text cannot be mixed as equal build authority.
Locked final DOC-C ends at §5.6. Its incident law requires primary incident creation for FREEZE/STOP, secondary failures linked as secondary incidents, and recover AuditLog + EventLog. The final DOC-C contains no incident error-code rank table.

An exact AI-CONTEXT authority search found no active authority record for the hardcoded SECURITY_BREACH_DETECTED > SCHEMA_VIOLATION > STATE_TRANSITION_DENIED > CONSENSUS_FAILED > TIMEOUT/AGENT_TIMEOUT ranking.

## EXACT-HEAD SOURCE FACTS
packages/obs/incident-priority.ts blob 12689c38239fc49f83c6dc23d0c73a6f7c667717:
- cites nonexistent final-DOC-C §5.8 / §11.4;
- defines the above rank table;
- can replace an existing primary with a later higher-ranked code.

packages/queue/run-state.ts and packages/orch-core/system-state.ts consume that arbitration and can change persisted primary incident truth.

tests/contract/incident-semantics.test.ts blob 7dc8d552cf407e4b83dff4a23cdb16112c350db3 names the ordering the "fixed DOC-C primary priority order" and therefore protects a non-DOC-C rule as the test oracle.

packages/contracts/incidents.ts and packages/obs/incidents.ts also cite DOC-C §10/§11, which are outside the locked final build-spec range.

## VERDICT
FALSE_DOC_C_CITATIONS: CONFIRMED
TEST_ORACLE_DEFECT_FOR_RANK_AS_DOC_C: CONFIRMED
RUNTIME_RANKING_IS_REQUIRED_BY_DOC_C: FALSE
RUNTIME_RANKING_IS_FORBIDDEN_BY_DOC_C: NOT_PROVEN
PERSISTED_PRIMARY_REPLACEMENT_COMPATIBILITY: REVERIFY_REQUIRED
REVIEW_RESULT: SECOND_INDEPENDENT_PARTIAL_CONFIRMATION_WITH_SCOPE_NARROWING

## SAFE REPAIR CONTRACT
1. Remove/rebind false DOC-C section citations.
2. Stop describing the hardcoded rank order as a final-DOC-C requirement.
3. Preserve final-DOC-C primary creation and linked secondary failures.
4. Do not delete or preserve primary replacement semantics merely from absence of a rank table. If runtime semantics are changed, first resolve compatibility/persistence/API/replay effects and identify any active non-DOC-C incorporation path that is allowed to constrain the build.
5. Maintain canonical ErrorCode validation.

GLOBAL_BLOCKER: INC-BRANCH-NAMESPACE-001 prevents isolated source/test mutation.
