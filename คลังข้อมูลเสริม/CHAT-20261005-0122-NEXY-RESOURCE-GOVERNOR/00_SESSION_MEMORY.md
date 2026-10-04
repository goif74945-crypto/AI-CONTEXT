# Temporary Execution Memory — NEXY Proof-Preserving Resource Governor Lab

Status: PARTIAL
Truth class: REPO_FACT_FOR_THIS_TASK_RECORD
Durable session code: CHAT-20261005-0122-NEXY-RESOURCE-GOVERNOR
Platform-native ChatGPT conversation ID: UNKNOWN_NOT_EXPOSED
Started local: 2026-10-05T01:22:00+07:00
Target repository: goif74945-crypto/AI-CONTEXT
Target branch: main
Authorized write scope: คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-RESOURCE-GOVERNOR/
Protected mutation scope: every repository whose name contains NEXY.AI; all existing sibling artifacts outside this new namespace.

## Objective
Design, implement, test, and document an AI-proposed deterministic resource governor for NEXY that can allocate workers/verifiers under token, cost, latency, capability, privacy, and independence constraints without ever weakening authority or required verification.

## Source-grounded invariants
- NEXY is a deterministic AI control hub; SWARM/AGENT are labor, CORE/JUDGE retain authority.
- Never guess on material ambiguity.
- One legal verified output or freeze/silence is the release boundary.
- USER LAW / governing authority is not reducible by optimization.
- Design, implementation, runtime, and deployment remain separate truth domains.
- Current source denominator is 837 normalized requirement rows; this lab does not promote new current-build requirements.

## Distinctness check
Recent sibling work already covers experience compilation, human authority interaction integrity, proof-carrying execution, context compilation, failure atlas, scope firewall, temporal compatibility, uncertainty debt, verification economy/proof scheduling, evidence graphs, capability admission, survivability, epistemic economics, idempotency/replay, and compatibility evolution.
Repository commit search returned no matching prior work for: resource budget governor; token latency cost budget; multi-agent orchestrator; model routing; quality budget; cost latency quality.

This lab therefore focuses on RESOURCE ALLOCATION across worker/model choices, not proof-job scheduling. It preserves mandatory proof requirements but optimizes execution resources beneath them.

## Selected AI-proposed concept
NEXY Proof-Preserving Resource Governor (NPRG).

The governor is advisory/planning infrastructure below CORE/JUDGE. It may select a feasible resource plan, but it cannot declare a task correct, verified, deployed, or canonical.

## Planned deliverables
1. manifest/task contract
2. architecture + invariants
3. requirement ledger
4. machine-readable contract schema
5. deterministic Python reference implementation
6. adversarial/unit tests and scenario corpus
7. failure/recovery model
8. non-governing integration proposal
9. research backlog
10. validation evidence
11. final audit and closed resumable state

## Verification target
- E0: committed artifacts exist and can be re-read.
- E1: Python compile + JSON parse.
- E2: executed unit/adversarial tests for the reference implementation.
- E3-E7: NOT_VERIFIED and not claimed.
- NEXY.AI product implementation/runtime/deployment: NOT_VERIFIED and out of mutation scope.

## Stop conditions
- Any step would mutate a repository whose name contains NEXY.AI.
- A required authoritative constraint conflicts and cannot be resolved.
- A write would overwrite concurrent/sibling work outside this namespace.
- Secret/credential material would be persisted.
- Verification evidence does not support the intended claim.

## Resume
Read this file first. Continue only within the authorized namespace. Do not infer completion from file presence. Final status must be based on the validation report and final audit.

## Closure / Final verified state
Bounded NPRG lab acceptance status: PASS.
Overall original user objective status: PARTIAL because the literal multi-tens-of-hours continuous/background duration requirement cannot execute inside one synchronous chat turn and is not claimed.

Final audit:
- path: 09_FINAL_AUDIT.md
- Git blob SHA: 36ca8e4923c54d4a808c80acf03916e960321b3e

Verified evidence:
- E0: 18 core local validated artifacts matched the corresponding AI-CONTEXT Git blob SHAs exactly.
- E1: Python compile PASS; JSON parse PASS; Draft 2020-12 schema check PASS; 4 positive fixture payloads PASS; zero+zero worker-token negative payload correctly rejected.
- E2: 16/16 unit/adversarial/property tests PASS; 300 fixed-seed generated task/inventory cases included.
- Synthetic benchmark: 250,000 worker/verifier pairs median 423.918 ms in this Python 3.13.5 container; environment-specific, not a production SLA.
- E3-E7: NOT_VERIFIED.
- NEXY.AI implementation/runtime/deployment: NOT_VERIFIED and not mutated.

Defects corrected before closure:
1. feasible-pair materialization replaced by streaming best-candidate selection;
2. self-verification forbidden;
3. source split into models/governor/serde;
4. stale requirement-ledger helper names corrected;
5. schema aligned with nonzero worker-token invariant;
6. README artifact index completed.

Concurrency incident:
A GitHub 409 occurred because another AI-CONTEXT writer moved main during an isolated validation-report update. Recovery re-fetched and retried only this namespace/file. No force, reset, rebase, destructive update, or sibling overwrite was used.

Resume rule:
Read 09_FINAL_AUDIT.md before extending this lab. Any future promotion into canonical/current NEXY build scope requires explicit authority plus fresh implementation/integration/runtime evidence. Do not treat this proposal as current NEXY product truth.
