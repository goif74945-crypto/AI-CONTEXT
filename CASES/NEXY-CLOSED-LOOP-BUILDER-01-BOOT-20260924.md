CASE_ID: NEXY-CLOSED-LOOP-BUILDER-01-BOOT-20260924
title: Builder boot with no live executable queue state
cause: canonical control-plane contains schemas, policies and examples but no discovered live queue/worker/claim instance for the requested pair.
impact: Builder cannot validly register, claim, lease, resolve TARGET_REPO/TARGET_BRANCH/EXPECTED_HEAD, or mutate implementation.
safe_action: remain WAITING_FOR_COMMAND and preserve evidence; never promote examples into live state.
prevention: publish canonical live execution-state artifacts or an explicit canonical runtime endpoint before dispatching Builder.
status: OPEN_WAITING
trace_id: NEXY-CLOSED-LOOP-BUILDER-01-BOOT-20260924
