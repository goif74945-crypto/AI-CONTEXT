FAILURE_ID: NEXY-CLOSED-LOOP-BUILDER-01-BOOT-20260924
context: NEXY closed-loop Builder first execution
failure_class: MISSING_OPERATIONAL_CONTROL_STATE
symptom: no READY command for pair NEXY-CLOSED-LOOP-01 and no live worker/claim registry instance found in canonical control-plane paths
proof:
  - pair-id search returned zero results
  - worker-id search returned zero results
  - queue directory has only policy/schema/examples/validation artifacts
  - workers directory has only policy/schema/examples/validation artifacts
  - claims directory has only policy/schema/examples/validation artifacts
failed_approach: none; no unsafe execution attempted
recovery: Auditor publishes canonical live READY command and operational claim state; Builder refreshes and revalidates
boundary: do not create a defect/command or execute golden examples
prevention: require canonical live-state discovery path in dispatch protocol
status: WAITING_FOR_COMMAND
trace_id: NEXY-CLOSED-LOOP-BUILDER-01-BOOT-20260924
