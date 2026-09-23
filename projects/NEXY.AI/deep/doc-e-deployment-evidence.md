# NEXY.AI — DOC-E Deployment Evidence Pack

## Authority
SOURCE-BUILD/DEPLOYMENT SPEC. This file records what counts as **deployment proof**. It is not itself proof that deployment passed.

The source explicitly states:

**DOC-E is not checklist text only. DOC-E must contain proof artifacts.**

Build obligation comes from DOC-C; deployment approval comes from DOC-E.

## 1. Required evidence artifacts

Named evidence IDs:
- **E1** — contract test report.
- **E2** — API schema snapshot.
- **E3** — migration applied + rollback tested.
- **E4** — state-machine tests pass.
- **E5** — RBAC tests pass.
- **E6** — auth-abuse simulation report.
- **E7** — queue-worker readiness proof.
- **E8** — observability/alarm verification.
- **E9** — incident-drill result.
- **E10** — deploy runbook with commands.
- **E11** — release signoff record.
- **E12** — rollback-playbook execution proof.

A design document saying these should pass is not equivalent to the artifacts existing.

## 2. Minimum evidence-item format
Every proof item should bind at least:
- artifact name;
- commit hash;
- environment;
- date;
- operator;
- command/test identifier;
- result;
- log link/reference;
- screenshot or output excerpt where relevant;
- explicit PASS/FAIL.

This prevents “tested” from being an untraceable prose claim.

## 3. Deployment runbook skeleton
The source’s minimum operational sequence:
1. install;
2. migrate;
3. seed minimum roles;
4. start queue;
5. start API;
6. start web;
7. verify health endpoints;
8. run smoke tests;
9. verify logs flowing;
10. verify freeze path;
11. deploy;
12. execute rollback if needed.

The actual production runbook must replace generic verbs with exact commands/environment identifiers.

## 4. Release signoff
No deploy without:
- engineering signoff;
- security signoff;
- migration signoff;
- rollback verification;
- monitoring verification.

Signoff is an evidence artifact, not a ceremonial checkbox.

## 5. Queue readiness proof
Must demonstrate:
- enqueue works;
- worker consumes;
- invalid payload produces the correct blocking/freeze behavior;
- stale jobs expire;
- idempotency blocks duplicate execution.

This is especially important because queue/idempotency semantics are part of the canonical execution contract, not optional infrastructure.

## 6. Monitoring/alarm verification
Alerts must be proven for at least:
- auth abuse;
- freeze incident;
- worker down;
- queue backlog;
- database failure;
- release-policy failure.

Merely having logging code is insufficient; alarm delivery/triggering must be exercised.

## 7. Incident-drill evidence
DOC-E expects an actual incident exercise tied to:
- incident identifiers;
- event/audit/security/freeze logs;
- recovery or containment path;
- operator actions;
- final outcome.

The incident graph defined in DOC-C should be reconstructable from the evidence.

## 8. Migration / rollback evidence
Migration readiness requires:
- migration applied on the target-like environment;
- resulting schema/state verified;
- rollback path executed, not just documented;
- data/revision integrity checked after rollback where applicable.

## 9. Contract / API evidence
E1/E2 should prove:
- current canonical contracts;
- runtime schema enforcement;
- response envelope;
- error-code behavior;
- mutating-route auth/CSRF/idempotency requirements;
- no accidental contract drift.

Unreviewed snapshot drift is a release blocker under the build-spec test gates.

## 10. Auth-abuse simulation
E6 must exercise abuse cases rather than only happy-path login:
- invalid/expired OTAC;
- consumed/reused OTAC;
- attempt exhaustion;
- resend cooldown;
- repeated lock cycles;
- device mismatch;
- revoked session;
- CSRF failure;
- rate-limit behavior.

Security incidents/audit linkage should be visible in evidence.

## 11. Freeze-path proof
Deployment is not valid if only success paths work.
The environment must prove:
- a blocking condition reaches FREEZE;
- output release is blocked;
- UI/API reflect the frozen state truthfully;
- incident linkage exists;
- recovery only succeeds through permitted actor/guard path;
- pending/old execution is not silently resumed.

## 12. Evidence status semantics
For future AI-CONTEXT/audits use only:
- PASS — proof artifact exists and supports claim.
- FAIL — proof demonstrates violation.
- PARTIAL — some required proof exists but not the whole contract.
- NOT VERIFIED — no sufficient execution/deployment proof.
- BLOCKED — external dependency prevents verification.
- UNKNOWN — evidence/state could not be determined.

Do not infer PASS from source code, docs, file names, expected architecture or CI configuration alone.

## 13. Relationship to implementation readiness
The source’s gap-closure section distinguishes:
- API definition;
- executable state matrix;
- product-design pack;
- migration-ready storage;
- hardened auth;
- evidence-artifact pack.

Even if all design packs are complete, release remains **NON-DEPLOYABLE** until the relevant DOC-E proof artifacts exist for the exact commit/environment being released.

## 14. Evidence identity rule
A valid evidence artifact should bind to the exact build/commit/environment it proves. Evidence from an older commit, different branch or different environment must not be silently reused as proof of the current deployment.

## 15. Core principle
**Specification says what must be true.  
Implementation attempts to make it true.  
DOC-E proves whether it was true for a specific build/environment.**

These three states must never be collapsed.
