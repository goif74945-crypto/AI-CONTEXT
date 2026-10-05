# Queue retry-cap integration evidence

TASK_ID: TASK-QUEUE-RETRY-CAP-001
INTEGRATION_SHA: 5fff467be07fd45993b2e3cfa07cc319dc4fa755
PR: 62

Focused execution and compile passed for the exact target source blobs. Exact-head GitHub workflows at the integration SHA fail before any step starts. The immediately preceding base SHA c1f94b2c59b787a7761079362a82aefbbfca9855 shows the same zero-step failure in both exact-head workflows, so current evidence classifies this as a pre-existing runner/startup blocker rather than a patch regression.

Runs:
- integration Exact HEAD: 37360868127
- integration Six-system: 37360868111
- pre-base Exact HEAD: 37360804656
- pre-base Six-system: 37360804659

Shared Railway validator remains leased by T-B7E4C2A1; no takeover performed.
