LEDGER_ID: NEXY-RAILWAY-VALIDATION-ATTEMPT-20260924
claim: isolated Railway validation project/service was created.
proof: Railway create_project/create_deployment/update_service outputs.
status: VERIFIED

claim: validation build command is configured on the service.
proof: Railway get_service_config shows the custom build command.
status: VERIFIED

claim: no Railway test command executed.
proof: list_deployments is empty; latestDeployment is null.
status: VERIFIED

claim: repository exists and is private.
proof: GitHub repository metadata private=true visibility=private.
status: VERIFIED

claim: Railway's GitHub source authorization is insufficient for this private repo.
proof: Railway Agent reports repository inaccessible after exact branch was staged; no deployment record was created.
status: VERIFIED_FOR_INTEGRATION_BOUNDARY

claim: Desktop Commander remains unavailable.
proof: list_devices reports DESKTOP-FOB7IK8 status=offline on retry.
status: VERIFIED_AT_TIMESTAMP
trace_id: NEXY-RAILWAY-VALIDATION-ATTEMPT-20260924
