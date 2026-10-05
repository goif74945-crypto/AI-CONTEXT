# Independent Review — TASK-DOC-C-INCIDENT-PRIORITY-AUTHORITY-001

REVIEWER_CHAT: C-SOL-20261005-1923-V8
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
TASK_ID: TASK-DOC-C-INCIDENT-PRIORITY-AUTHORITY-001
FINDING_ID: FINDING-DOC-C-INCIDENT-PRIORITY-AUTHORITY-001
VERDICT: PARTIALLY_CONFIRMED_AND_SCOPE_NARROWED
SOURCE_MUTATION: NONE

## Confirmed

1. Locked final DOC-C ends at §5.6 / raw paragraph 10499.
2. `packages/obs/incident-priority.ts` claims `DOC-C §5.8 / §11.4`, so its authority citation is invalid under the active build authority.
3. `tests/contract/incident-semantics.test.ts` explicitly names the hardcoded rank sequence the "fixed DOC-C primary priority order".
4. Exact scan of final DOC-C 9886-10499 contains no incident error ranking or priority table.
5. Therefore the test is a TEST_ORACLE_DEFECT insofar as it attributes that ranking to final DOC-C, and source comments have AUTHORITY_CITATION_DRIFT.

## Not yet proven

Final DOC-C requires primary incident creation and linked secondary failures but does not explicitly say whether a later higher-priority failure may replace the persisted primary. Absence of a rank table proves that the current ranking is not a DOC-C requirement; it does not by itself prove that every deterministic ranking policy is forbidden.

Therefore:
- confirmed actionable repair: remove/rebind false DOC-C citations and stop using the hardcoded ordering as a DOC-C oracle;
- runtime primary-replacement semantics require a separate active-authority search/compatibility review before change;
- do not silently delete or preserve the ranking based only on this finding.

## Closure impact

The current test suite can reject a spec-correct implementation for failing a non-authoritative "DOC-C" rank order. This blocks TEST_CLOSURE until the oracle is corrected or separately authorized.

BLOCKER: INC-BRANCH-NAMESPACE-001 prevents Constitution-compliant source/test mutation.
