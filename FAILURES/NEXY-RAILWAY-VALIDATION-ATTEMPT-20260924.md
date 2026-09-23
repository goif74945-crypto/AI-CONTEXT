FAILURE_ID: NEXY-RAILWAY-VALIDATION-ATTEMPT-20260924
context: isolated Railway test execution
cause: Railway can authenticate the user and create/configure services, but its GitHub integration cannot read the private repository goif74945-crypto/NEXY.AI-
proof:
  - GitHub repo exists and visibility=private
  - Railway create_deployment returned triggered but list_deployments remained empty
  - Railway Agent explicitly reported repository inaccessible and branch update staged without deployment
  - service config contains source repo and validation build command
impact: no validation command reached execution
recovery: grant Railway GitHub App repository access, or reconnect Desktop Commander
status: ACTIVE
trace_id: NEXY-RAILWAY-VALIDATION-ATTEMPT-20260924
