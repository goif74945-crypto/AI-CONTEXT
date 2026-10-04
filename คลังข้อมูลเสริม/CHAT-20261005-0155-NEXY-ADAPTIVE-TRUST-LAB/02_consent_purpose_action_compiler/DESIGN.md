# CPAC — Consent-Purpose Action Compiler

**Status:** AI_PROPOSAL / NON_GOVERNING

## Objective
Make user consent inspectable and purpose-bound. A broad authenticated session must not be treated as consent for every action that the session technically permits.

## Separation from existing delegation lease work
A delegation lease scopes *agent execution authority*. CPAC scopes *user consent to a declared purpose/action/resource*. CPAC cannot elevate RBAC/LAW and does not delegate anything.

## Contract
A grant binds subject, one or more purposes, exact action verbs, exact resources, issue/expiry time, and revocation state. Wildcards are intentionally rejected by the reference implementation.

## Invariants
- exact subject match;
- exact purpose/action/resource membership;
- grant must be active and unrevoked;
- wildcard scope is invalid;
- decision receipt is deterministic and does not contain sensitive payload values;
- ALLOW means only “consent grant matched”; upstream authorization/policy may still deny.

## Failure semantics
Malformed grant/request → `BLOCK`; no valid matching grant → `ASK`; exact active match → `ALLOW`.

## Integration
Use as an additional restrictive gate before sensitive connector/export/write actions, downstream of authentication but upstream of execution. Combine with LAW/RBAC/lease/privacy policies using deny-dominant composition.
