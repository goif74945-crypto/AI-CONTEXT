CASE_ID: NEXY-RAILWAY-VALIDATION-ATTEMPT-20260924
cause: connected execution plugin exists, but private-repository source authorization is missing at the Railway GitHub integration boundary.
impact: build/test execution cannot start despite valid Railway account and configured validation service.
fix_attempted:
  - isolated Railway project creation
  - explicit repo/branch attachment
  - validation build command configuration
  - repeated deployment trigger
  - Railway Agent exact branch staging
prevention: verify provider-to-GitHub private repository authorization before treating a connected deployment plugin as an executable runner.
status: OPEN_EXTERNAL_AUTHORIZATION
trace_id: NEXY-RAILWAY-VALIDATION-ATTEMPT-20260924
