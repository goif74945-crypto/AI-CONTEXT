# 06 — Integration and Promotion Gate

## Current status
Supplemental research only. Reference tests grant zero authority to enter the current NEXY build.

## Promotion prerequisites
An authorized future task must resolve:
1. spec authority/version and module ownership;
2. canonical terminology;
3. task-local/execution-local/global FREEZE semantics;
4. binding to USER LAW/AUTH/RBAC/LAW with monotonic restriction proof;
5. provider-specific canonical resource IDs and alias tests;
6. race-safe check + budget reservation + dispatch + crash/replay;
7. issuer/subject/plan/scope/version/expiry integrity and approved signing if required;
8. local/distributed revocation semantics;
9. Event/Audit/Freeze/Security observability without duplicate truth;
10. backend-authoritative UX;
11. explicit compatibility/migration with no permissive fallback;
12. evidence gates E1-E6 as applicable.

## Monotonic authority
```text
USER LAW / AUTH / RBAC / LAW
          |
          | may restrict
          v
       TASK PLAN
          |
          v
   AUTHORITY LEASE
          |
          | may restrict only
          v
 EXECUTOR / TOOL ADAPTER
```

A lease must never turn upstream denial into allow.

## Explicit non-promotion rule
Reference code, unit tests, and these documents are insufficient evidence to change NEXY runtime or repository behavior.
