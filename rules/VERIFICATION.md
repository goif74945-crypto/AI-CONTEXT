# VERIFICATION LAW

## 1. Status vocabulary
Use exactly:
- PASS
- FAIL
- PARTIAL
- BLOCKED
- NOT_VERIFIED
- UNKNOWN
- CONFLICT

Do not invent optimistic substitutes such as “basically done.”

## 2. Evidence classes

### E0 — Presence
File/symbol/config exists.
Proves presence only.

### E1 — Static
Parser/compiler/typecheck/lint/schema/static analysis.
Proves static properties only.

### E2 — Unit
Executed isolated behavior test.

### E3 — Integration
Executed interaction across components/services.

### E4 — End-to-End
Executed real user/system flow through relevant boundaries.

### E5 — Runtime/Operational
Logs, metrics, traces, load/fault/recovery behavior in the target runtime.

### E6 — Deployment
Exact build deployed in exact environment, with health/smoke/rollback/monitoring evidence.

### E7 — Physical
Hardware-in-loop or physical-world evidence.

Higher evidence class is not always “better”; the required class depends on the claim.

## 3. Claim/evidence matching
Examples:
- “type-safe” → E1 may suffice.
- “function returns X” → E2.
- “API and DB work together” → E3.
- “user can complete flow” → E4.
- “recovers from worker crash” → E5.
- “production deployed successfully” → E6.
- “emergency stop halts robot” → E7.

## 4. PASS rule
PASS requires:
- correct target;
- current relevant version/commit;
- matching evidence class;
- successful result;
- no unresolved blocker that invalidates the claim.

## 5. PARTIAL
Use when:
- only part of the contract was proven;
- some required environments/platforms remain;
- static evidence exists but runtime proof is still required.

## 6. NOT_VERIFIED
Use when:
- implementation/design may exist;
- required evidence was not executed or not available.

## 7. BLOCKED
Use only when an external/precondition obstacle prevents verification or completion.
Name the blocker precisely.

## 8. UNKNOWN
Use when state cannot be established from available evidence.
Do not convert UNKNOWN into FAIL unless absence/failure is proven.

## 9. CONFLICT
Use when credible authorities/evidence disagree and no rule currently resolves them.

## 10. Regression
After a repair:
- rerun the failing proof;
- run nearby regression tests;
- re-check invariants;
- inspect final diff/state.

A focused PASS does not prove unrelated system-wide cleanliness.

## 11. Negative-path proof
Critical systems must test failure paths:
- invalid input;
- permission denial;
- timeout;
- dependency failure;
- duplicate/idempotency behavior;
- freeze/rollback/recovery;
- security-abuse cases where applicable.

## 12. Evidence record
A useful evidence record contains:
- claim;
- target;
- version/commit;
- evidence class;
- command/test;
- environment;
- result;
- artifact/log reference;
- limitations.

## 13. No stale evidence
If relevant code/config changed after evidence was produced, revalidation is required.

## 14. No fake execution
Never imply a command/test/browser/deploy was run when it was not.
