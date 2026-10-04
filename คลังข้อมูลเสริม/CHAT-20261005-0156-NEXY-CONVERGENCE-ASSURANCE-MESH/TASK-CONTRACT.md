# Task Contract

## Objective
Build and verify five new NEXY-compatible auxiliary systems outside the NEXY implementation repository, persist them under AI-CONTEXT `คลังข้อมูลเสริม`, and preserve resumable evidence.

## Target
- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch: `main`
- Authorized write root: `คลังข้อมูลเสริม/CHAT-20261005-0156-NEXY-CONVERGENCE-ASSURANCE-MESH/`

## Authorized scope
New files under the mission root only.

## Protected scope
- Any repository whose name contains `NEXY.AI`.
- Existing AI-CONTEXT files outside the mission root.
- Credentials and secrets.

## Preconditions observed
- AI-CONTEXT exists, default branch `main`, push permission available.
- `คลังข้อมูลเสริม` already exists.
- NEXY current context states deterministic verify/freeze principles.
- Existing recent supplemental work was inspected to avoid obvious concept collision.

## Success invariants
1. No protected path is mutated.
2. New concepts remain clearly AI-proposed, not canonical requirements.
3. Every RELEASE/PASS path has executable evidence.
4. Every critical ambiguity/failure path fails closed.
5. Equivalent input ordering does not alter deterministic outputs where order is semantically irrelevant.
6. Evidence planning never substitutes a lower class for a higher required class.
7. Evidence independence accounts for producer/failure-domain ancestry.
8. Resume proof ignores explicitly ephemeral state but freezes on resume-critical drift.

## Required evidence
- E0: files exist/read back from GitHub.
- E1: Python compileall succeeds; secret-pattern scan has zero findings.
- E2: concept unit tests pass.
- E3: local integration mesh tests pass.
- Additional property/regression evidence under multiple `PYTHONHASHSEED` values.

## Stop conditions
- A required action would mutate protected NEXY scope.
- Repository target or authority becomes uncertain.
- Fast-forward-only commit cannot be made safely after refresh/retry.
- Required evidence cannot be reproduced.
