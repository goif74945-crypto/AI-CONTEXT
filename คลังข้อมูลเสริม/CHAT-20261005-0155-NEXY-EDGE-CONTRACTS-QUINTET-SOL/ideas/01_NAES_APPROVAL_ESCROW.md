# 01 — NAES: NEXY Approval Escrow Seal

**Status:** AI-PROPOSED CONCEPT.

## Problem
Human approval can become unsafe between review and execution: the plan changes, scope widens, instructions move to a newer directive epoch, or the approval is simply stale. A generic "approved=true" flag is therefore dangerously under-specified.

## Design
NAES creates a plan-bound authorization seal containing plan hash, authority identity, exact allowed scope, directive epoch, expiry and mutation budget. The reference uses HMAC only to demonstrate record integrity; production identity/authentication remains an upstream responsibility.

## Invariants
- changed plan hash => FREEZE;
- expired approval => FREEZE;
- changed directive epoch => FREEZE;
- requested scope not subset of approved scope => FREEZE;
- mutation count beyond approved budget => FREEZE;
- invalid record signature => FREEZE.

## NEXY integration hypothesis
Place between human approval and NEXY::RUN side-effect execution so authorization is checked against the exact candidate action bundle immediately before commit.
