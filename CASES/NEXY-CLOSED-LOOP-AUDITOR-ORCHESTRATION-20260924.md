CASE_ID: NEXY-CLOSED-LOOP-AUDITOR-ORCHESTRATION-20260924
title: Cross-chat Auditor/Builder loop with idle skill creation
cause: user requires the Auditor chat to verify Builder work continuously across turns and use idle periods for NEXY Skill creation.
decision:
  - use AI-CONTEXT live control files as cross-chat truth
  - Builder work always preempts idle skill creation
  - routine state is persisted instead of narrated to the user
  - no hidden/background execution claims
status: ACTIVE_PROTOCOL
evidence:
  - projects/NEXY.AI/control-plane/CLOSED-LOOP-PAIR-PROTOCOL.md
  - projects/NEXY.AI/control-plane/live/pair-state.json
trace_id: NEXY-CLOSED-LOOP-AUDITOR-ORCHESTRATION-20260924
