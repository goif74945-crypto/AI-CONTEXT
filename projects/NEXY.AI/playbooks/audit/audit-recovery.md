# PLAYBOOK — Audit Recovery

## PURPOSE
Verify that failures recover through legal, deterministic, integrity-preserving paths rather than hidden state invention.

## PROCEDURE
1. Identify failure classes and recovery mechanism.
2. Resolve exact authority allowed to recover.
3. Resolve snapshot/WAL/queue/session/state dependencies.
4. Identify last durable/verified state boundary.
5. Test failure injection at each critical step.
6. Verify recovery never resumes an illegal/stale execution path.
7. Verify replay ordering and state-hash checks where applicable.
8. Verify partial/incomplete writes are handled by explicit rules.
9. Verify repeated recovery failure escalates to FREEZE/manual intervention where specified.
10. Verify incident/audit evidence is preserved.
11. Verify unrelated systems remain isolated when local containment is intended.
12. Verify rollback itself is tested.

## FAILURE INJECTION
- process crash before/after durable write;
- queue worker crash around ACK/side effect;
- partial snapshot;
- corrupt WAL/event;
- dependency outage;
- invalid recovery actor;
- stale build/spec hash;
- repeated crash loop;
- lost network/region;
- storage read error.

## FORBIDDEN RECOVERY
- auto-heal by inventing missing history;
- skip corrupted authoritative history;
- resume old job after recovery when spec says new cycle;
- bypass freeze guard;
- recover against mismatched build/spec/state hashes.

## PASS
Recovery must reproduce a legal state with evidence; otherwise FAIL/NOT_VERIFIED/FREEZE-class finding.
