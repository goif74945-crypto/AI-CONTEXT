# Independent Review — durable queue dispatch CAS

REVIEW_ID: RV-QUEUE-FAILED-STATE-CAS-C-SOL-1933-A4C7
CHAT_ID: C-SOL-20261005-1933-V8-QREV-A4C7
TASK_ID: TASK-QUEUE-FAILED-STATE-CAS-001
FINDING_ID: FINDING-QUEUE-FAILED-STATE-RESURRECTION-001
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_TREE: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
ROLE: INDEPENDENT_REVIEWER / RED_TEAM
SOURCE_MUTATION: NONE
RESULT: P1_FINDING_INDEPENDENTLY_CONFIRMED

## FACT

packages/queue/dispatch.ts@002eef253ce836e2cd0e200f5d15cb5042cdeb29 reads one DirectiveDispatch row before awaiting enqueueDirective().

After enqueueDirective returns, dispatchDirective uses prisma.directiveDispatch.update({ where: { id: row.id } }) and unconditionally writes status=ENQUEUED, increments attempts and clears lastError. The final update does not require the durable row to still be PENDING/ENQUEUED or the previously observed state.

failDirectiveDispatch uses guarded updateMany for PROCESSING/ENQUEUED -> FAILED. cancelDirectiveDispatch also uses a guarded predecessor set. claimDirectiveDispatch likewise uses a guarded compare-and-set style updateMany. The delivery-completion write is therefore the outlier lacking a durable predecessor guard.

packages/queue/jobs.ts@e90ac64acc446c5bbd24a710e0208fc76bce9089 returns idempotent=true when a BullMQ job already exists unless explicit FAILED retryAuthorization is present and the existing job state is failed. A reconciler that originally read durable ENQUEUED does not attach FAILED retryAuthorization.

The documented interleaving is therefore source-valid:
1. reconciler reads ENQUEUED;
2. reconciler awaits queue lookup;
3. worker failure persists FAILED + lastError;
4. reconciler resumes and overwrites the durable row to ENQUEUED + lastError=null;
5. existing BullMQ job can remain failed because no authorized failed-job retry occurred.

## ASSUMPTION

None for the stale-write possibility; the two writes are not protected by one transaction/lock/CAS predicate in the inspected source.

## UNKNOWN

This review did not execute a real Redis/PostgreSQL interleaving. Exact timing frequency is unknown and is not required to classify the unguarded stale write as a concurrency/data-integrity gap.

## Repair constraints

- Commit PENDING/ENQUEUED -> ENQUEUED only if the durable row still satisfies an eligible predecessor condition.
- A CAS miss must be returned distinctly from successful delivery and must not clear lastError.
- FAILED/CANCELLED/COMPLETED written after the initial read must win over stale reconciliation.
- Preserve explicit safe FAILED retry authorization and attempt cap; do not broaden retry error codes.
- Add deterministic interleaving tests for FAILED and, where reachable, CANCELLED/COMPLETED winners.
- Keep BullMQ state and durable projection from falsely diverging as “ENQUEUED” after an unretried failed job.

## Closure effect

ACTIONABLE_CODE_GAP: CONFIRMED
CONCURRENCY_DEFECT: CONFIRMED
DATA_INTEGRITY_DEFECT: CONFIRMED
INVALID_ERROR_PATH: CONFIRMED
MISSING_REQUIRED_TEST: CONFIRMED
GAP_FIXED: NO
REVERIFY_REQUIRED: YES
SOURCE_REPAIR: BLOCKED_BY_INC-BRANCH-NAMESPACE-001
CODE_CLOSURE_ELIGIBLE: NO
