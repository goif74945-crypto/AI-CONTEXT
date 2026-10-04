# Integration Proposal — NON-GOVERNING

**Status:** AI_PROPOSED_CONCEPT. Not current NEXY build scope.

## Candidate placement
```text
Task Contract
  -> Context Resolver
  -> Data Policy Lookup
  -> NMDPC
      -> FREEZE -> NEXY::PULSE / reason summary
      -> ALLOW/TRANSFORM -> Bundle Builder
  -> Provider/Tool Gateway
  -> Execution
  -> Disclosure Receipt / Evidence
```

## Required production dependencies before adoption
1. authoritative recipient registry;
2. authoritative data classification registry;
3. purpose registry mapped to capabilities;
4. consent/authority service;
5. credential broker;
6. tokenization/key service;
7. egress gateway that cannot bypass NMDPC;
8. retention/deletion enforcement and evidence;
9. audit pipeline that stores metadata, not raw sensitive values;
10. abuse/integration/E2E tests.

## User-facing idea
For ordinary low-risk work, no extra dialog should appear. For material sensitive disclosure, NEXY could show a compact receipt such as:

- recipient: External Model A;
- purpose: summarize support case;
- sent: issue title, masked customer identity;
- not sent: account history, provider credential;
- retention cap: 10 minutes;
- decision: transformed and allowed.

The exact UX must be tested. This lab does not claim users prefer this presentation.

## Adoption gate
Do not integrate merely because unit tests pass. Minimum gate:
- E3 integration proof at the actual provider gateway;
- bypass-path audit;
- E4 representative user flow;
- E5 operational logging/retention/failure evidence;
- threat-model review;
- privacy/legal review where applicable;
- no conflict with current DOC-B/C authority.
