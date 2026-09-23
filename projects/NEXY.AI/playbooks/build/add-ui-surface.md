# PLAYBOOK — Add UI Surface

## PRECONDITIONS
- Surface is authorized by DOC-D/current product scope or explicit extension.
- Backend truth/permission contract already exists or is part of authorized dependency work.
- UI is not becoming an authority owner.

## REQUIRED CONTEXT
- DOC-D screen/component contract;
- UI Truth invariant;
- API/permission contracts;
- relevant FSM states;
- errors/incidents;
- accessibility/mobile/desktop behavior where specified;
- implementation UI map;
- E2E acceptance matrix.

## IMPLEMENTATION SEQUENCE
1. Define screen/component purpose and primary/secondary actions.
2. Map every displayed state to authoritative backend state.
3. Map every action to an authorized API/command.
4. Define role visibility and backend permission enforcement.
5. Define loading/pending/error/freeze/empty states.
6. Define dangerous-action confirmation/recovery semantics.
7. Implement no optimistic fake success for blocking actions.
8. Preserve FREEZE visibility and incident linkage.
9. Add component/static tests where useful.
10. Add E2E for critical user flows.
11. Test denied role, backend error, stale request, frozen system.

## UI TRUTH NEGATIVE TESTS
- backend FREEZE while prior success is visible;
- permission-hidden control called manually;
- pending request shown as completed;
- partial/unverified output exposed as released;
- recovery button shown to unauthorized role.

## DONE
The surface renders backend truth faithfully and critical flows have the required E2E evidence.
