# PLAYBOOK — Audit FSM

## PURPOSE
Verify one FSM's states, transitions, guards, event ownership, persistence and illegal-path blocking.

## PROCEDURE
1. Identify exact FSM; never merge same-named states across FSMs.
2. Resolve source authority and registry JSON.
3. Enumerate legal states and transitions.
4. For each transition inspect:
   FROM / EVENT / GUARD / ACTION / TO / FAILURE / AUDIT_EVENT.
5. Verify event owner/actor permissions.
6. Verify guard enforcement before side effect.
7. Verify state persistence/atomicity.
8. Test illegal transitions.
9. Test duplicate/reordered events where relevant.
10. Test crash/recovery/replay boundaries.
11. Verify STOP/FREEZE terminal/side semantics.
12. Compare implementation and tests against registry.

## REQUIRED NEGATIVE CASES
- illegal FROM→TO;
- wrong event owner;
- false guard;
- duplicate event;
- partial action/persist crash;
- recovery bypass;
- transition skipped through shortcut;
- state display inconsistent with backend truth.

## PASS
All legal transitions behave correctly and illegal paths are blocked with required evidence.
