FAILURE_ID: NEXY-RUNTIME-ATTEMPT-20260924-RDC-DISCONNECTED
context: real desktop execution attempt
cause: Remote Desktop Commander transport has no connected device even though user reports machine is powered on
proof:
  - list_devices: DESKTOP-FOB7IK8 status=offline
  - ping device: No devices available; please connect a device to use remote tools
boundary:
  - machine power state is not the same as connector availability
  - no test/build result may be inferred
recovery: reconnect Desktop Commander transport, then retry commands on exact branch HEAD
status: ACTIVE
trace_id: NEXY-RUNTIME-ATTEMPT-20260924-RDC-DISCONNECTED
