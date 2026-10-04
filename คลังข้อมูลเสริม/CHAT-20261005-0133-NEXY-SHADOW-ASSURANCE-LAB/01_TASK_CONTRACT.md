# Task Contract

## Objective
Build and verify a standalone shadow-mode assurance prototype that can later support safe NEXY evolution without mutating NEXY.AI.

## Target
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0133-NEXY-SHADOW-ASSURANCE-LAB/`

## Authorized scope
Design documents, Python prototype, fixtures, tests, reports and evidence inside the target directory.

## Protected scope
Every repository whose name contains `NEXY.AI`; existing supplemental projects from other chats; root AI-CONTEXT files unless explicitly required.

## Success invariants
1. Candidate actions are never executed.
2. Stable FREEZE/STOP -> candidate RELEASE is blocking.
3. Stable authority precedence cannot be weakened silently.
4. Evidence must be revision-bound and required classes cannot be silently dropped.
5. Same case with structurally different candidate records is a nondeterminism signal.
6. Policy/input mismatch is not normalized away.
7. PASS requires zero blocking findings and zero unresolved warnings.
8. Code uses Python standard library only.
9. Tests include positive and negative paths.
10. AI-proposed future additions are labeled advisory, not current NEXY requirements.

## Required evidence
E1: Python compilation/static import succeeds.  
E2: executed unit tests.  
E2/E3-like fixture demonstration: PASS and FAIL datasets produce expected gate status through CLI.  
Repository presence: post-write re-fetch from AI-CONTEXT.

## Stop conditions
FREEZE if target repository identity is ambiguous, a write would touch NEXY.AI, secrets are encountered, or concurrent repository movement makes a safe additive commit impossible after bounded retry.
