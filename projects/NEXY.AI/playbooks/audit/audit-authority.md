# PLAYBOOK — Audit Authority

## PURPOSE
Detect authority inversion, stale Canon use, illegal override and scope leakage.

## PROCEDURE
1. Load authority graph.
2. Load supersession graph.
3. Load unresolved conflict registry.
4. Load scope registry.
5. Identify actor/module making the decision/mutation.
6. Trace who may propose, validate, decide, enforce, freeze, recover and persist.
7. Compare implementation permission paths with governance.
8. Search for force/bypass/debug/maintenance shortcuts.
9. Check UI visibility vs backend authorization.
10. Check historical/vision rules are not promoted into current build accidentally.
11. Check owner/system recovery paths against current Canon.

## RED FLAGS
- SWARM/model output treated as truth authority.
- UI directly mutates LAW/VAULT.
- Architect/owner ad-hoc override bypasses deterministic operation law.
- future Universe/Game/Robotics rules treated as current DOC-C build requirements without promotion.
- superseded constants/rules still active.
- authorization encoded only in presentation layer.

## OUTPUT
Authority path, inversion findings, stale-claim findings, and exact governing source.
