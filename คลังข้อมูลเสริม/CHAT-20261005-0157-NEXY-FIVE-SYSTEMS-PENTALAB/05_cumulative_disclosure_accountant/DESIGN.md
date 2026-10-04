# Design — NEXY Cumulative Disclosure Accountant (CDA)

**Status:** AI-PROPOSED / NON-AUTHORITY / NOT PRODUCTION INTEGRATED.

## Objective
Detect privacy exposure that composes across repeated individually acceptable releases.

## Algorithm
Track unique disclosed items per audience; compute projected cumulative audience/category/linkability exposure; freeze on budget/concentration breach; REVIEW near limit without mutating state; ALLOW advances canonical ledger; accepted event replay rejects.

## Invariants
No double charge for same item/audience; audiences isolated; FREEZE and REVIEW preserve state; purpose changes do not erase prior exposure; deterministic receipts.

## Complexity
O(C+A) over catalog and projected audience items plus deterministic sorting.

## Future NEXY boundary
Candidate after per-transfer minimum-disclosure/egress policy and before external dispatch. Accounting guard only, not legal advice or consent authority.

## Limits
Risk points/budgets are engineering policy inputs, not calibrated privacy guarantees; no time decay/cross-audience collusion yet.

## Security boundary
No network access, credential handling, repository mutation, production side effect, or NEXY law override occurs in the reference engine. A future adapter must validate provenance and authorization.
