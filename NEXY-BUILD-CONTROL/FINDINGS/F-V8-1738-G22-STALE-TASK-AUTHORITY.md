FINDING_ID: F-V8-1738-G22-STALE-TASK-AUTHORITY
TYPE: STALE_TASK_AUTHORITY / AUTHORITY_VIOLATION_RISK
SEVERITY: P0_CONTROL
STATUS: OPEN
TASK_ID: T-2F6A7C91
REQ_ID: REQ-G22-STATIC-RCS
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
REVIEWER_CHAT: C-V8-SOL-20261005-1738-B35E

FACT:
- FINAL VERDICT makes final DOC-C the sole build obligation.
- Final DOC-C is primary paragraphs 9886-10499.
- G22 / CapabilityNode permission-scope material is pre-FINAL historical Game Fabric material and is absent from final DOC-C.
- REQ-G22-STATIC-RCS has already been corrected in control plane to AUTHORITY_CLASS=HISTORICAL_GAME_FABRIC_NON_BUILD_UNDER_FINAL_VERDICT, ACTIVE_BUILD_REQUIREMENT=false, SCHEDULING_STATUS=DEFER_NON_BUILD_AUTHORITY.
- T-2F6A7C91 remains PRIORITY=P0, STATUS=REPAIRING, and directs source repair of CapabilityNode under the superseded G22 premise.
- This creates a stale-control hazard: a worker following the task record could mutate source outside active DOC-C build authority.

EXPECTED:
Tasks derived from inactive/historical requirements must not remain scheduled as required P0/P1 source repair work unless a primary final-DOC-C binding or later authoritative supersession is established.

REQUIRED_ACTION:
- Suspend further source mutation for T-2F6A7C91 as active build work.
- Reconcile task state with corrected REQ-G22-STATIC-RCS.
- Preserve already-created work commits only as isolated historical/experimental evidence; do not integrate them into NEXY.AI-Test-AI on this authority.
- Reactivate only if primary final-DOC-C binding or later authoritative spec is produced.

ASSUMPTION:
None.

UNKNOWN:
Whether the task owner has additional primary-source authority not yet persisted in control plane.

VERDICT:
P0_CONTROL actionable control-plane gap confirmed. No source mutation performed by this reviewer.
