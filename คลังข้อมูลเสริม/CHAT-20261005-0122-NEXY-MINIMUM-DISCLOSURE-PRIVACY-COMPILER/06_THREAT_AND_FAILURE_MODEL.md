# Threat and Failure Model

## Protected asset
User/project data crossing a model/processor/tool boundary.

## Threats in scope
1. **Over-collection:** unrelated fields sent because they happen to be present in context.
2. **Purpose creep:** previously permitted data reused for a new purpose.
3. **Recipient ambiguity:** unknown processor/model trust treated as safe by default.
4. **Credential leakage:** API key/token inserted into prompt/tool context.
5. **Sensitive raw-value leakage:** private/internal fields sent when masked/tokenized form suffices.
6. **Secret exfiltration:** strategic/private system secret sent to an external model.
7. **Retention inflation:** recipient/context retention exceeds policy maximum.
8. **Rule collision:** multiple policy rules define the same field inconsistently.
9. **Order dependence:** plan changes based on incidental rule input order.
10. **Freeze bypass:** downstream bundle builder proceeds despite a failed precondition.

## Threats out of scope for prototype
- actual network egress enforcement;
- provider identity verification;
- data residency enforcement;
- cryptographic key management;
- side-channel leakage;
- model memorization measurement;
- downstream deletion proof;
- legal compliance determination;
- tenant authorization;
- production secret broker implementation.

## Failure semantics
- material ambiguity → FREEZE;
- missing transform runtime key → execution error, no partial bundle;
- missing planned payload field → execution error, no silent omission;
- duplicate rule → global FREEZE;
- unknown classification path → FREEZE defensively.

## Anti-bypass integration requirement
A future integration is only meaningful if every external context path is forced through a single enforcement boundary. A helper library that callers can bypass does not satisfy the security claim.
