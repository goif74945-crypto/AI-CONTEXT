# Failure Model — Resource Governor Proposal

## Contract failures
These are invalid inputs and should fail fast before planning:
- empty IDs/domains;
- duplicate `agent_id`;
- unsupported role/objective;
- negative prices/latency/token estimates;
- evidence class outside E0-E7;
- malformed quality score.

Reference behavior: raise `ContractError`. A production integration should translate this into a governed CORE-visible freeze/error event rather than crash uncontrolled.

## Planning freeze reasons
- `NO_ELIGIBLE_WORKER`
- `NO_ELIGIBLE_VERIFIER`
- `INDEPENDENCE_DOMAIN_COLLISION`
- `SELF_VERIFICATION_FORBIDDEN`
- `TOKEN_BUDGET_EXCEEDED`
- `COST_BUDGET_EXCEEDED`
- `LATENCY_BUDGET_EXCEEDED`
- `NO_FEASIBLE_ALLOCATION`

Candidate-level elimination reasons additionally expose inactive/quarantined state, insufficient clearance, missing role/capability, insufficient context, evidence capability and quality-floor failures.

## Fail-closed laws
1. Missing legal worker → FREEZE.
2. Required verifier absent → FREEZE.
3. Required independent verification but only same-domain verifier exists → FREEZE.
4. Required plan exceeds any hard user/policy budget → FREEZE.
5. Required evidence class above verifier capability → FREEZE.
6. Quarantined agent can never win because price/latency/quality is attractive.
7. Planning success never becomes evidence PASS.

## Recovery
A new planning attempt is legal only when an input fact changes, for example:
- budget authorization increases;
- a compliant verifier becomes available;
- quarantine is lifted through an authorized process;
- task scope/capability requirements are explicitly changed;
- current price/latency metadata is refreshed;
- governing policy changes through its authorized path.

The governor must not mutate those facts itself merely to obtain a feasible answer.
